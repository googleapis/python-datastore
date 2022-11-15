# # Copyright 2022 Google LLC
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
#
# """Create / interact with Google Cloud Datastore aggregation queries."""
import abc
from abc import ABC

from google.api_core import page_iterator

from google.cloud.datastore_v1.types import entity as entity_pb2
from google.cloud.datastore_v1.types import query as query_pb2
from google.cloud.datastore import helpers
from google.cloud.datastore.query import _pb_from_query


_NOT_FINISHED = query_pb2.QueryResultBatch.MoreResultsType.NOT_FINISHED
_NO_MORE_RESULTS = query_pb2.QueryResultBatch.MoreResultsType.NO_MORE_RESULTS

_FINISHED = (
    _NO_MORE_RESULTS,
    query_pb2.QueryResultBatch.MoreResultsType.MORE_RESULTS_AFTER_LIMIT,
    query_pb2.QueryResultBatch.MoreResultsType.MORE_RESULTS_AFTER_CURSOR,
)


class BaseAggregation(ABC):
    """
    Base class representing an Aggregation operation in Datastore
    """

    @abc.abstractmethod
    def _to_pb(self):
        """
        Convert this instance to the protobuf representation
        """


class CountAggregation(BaseAggregation):
    """
    Representation of a "Count" aggregation query.

    :type alias: str
    :param alias: The alias for the aggregation.

    :type value: int
    :param value: The resulting value from the aggregation.

    """

    def __init__(self, alias=None):
        self.alias = alias

    def _to_pb(self):
        """
        Convert this instance to the protobuf representation
        """
        aggregation_pb = query_pb2.AggregationQuery.Aggregation()
        aggregation_pb.count = query_pb2.AggregationQuery.Aggregation.Count()
        aggregation_pb.alias = self.alias
        return aggregation_pb


class AggregationResult(object):
    """
    A class representing result from Aggregation Query

    :type alias: str
    :param alias: The alias for the aggregation.

    :type value: int
    :param value: The resulting value from the aggregation.

    """

    def __init__(self, alias, value):
        self.alias = alias
        self.value = value

    def __repr__(self):
        return "<Aggregation alias=%s, value=%s>" % (self.alias, self.value)


