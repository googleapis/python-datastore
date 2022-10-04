# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import pytest

from google.cloud.datastore.aggregation import CountAggregation, AggregationQuery

from tests.unit.test_query import _make_query, _make_client

_PROJECT = "PROJECT"


def test_count_aggregation_to_pb():
    from google.cloud.datastore_v1.types import query as query_pb2

    count_aggregation = CountAggregation(limit=10, alias="total")

    expected_aggregation_query_pb = query_pb2.AggregationQuery.Aggregation()
    expected_aggregation_query_pb.count.up_to = count_aggregation.limit
    expected_aggregation_query_pb.alias = count_aggregation.alias
    assert count_aggregation._to_pb() == expected_aggregation_query_pb


@pytest.fixture
def client():
    return _make_client()


def test_pb_over_query(client):
    from google.cloud.datastore.query import _pb_from_query

    query = _make_query(client)
    aggregation_query = _make_aggregation_query(client=client, query=query)
    pb = aggregation_query._to_pb()
    assert pb.nested_query == _pb_from_query(query)
    assert pb.aggregations == []


def test_pb_over_query_with_count(client):
    from google.cloud.datastore.query import _pb_from_query

    query = _make_query(client)
    aggregation_query = _make_aggregation_query(client=client, query=query)

    aggregation_query.count(alias="total", limit=10)
    pb = aggregation_query._to_pb()
    assert pb.nested_query == _pb_from_query(query)
    assert len(pb.aggregations) == 1
    assert pb.aggregations[0] == CountAggregation(alias="total", limit=10)._to_pb()


def test_pb_over_query_with_add_aggregation(client):
    from google.cloud.datastore.query import _pb_from_query

    query = _make_query(client)
    aggregation_query = _make_aggregation_query(client=client, query=query)

    aggregation_query.add_aggregation(CountAggregation(alias="total", limit=10))
    pb = aggregation_query._to_pb()
    assert pb.nested_query == _pb_from_query(query)
    assert len(pb.aggregations) == 1
    assert pb.aggregations[0] == CountAggregation(alias="total", limit=10)._to_pb()


def test_pb_over_query_with_add_aggregations(client):
    from google.cloud.datastore.query import _pb_from_query

    aggregations = [
        CountAggregation(alias="total", limit=10),
        CountAggregation(alias="all", limit=2),
    ]

    query = _make_query(client)
    aggregation_query = _make_aggregation_query(client=client, query=query)

    aggregation_query.add_aggregations(aggregations)
    pb = aggregation_query._to_pb()
    assert pb.nested_query == _pb_from_query(query)
    assert len(pb.aggregations) == 2
    assert pb.aggregations[0] == CountAggregation(alias="total", limit=10)._to_pb()
    assert pb.aggregations[1] == CountAggregation(alias="all", limit=2)._to_pb()


def test_query_fetch_defaults_w_client_attr(client):
    from google.cloud.datastore.aggregation import AggregationResultIterator

    query = _make_query(client)
    aggregation_query = _make_aggregation_query(client=client, query=query)
    iterator = aggregation_query.fetch()

    assert isinstance(iterator, AggregationResultIterator)
    assert iterator._aggregation_query is aggregation_query
    assert iterator.client is client
    assert iterator._retry is None
    assert iterator._timeout is None


def test_query_fetch_w_explicit_client_w_retry_w_timeout(client):
    from google.cloud.datastore.aggregation import AggregationResultIterator

    other_client = _make_client()
    query = _make_query(client)
    aggregation_query = _make_aggregation_query(client=client, query=query)
    retry = mock.Mock()
    timeout = 100000

    iterator = aggregation_query.fetch(
        client=other_client, retry=retry, timeout=timeout
    )

    assert isinstance(iterator, AggregationResultIterator)
    assert iterator._aggregation_query is aggregation_query
    assert iterator.client is other_client
    assert iterator._retry == retry
    assert iterator._timeout == timeout


