# -*- coding: utf-8 -*-
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
#
from typing import MutableMapping, MutableSequence

import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.datastore.admin.v1",
    manifest={
        "Index",
    },
)


class Index(proto.Message):
    r"""Datastore composite index definition.

    Attributes:
        project_id (str):
            Output only. Project ID.
        index_id (str):
            Output only. The resource ID of the index.
        kind (str):
            Required. The entity kind to which this index
            applies.
        ancestor (google.cloud.datastore_admin_v1.types.Index.AncestorMode):
            Required. The index's ancestor mode. Must not be
            ANCESTOR_MODE_UNSPECIFIED.
        properties (MutableSequence[google.cloud.datastore_admin_v1.types.Index.IndexedProperty]):
            Required. An ordered sequence of property
            names and their index attributes.
        state (google.cloud.datastore_admin_v1.types.Index.State):
            Output only. The state of the index.
    """

    class AncestorMode(proto.Enum):
        r"""For an ordered index, specifies whether each of the entity's
        ancestors will be included.
        """
        ANCESTOR_MODE_UNSPECIFIED = 0
        NONE = 1
        ALL_ANCESTORS = 2

    class Direction(proto.Enum):
        r"""The direction determines how a property is indexed."""
        DIRECTION_UNSPECIFIED = 0
        ASCENDING = 1
        DESCENDING = 2

    class State(proto.Enum):
        r"""The possible set of states of an index."""
        STATE_UNSPECIFIED = 0
        CREATING = 1
        READY = 2
        DELETING = 3
        ERROR = 4

    class IndexedProperty(proto.Message):
        r"""A property of an index.

        Attributes:
            name (str):
                Required. The property name to index.
            direction (google.cloud.datastore_admin_v1.types.Index.Direction):
                Required. The indexed property's direction. Must not be
                DIRECTION_UNSPECIFIED.
        """

        name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        direction: "Index.Direction" = proto.Field(
            proto.ENUM,
            number=2,
            enum="Index.Direction",
        )

    project_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    index_id: str = proto.Field(
        proto.STRING,
        number=3,
    )
    kind: str = proto.Field(
        proto.STRING,
        number=4,
    )
    ancestor: AncestorMode = proto.Field(
        proto.ENUM,
        number=5,
        enum=AncestorMode,
    )
    properties: MutableSequence[IndexedProperty] = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message=IndexedProperty,
    )
    state: State = proto.Field(
        proto.ENUM,
        number=7,
        enum=State,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