class AggregationQuery(object):
    """An Aggregation query against the Cloud Datastore.

    This class serves as an abstraction for creating aggregations over query
    in the Cloud Datastore.

    :type client: :class:`google.cloud.datastore.client.Client`
    :param client: The client used to connect to Datastore.

    :type query: :class:`google.cloud.datastore.query.Query`
    :param query: The query used for aggregations.
    """

    def __init__(
        self,
        client,
        query,
    ):

        self._client = client
        self._nested_query = query
        self._aggregations = []

    @property
    def project(self):
        """Get the project for this AggregationQuery.

        :rtype: str
        :returns: The project for the query.
        """
        return self._nested_query._project or self._client.project

    @property
    def namespace(self):
        """The nested query's namespace

        :rtype: str or None
        :returns: the namespace assigned to this query
        """
        return self._nested_query._namespace or self._client.namespace

    def _to_pb(self):
        """
        Returns the protobuf representation for this Aggregation Query
        """
        pb = query_pb2.AggregationQuery()
        pb.nested_query = _pb_from_query(self._nested_query)
        for aggregation in self._aggregations:
            aggregation_pb = aggregation._to_pb()
            pb.aggregations.append(aggregation_pb)
        return pb

    def count(self, alias=None):
        """
        Adds a count over the nested query

        :type alias: str
        :param alias: (Optional) The alias for the count
        """
        count_aggregation = CountAggregation(alias=alias)
        self._aggregations.append(count_aggregation)
        return self

    def add_aggregation(self, aggregation):
        """
        Adds an aggregation operation to the nested query

        :type aggregation: :class:`google.cloud.datastore.aggregation.BaseAggregation`
        :param aggregation: An aggregation operation, e.g. a CountAggregation
        """
        self._aggregations.append(aggregation)

    def add_aggregations(self, aggregations):
        """
        Adds a list of aggregations to the nested query
        :type aggregations: list
        :param aggregations: a list of aggregation operations
        """
        self._aggregations.extend(aggregations)

    def fetch(
        self,
        client=None,
        limit=None,
        eventual=False,
        retry=None,
        timeout=None,
        read_time=None,
    ):
        """Execute the Aggregation Query; return an iterator for the aggregation results.

        For example:

        .. testsetup:: aggregation-query-fetch

            import uuid

            from google.cloud import datastore

            unique = str(uuid.uuid4())[0:8]
            client = datastore.Client(namespace='ns{}'.format(unique))


        .. doctest:: aggregation-query-fetch

            >>> andy = datastore.Entity(client.key('Person', 1234))
            >>> andy['name'] = 'Andy'
            >>> sally = datastore.Entity(client.key('Person', 2345))
            >>> sally['name'] = 'Sally'
            >>> bobby = datastore.Entity(client.key('Person', 3456))
            >>> bobby['name'] = 'Bobby'
            >>> client.put_multi([andy, sally, bobby])
            >>> query = client.query(kind='Andy')
            >>> aggregation_query = client.aggregation_query(query)
            >>> result = aggregation_query.count(alias="total").fetch(limit=5)
            >>> result
            <google.cloud.datastore.aggregation.AggregationResultIterator object at ...>

        .. testcleanup:: aggregation-query-fetch

            client.delete(andy.key)

        :type client: :class:`google.cloud.datastore.client.Client`
        :param client: (Optional) client used to connect to datastore.
                       If not supplied, uses the query's value.

        :type eventual: bool
        :param eventual: (Optional) Defaults to strongly consistent (False).
                                    Setting True will use eventual consistency,
                                    but cannot be used inside a transaction or
                                    with read_time, otherwise will raise
                                    ValueError.

        :type retry: :class:`google.api_core.retry.Retry`
        :param retry:
            A retry object used to retry requests. If ``None`` is specified,
            requests will be retried using a default configuration.

        :type timeout: float
        :param timeout:
            Time, in seconds, to wait for the request to complete.
            Note that if ``retry`` is specified, the timeout applies
            to each individual attempt.

        :type read_time: datetime
        :param read_time:
            (Optional) use read_time read consistency, cannot be used inside a
            transaction or with eventual consistency, or will raise ValueError.

        :rtype: :class:`AggregationIterator`
        :returns: The iterator for the aggregation query.
        """
        if client is None:
            client = self._client

        return AggregationResultIterator(
            self,
            client,
            limit=limit,
            eventual=eventual,
            retry=retry,
            timeout=timeout,
            read_time=read_time,
        )