def test_iterator_constructor_defaults():
    query = object()
    client = object()
    aggregation_query = AggregationQuery(client=client, query=query)
    iterator = _make_aggregation_iterator(aggregation_query, client)

    assert not iterator._started
    assert iterator.client is client
    assert iterator.page_number == 0
    assert iterator.num_results == 0
    assert iterator._aggregation_query is aggregation_query
    assert iterator._more_results
    assert iterator._retry is None
    assert iterator._timeout is None


def test_iterator_constructor_explicit():
    query = object()
    client = object()
    aggregation_query = AggregationQuery(client=client, query=query)
    retry = mock.Mock()
    timeout = 100000

    iterator = _make_aggregation_iterator(
        aggregation_query,
        client,
        retry=retry,
        timeout=timeout,
    )

    assert not iterator._started
    assert iterator.client is client
    assert iterator.page_number == 0
    assert iterator.num_results == 0
    assert iterator._aggregation_query is aggregation_query
    assert iterator._more_results
    assert iterator._retry == retry
    assert iterator._timeout == timeout


def test_iterator__build_protobuf_empty():
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.query import Query

    client = _Client(None)
    query = Query(client)
    aggregation_query = AggregationQuery(client=client, query=query)
    iterator = _make_aggregation_iterator(aggregation_query, client)

    pb = iterator._build_protobuf()
    expected_pb = query_pb2.AggregationQuery()
    expected_pb.nested_query = query_pb2.Query()
    assert pb == expected_pb


def test_iterator__build_protobuf_all_values():
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.query import Query

    client = _Client(None)
    query = Query(client)
    aggregation_query = AggregationQuery(client=client, query=query)

    iterator = _make_aggregation_iterator(aggregation_query, client)
    iterator.num_results = 4

    pb = iterator._build_protobuf()
    expected_pb = query_pb2.AggregationQuery()
    expected_pb.nested_query = query_pb2.Query()
    assert pb == expected_pb


def test_iterator__process_query_results():
    from google.cloud.datastore_v1.types import query as query_pb2
    from google.cloud.datastore.aggregation import AggregationResult

    iterator = _make_aggregation_iterator(None, None)

    aggregation_pbs = [AggregationResult(alias="total", value=1)]

    more_results_enum = query_pb2.QueryResultBatch.MoreResultsType.NOT_FINISHED
    response_pb = _make_aggregation_query_response(aggregation_pbs, more_results_enum)
    result = iterator._process_query_results(response_pb)
    assert result == [
        r.aggregate_properties for r in response_pb.batch.aggregation_results
    ]
    assert iterator._more_results


class _Client(object):
    def __init__(self, project, datastore_api=None, namespace=None, transaction=None):
        self.project = project
        self._datastore_api = datastore_api
        self.namespace = namespace
        self._transaction = transaction

    @property
    def current_transaction(self):
        return self._transaction


def _make_aggregation_query(*args, **kw):
    from google.cloud.datastore.aggregation import AggregationQuery

    return AggregationQuery(*args, **kw)


def _make_aggregation_iterator(*args, **kw):
    from google.cloud.datastore.aggregation import AggregationResultIterator

    return AggregationResultIterator(*args, **kw)


def _make_aggregation_query_response(aggregation_pbs, more_results_enum):
    from google.cloud.datastore_v1.types import datastore as datastore_pb2
    from google.cloud.datastore_v1.types import aggregation_result

    aggregation_results = []
    for aggr in aggregation_pbs:
        result = aggregation_result.AggregationResult()
        result.aggregate_properties.alias = aggr.alias
        result.aggregate_properties.value = aggr.value
        aggregation_results.append(result)

    return datastore_pb2.RunAggregationQueryResponse(
        batch=aggregation_result.AggregationResultBatch(
            aggregation_results=aggregation_results,
            more_results=more_results_enum,
        )
    )


def _make_datastore_api_for_aggregation(*results):
    if len(results) == 0:
        run_aggregation_query = mock.Mock(return_value=None, spec=[])
    else:
        run_aggregation_query = mock.Mock(side_effect=results, spec=[])

    return mock.Mock(
        run_aggregation_query=run_aggregation_query, spec=["run_aggregation_query"]
    )
