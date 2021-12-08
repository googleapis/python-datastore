# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
#

from google.cloud.datastore_v1.services.datastore.client import DatastoreClient
from google.cloud.datastore_v1.services.datastore.async_client import DatastoreAsyncClient

from google.cloud.datastore_v1.types.datastore import AllocateIdsRequest
from google.cloud.datastore_v1.types.datastore import AllocateIdsResponse
from google.cloud.datastore_v1.types.datastore import BeginTransactionRequest
from google.cloud.datastore_v1.types.datastore import BeginTransactionResponse
from google.cloud.datastore_v1.types.datastore import CommitRequest
from google.cloud.datastore_v1.types.datastore import CommitResponse
from google.cloud.datastore_v1.types.datastore import LookupRequest
from google.cloud.datastore_v1.types.datastore import LookupResponse
from google.cloud.datastore_v1.types.datastore import Mutation
from google.cloud.datastore_v1.types.datastore import MutationResult
from google.cloud.datastore_v1.types.datastore import ReadOptions
from google.cloud.datastore_v1.types.datastore import ReserveIdsRequest
from google.cloud.datastore_v1.types.datastore import ReserveIdsResponse
from google.cloud.datastore_v1.types.datastore import RollbackRequest
from google.cloud.datastore_v1.types.datastore import RollbackResponse
from google.cloud.datastore_v1.types.datastore import RunQueryRequest
from google.cloud.datastore_v1.types.datastore import RunQueryResponse
from google.cloud.datastore_v1.types.datastore import TransactionOptions
from google.cloud.datastore_v1.types.entity import ArrayValue
from google.cloud.datastore_v1.types.entity import Entity
from google.cloud.datastore_v1.types.entity import Key
from google.cloud.datastore_v1.types.entity import PartitionId
from google.cloud.datastore_v1.types.entity import Value
from google.cloud.datastore_v1.types.query import CompositeFilter
from google.cloud.datastore_v1.types.query import EntityResult
from google.cloud.datastore_v1.types.query import Filter
from google.cloud.datastore_v1.types.query import GqlQuery
from google.cloud.datastore_v1.types.query import GqlQueryParameter
from google.cloud.datastore_v1.types.query import KindExpression
from google.cloud.datastore_v1.types.query import Projection
from google.cloud.datastore_v1.types.query import PropertyFilter
from google.cloud.datastore_v1.types.query import PropertyOrder
from google.cloud.datastore_v1.types.query import PropertyReference
from google.cloud.datastore_v1.types.query import Query
from google.cloud.datastore_v1.types.query import QueryResultBatch

__all__ = ('DatastoreClient',
    'DatastoreAsyncClient',
    'AllocateIdsRequest',
    'AllocateIdsResponse',
    'BeginTransactionRequest',
    'BeginTransactionResponse',
    'CommitRequest',
    'CommitResponse',
    'LookupRequest',
    'LookupResponse',
    'Mutation',
    'MutationResult',
    'ReadOptions',
    'ReserveIdsRequest',
    'ReserveIdsResponse',
    'RollbackRequest',
    'RollbackResponse',
    'RunQueryRequest',
    'RunQueryResponse',
    'TransactionOptions',
    'ArrayValue',
    'Entity',
    'Key',
    'PartitionId',
    'Value',
    'CompositeFilter',
    'EntityResult',
    'Filter',
    'GqlQuery',
    'GqlQueryParameter',
    'KindExpression',
    'Projection',
    'PropertyFilter',
    'PropertyOrder',
    'PropertyReference',
    'Query',
    'QueryResultBatch',
)
