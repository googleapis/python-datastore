# Copyright 2024 Google LLC
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
from __future__ import annotations

import collections

from typing import Tuple, Sequence
from dataclasses import dataclass
from enum import Enum
from google.cloud.datastore_v1.types import Value


class DistanceMeasure(Enum):
    EUCLIDEAN = 1
    COSINE = 2
    DOT_PRODUCT = 3


class Vector(collections.abc.Sequence):
    r"""A class to represent Firestore Vector in python.
    Underlying object will be converted to a map representation in Firestore API.
    """

    _value: Tuple[float] = ()

    def __init__(self, value: Sequence[float]):
        self._value = tuple([float(v) for v in value])

    def __getitem__(self, arg: int):
        return self._value[arg]

    def __len__(self):
        return len(self._value)

    def __eq__(self, other: object) -> bool:
        return self._value == other._value

    def __repr__(self):
        return f"Vector<{str(self._value)[1:-1]}>"

    def _to_dict(self):
        return {"array_value": {"values": [{"double_value": v} for v in self._value]}, "meaning": 31, "exclude_from_indexes": True}


@dataclass
class FindNearest:
    vector_property: str
    query_vector: Vector | Sequence[float]
    limit: int
    distance_measure:DistanceMeasure = DistanceMeasure.EUCLIDEAN,
    distance_result_property: str | None = None
    distance_threshold: float | None = None

    def __post_init__(self):
        if not isinstance(self.query_vector, Vector):
            self.query_vector = Vector(self.query_vector)

    def __repr__(self):
        return f"FindNearest<vector_field={self.vector_field}, query_vector={self.query_vector}, limit={self.limit}, distance_measure={self.distance_measure}>"

    def _to_dict(self):
        output = {
            "vector_property": {"name":self.vector_property},
            "query_vector": self.query_vector._to_dict(),
            "distance_measure": self.distance_measure.value,
            "limit": self.limit,
        }
        if self.distance_result_property is not None:
            output["distance_result_property"] = self.distance_result_property
        if self.distance_threshold is not None:
            output["distance_threshold"] = float(self.distance_threshold)
        return output
