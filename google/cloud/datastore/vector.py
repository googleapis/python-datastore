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

from typing import Sequence
from dataclasses import dataclass
from enum import Enum

_VECTOR_VALUE = 31


class DistanceMeasure(Enum):
    EUCLIDEAN = 1
    COSINE = 2
    DOT_PRODUCT = 3


class Vector(collections.abc.Sequence):
    """A class to represent a Vector for use in query.find_nearest.
    Underlying object will be converted to a map representation in Firestore API.
    """

    def __init__(self, value: Sequence[float]):
        self._value = tuple([float(v) for v in value])

    def __getitem__(self, arg: int | slice):
        if isinstance(arg, int):
            return self._value[arg]
        elif isinstance(arg, slice):
            return Vector(self._value[arg])
        else:
            raise NotImplementedError

    def __len__(self):
        return len(self._value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            raise NotImplementedError
        return self._value == other._value

    def __repr__(self):
        return f"Vector<{str(self._value)[1:-1]}>"

    def _to_dict(self):
        return {
            "array_value": {"values": [{"double_value": v} for v in self._value]},
            "meaning": _VECTOR_VALUE,
            "exclude_from_indexes": True,
        }


@dataclass
class FindNearest:
    """
    Represents configuration for a find_nearest vector query.

    :type vector_field: str
    :param vector_field:
        An indexed vector property to search upon.
        Only documents which contain vectors whose dimensionality match
        the query_vector can be returned.

    :type query_vector: Union[Vector, Sequence[float]]
    :param query_vector:
        The query vector that we are searching on.
        Must be a vector of no more than 2048 dimensions.

    :type limit: int
    :param limit:
        The number of nearest neighbors to return.
        Must be a positive integer of no more than 100.

    :type distance_measure: DistanceMeasure
    :param distance_measure:
        The distance measure to use when comparing vectors.

    :type distance_result_property: Optional[str]
    :param distance_result_property:
        Optional name of the field to output the result of the vector distance
        calculation.

    :type distance_threshold: Optional[float]
    :param distance_threshold:
        Threshold value for which no less similar documents will be returned.
        The behavior of the specified ``distance_measure`` will affect the
        meaning of the distance threshold:
            For EUCLIDEAN, COSINE: WHERE distance <= distance_threshold
            For DOT_PRODUCT: WHERE distance >= distance_threshold

        Optional threshold to apply to the distance measure.
        If set, only documents whose distance measure is less than this value
        will be returned.
    """

    vector_property: str
    query_vector: Vector | Sequence[float]
    limit: int
    distance_measure: DistanceMeasure
    distance_result_property: str | None = None
    distance_threshold: float | None = None

    def __post_init__(self):
        if not isinstance(self.query_vector, Vector):
            self.query_vector = Vector(self.query_vector)

    def _to_dict(self):
        output = {
            "vector_property": {"name": self.vector_property},
            "query_vector": self.query_vector._to_dict(),
            "distance_measure": self.distance_measure.value,
            "limit": self.limit,
        }
        if self.distance_result_property is not None:
            output["distance_result_property"] = self.distance_result_property
        if self.distance_threshold is not None:
            output["distance_threshold"] = float(self.distance_threshold)
        return output
