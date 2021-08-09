# Copyright 2014 Google LLC
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

import requests

from google.cloud import datastore
from google.cloud.datastore.client import DATASTORE_DATASET

from test_utils.system import unique_resource_id


class Config(object):
    """Run-time configuration to be modified at set-up.

    This is a mutable stand-in to allow test set-up to modify
    global state.
    """

    CLIENT = None
    TO_DELETE = []


def clone_client(client):
    emulator_dataset = os.getenv(DATASTORE_DATASET)

    if emulator_dataset is None:
        return datastore.Client(
            project=client.project,
            namespace=client.namespace,
            credentials=client._credentials,
            _http=client._http,
        )
    else:
        return datastore.Client(
            project=client.project, namespace=client.namespace, _http=client._http,
        )


def setUpModule():
    emulator_dataset = os.getenv(DATASTORE_DATASET)
    # Isolated namespace so concurrent test runs don't collide.
    test_namespace = "ns" + unique_resource_id()
    if emulator_dataset is None:
        Config.CLIENT = datastore.Client(namespace=test_namespace)
    else:
        http = requests.Session()  # Un-authorized.
        Config.CLIENT = datastore.Client(
            project=emulator_dataset, namespace=test_namespace, _http=http,
        )


def tearDownModule():
    with Config.CLIENT.transaction():
        Config.CLIENT.delete_multi(Config.TO_DELETE)