class AggregationResultIterator(page_iterator.Iterator):
    """Represent the state of a given execution of a Query.

    :type aggregation_query: :class:`~google.cloud.datastore.aggregation.AggregationQuery`
    :param aggregation_query: AggregationQuery object holding permanent configuration (i.e.
                  things that don't change on with each page in
                  a results set).

    :type client: :class:`~google.cloud.datastore.client.Client`
    :param client: The client used to make a request.

    :type eventual: bool
    :param eventual: (Optional) Defaults to strongly consistent (False).
                                Setting True will use eventual consistency,
                                but cannot be used inside a transaction or
                                with read_time, otherwise will raise ValueError.

    :type retry: :class:`google.api_core.retry.Retry`
    :param retry:
        A retry object used to retry requests. If ``None`` is specified,
        requests will be retried using a default configuration.

    :type timeout: float
    :param timeout:
        Time, in seconds, to wait for the request to complete.
        Note that if ``retry`` is specified, the timeout applies
        to each individual attempt.

    :type read_time: datetime
    :param read_time: (Optional) Runs the query with read time consistency.
                      Cannot be used with eventual consistency or inside a
                      transaction, otherwise will raise ValueError. This feature is in private preview.
    """

    def __init__(
        self,
        aggregation_query,
        client,
        limit=None,
        eventual=False,
        retry=None,
        timeout=None,
        read_time=None,
    ):
        super(AggregationResultIterator, self).__init__(
            client=client,
            item_to_value=_item_to_aggregation_result,
        )

        self._aggregation_query = aggregation_query
        self._eventual = eventual
        self._retry = retry
        self._timeout = timeout
        self._read_time = read_time
        self._limit = limit
        # The attributes below will change over the life of the iterator.
        self._more_results = True

    def _build_protobuf(self):
        """Build a query protobuf.

        Relies on the current state of the iterator.

        :rtype:
            :class:`.query_pb2.AggregationQuery.Aggregation`
        :returns: The aggregation_query protobuf object for the current
                  state of the iterator.
        """
        pb = self._aggregation_query._to_pb()
        if self._limit is not None and self._limit > 0:
            for aggregation in pb.aggregations:
                aggregation.count.up_to = self._limit
        return pb

    def _process_query_results(self, response_pb):
        """Process the response from a datastore query.

        :type response_pb: :class:`.datastore_pb2.RunQueryResponse`
        :param response_pb: The protobuf response from a ``runQuery`` request.

        :rtype: iterable
        :returns: The next page of entity results.
        :raises ValueError: If ``more_results`` is an unexpected value.
        """

        if response_pb.batch.more_results == _NOT_FINISHED:
            self._more_results = True
        elif response_pb.batch.more_results in _FINISHED:
            self._more_results = False
        else:
            raise ValueError("Unexpected value returned for `more_results`.")

        return [
            result.aggregate_properties
            for result in response_pb.batch.aggregation_results
        ]

    def _next_page(self):
        """Get the next page in the iterator.

        :rtype: :class:`~google.cloud.iterator.Page`
        :returns: The next page in the iterator (or :data:`None` if
                  there are no pages left).
        """
        if not self._more_results:
            return None

        query_pb = self._build_protobuf()
        transaction = self.client.current_transaction
        if transaction is None:
            transaction_id = None
        else:
            transaction_id = transaction.id
        read_options = helpers.get_read_options(
            self._eventual, transaction_id, self._read_time
        )

        partition_id = entity_pb2.PartitionId(
            project_id=self._aggregation_query.project,
            namespace_id=self._aggregation_query.namespace,
        )

        kwargs = {}

        if self._retry is not None:
            kwargs["retry"] = self._retry

        if self._timeout is not None:
            kwargs["timeout"] = self._timeout

        response_pb = self.client._datastore_api.run_aggregation_query(
            request={
                "project_id": self._aggregation_query.project,
                "partition_id": partition_id,
                "read_options": read_options,
                "aggregation_query": query_pb,
            },
            **kwargs,
        )

        while response_pb.batch.more_results == _NOT_FINISHED:
            # We haven't finished processing. A likely reason is we haven't
            # skipped all of the results yet. Don't return any results.
            # Instead, rerun query, adjusting offsets. Datastore doesn't process
            # more than 1000 skipped results in a query.
            old_query_pb = query_pb
            query_pb = query_pb2.AggregationQuery()
            query_pb._pb.CopyFrom(old_query_pb._pb)  # copy for testability

            response_pb = self.client._datastore_api.run_aggregation_query(
                request={
                    "project_id": self._aggregation_query.project,
                    "partition_id": partition_id,
                    "read_options": read_options,
                    "aggregation_query": query_pb,
                },
                **kwargs,
            )

        item_pbs = self._process_query_results(response_pb)
        return page_iterator.Page(self, item_pbs, self.item_to_value)


# pylint: disable=unused-argument
def _item_to_aggregation_result(iterator, pb):
    """Convert a raw protobuf aggregation result to the native object.

    :type iterator: :class:`~google.api_core.page_iterator.Iterator`
    :param iterator: The iterator that is currently in use.

    :type pb:
        :class:`proto.marshal.collections.maps.MapComposite`
    :param pb: The aggregation properties pb from the aggregation query result

    :rtype: :class:`google.cloud.datastore.aggregation.AggregationResult`
    :returns: The list of AggregationResults
    """
    results = [AggregationResult(alias=k, value=pb[k].integer_value) for k in pb.keys()]
    return results
