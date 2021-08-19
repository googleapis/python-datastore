# Copyright 2021 Google LLC
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
import requests

from google.cloud import datastore
from . import _helpers


@pytest.fixture(scope="session")
def in_emulator():
    return _helpers.EMULATOR_DATASET is not None


@pytest.fixture(scope="session")
def test_namespace():
    return _helpers.unique_id("ns")


@pytest.fixture(scope="session")
def datastore_client(test_namespace):
    if _helpers.EMULATOR_DATASET is not None:
        http = requests.Session()  # Un-authorized.
        return datastore.Client(
            project=_helpers.EMULATOR_DATASET, namespace=test_namespace, _http=http,
        )
    else:
        return datastore.Client(namespace=test_namespace)


@pytest.fixture(scope="function")
def entities_to_delete(datastore_client):
    entities_to_delete = []

    yield entities_to_delete

    with datastore_client.transaction():
        datastore_client.delete_multi(entities_to_delete)
