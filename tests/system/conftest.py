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

import os

import pytest
import requests

from google.cloud import datastore
from google.cloud.datastore.client import DATASTORE_DATASET
from . import _helpers


@pytest.fixture(scope="session")
def in_emulator():
    return DATASTORE_DATASET in os.environment


@pytest.fixture(scope="session")
def emulator_dataset():
    return os.getenv(DATASTORE_DATASET)


@pytest.fixture(scope="session")
def test_namespace():
    return _helpers.unique_id("ns")


@pytest.fixture(scope="session")
def datastore_client(test_namespace, emulator_dataset):
    if emulator_dataset is not None:
        http = requests.Session()  # Un-authorized.
        return datastore.Client(
            project=emulator_dataset, namespace=test_namespace, _http=http,
        )
    else:
        return datastore.Client(namespace=test_namespace)


@pytest.fixture(scope="function")
def entities_to_delete(datastore_client):
    entities_to_delete = []

    yield entities_to_delete

    datastore_client.delete_multi(entities_to_delete)
