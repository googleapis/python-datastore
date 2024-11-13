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

import pytest

from google.cloud.datastore.vector import Vector, FindNearest, DistanceMeasure


class TestVector:
    """
    tests for google.cloud.datastore.vector.Vector
    """

    def test_vector_ctor(self):
        v = Vector([1.0, 2.0, 3.0])
        assert len(v) == 3
        assert v[0] == 1.0
        assert v[1] == 2.0
        assert v[2] == 3.0
        assert v.exclude_from_indexes == False

    def test_vector_ctor_w_ints(self):
        v = Vector([1, 2, 3])
        assert len(v) == 3
        assert v[0] == 1.0
        assert v[1] == 2.0
        assert v[2] == 3.0

    @pytest.mark.parametrize("exclude", [True, False])
    def test_vector_ctor_w_exclude_from_indexes(self, exclude):
        v = Vector([1], exclude_from_indexes=exclude)
        assert v.exclude_from_indexes == exclude

    def test_vector_empty_ctor(self):
        v = Vector([])
        assert len(v) == 0
        assert v._value == ()

    def test_vector_equality(self):
        v1 = Vector([1.0, 2.0, 3.0])
        v2 = Vector([1.0, 2.0, 3.0])
        v3 = Vector([3.0, 2.0, 1.0])
        assert v1 == v2
        assert v1 != v3

    def test_vector_representation(self):
        v = Vector([1, 9.4, 3.1234])
        assert repr(v) == "Vector<1.0, 9.4, 3.1234>"

    @pytest.mark.parametrize("exclude", [True, False])
    def test_vector_to_dict(self, exclude):
        v = Vector([1.0, 2.0, 3.0], exclude_from_indexes=exclude)
        expected = {
            "array_value": {
                "values": [
                    {"double_value": 1.0},
                    {"double_value": 2.0},
                    {"double_value": 3.0},
                ]
            },
            "meaning": 31,
            "exclude_from_indexes": exclude,
        }
        assert v._to_dict() == expected

    def test_vector_iteration(self):
        v = Vector(range(10))
        assert v[0] == 0.0
        assert v[3] == 3.0
        assert v[-1] == 9.0
        for i, val in enumerate(v):
            assert i == val

    @pytest.mark.parametrize("exclude", [True, False])
    def test_vector_slicing(self, exclude):
        v = Vector(range(10), exclude_from_indexes=exclude)
        assert v[1:3] == Vector([1.0, 2.0])
        assert v[:] == Vector([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
        assert v[::-1] == Vector([9.0, 8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0])
        assert v[3:7].exclude_from_indexes == exclude

    @pytest.mark.parametrize("exclude", [True, False])
    def test_vector_to_proto(self, exclude):
        from google.cloud.datastore_v1.types import Value

        v = Vector([1.0, 2.0, 3.0], exclude_from_indexes=exclude)
        proto = Value(**v._to_dict())
        assert proto.array_value.values[0].double_value == 1.0
        assert proto.array_value.values[1].double_value == 2.0
        assert proto.array_value.values[2].double_value == 3.0
        assert proto.meaning == 31
        assert proto.exclude_from_indexes == exclude

    def test_empty_vector_to_proto(self):
        from google.cloud.datastore_v1.types import Value

        v = Vector([])
        proto = Value(**v._to_dict())
        assert proto.array_value.values == []
        assert proto.meaning == 31


class TestFindNearest:
    """
    tests for google.cloud.datastore.vector.FindNearest
    """

    def test_ctor_defaults(self):
        expected_property = "embeddings"
        expected_vector = [1.0, 2.0, 3.0]
        expected_limit = 5
        expected_distance_measure = DistanceMeasure.DOT_PRODUCT
        fn = FindNearest(
            expected_property,
            expected_vector,
            expected_limit,
            expected_distance_measure,
        )
        assert fn.vector_property == expected_property
        assert fn.query_vector == Vector(expected_vector)
        assert fn.limit == expected_limit
        assert fn.distance_measure == expected_distance_measure
        assert fn.distance_result_property is None
        assert fn.distance_threshold is None

    def test_ctor_explicit(self):
        expected_property = "embeddings"
        expected_vector = Vector([1.0, 2.0, 3.0])
        expected_limit = 10
        expected_distance_measure = DistanceMeasure.EUCLIDEAN
        expected_distance_result_property = "distance"
        expected_distance_threshold = 0.5
        fn = FindNearest(
            expected_property,
            expected_vector,
            expected_limit,
            expected_distance_measure,
            expected_distance_result_property,
            expected_distance_threshold,
        )
        assert fn.vector_property == expected_property
        assert fn.query_vector == expected_vector
        assert fn.limit == expected_limit
        assert fn.distance_measure == expected_distance_measure
        assert fn.distance_result_property == expected_distance_result_property
        assert fn.distance_threshold == expected_distance_threshold

    def test_find_nearest_to_dict(self):
        fn = FindNearest(
            vector_property="embeddings",
            query_vector=[1.0, 2.0, 3.0],
            limit=10,
            distance_measure=DistanceMeasure.EUCLIDEAN,
            distance_result_property="distance",
            distance_threshold=0.5,
        )
        expected = {
            "vector_property": {"name": "embeddings"},
            "query_vector": {
                "array_value": {
                    "values": [
                        {"double_value": 1.0},
                        {"double_value": 2.0},
                        {"double_value": 3.0},
                    ]
                },
                "meaning": 31,
                "exclude_from_indexes": False,
            },
            "distance_measure": 1,
            "limit": 10,
            "distance_result_property": "distance",
            "distance_threshold": 0.5,
        }
        assert fn._to_dict() == expected

    def test_limited_find_nearest_to_dict(self):
        fn = FindNearest(
            vector_property="embeddings",
            query_vector=[3, 2, 1],
            limit=99,
            distance_measure=DistanceMeasure.DOT_PRODUCT,
        )
        expected = {
            "vector_property": {"name": "embeddings"},
            "query_vector": {
                "array_value": {
                    "values": [
                        {"double_value": 3.0},
                        {"double_value": 2.0},
                        {"double_value": 1.0},
                    ]
                },
                "meaning": 31,
                "exclude_from_indexes": False,
            },
            "distance_measure": 3,
            "limit": 99,
        }
        assert fn._to_dict() == expected

    def test_find_nearest_representation(self):
        fn = FindNearest(
            vector_property="embeddings",
            query_vector=[1.0, 2.0, 3.0],
            limit=10,
            distance_measure=DistanceMeasure.EUCLIDEAN,
        )
        expected = "FindNearest(vector_property='embeddings', query_vector=Vector<1.0, 2.0, 3.0>, limit=10, distance_measure=<DistanceMeasure.EUCLIDEAN: 1>, distance_result_property=None, distance_threshold=None)"
        assert repr(fn) == expected
