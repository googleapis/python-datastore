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

from .services.datastore_admin import DatastoreAdminClient
from .types.datastore_admin import CommonMetadata
from .types.datastore_admin import EntityFilter
from .types.datastore_admin import ExportEntitiesMetadata
from .types.datastore_admin import ExportEntitiesRequest
from .types.datastore_admin import ExportEntitiesResponse
from .types.datastore_admin import GetIndexRequest
from .types.datastore_admin import ImportEntitiesMetadata
from .types.datastore_admin import ImportEntitiesRequest
from .types.datastore_admin import IndexOperationMetadata
from .types.datastore_admin import ListIndexesRequest
from .types.datastore_admin import ListIndexesResponse
from .types.datastore_admin import OperationType
from .types.datastore_admin import Progress
from .types.index import Index


__all__ = (
    "CommonMetadata",
    "EntityFilter",
    "ExportEntitiesMetadata",
    "ExportEntitiesRequest",
    "ExportEntitiesResponse",
    "GetIndexRequest",
    "ImportEntitiesMetadata",
    "ImportEntitiesRequest",
    "Index",
    "IndexOperationMetadata",
    "ListIndexesRequest",
    "ListIndexesResponse",
    "OperationType",
    "Progress",
    "DatastoreAdminClient",
)
