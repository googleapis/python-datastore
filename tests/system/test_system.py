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
import unittest

import requests

from google.cloud import datastore
from google.cloud.datastore.client import DATASTORE_DATASET
from google.cloud.exceptions import Conflict

from test_utils.system import unique_resource_id

from tests.system.utils import clear_datastore
from tests.system.utils import populate_datastore


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


class TestDatastore(unittest.TestCase):
    def setUp(self):
        self.case_entities_to_delete = []

    def tearDown(self):
        with Config.CLIENT.transaction():
            Config.CLIENT.delete_multi(self.case_entities_to_delete)


class TestDatastoreQuery(TestDatastore):
    @classmethod
    def setUpClass(cls):
        cls.CLIENT = clone_client(Config.CLIENT)
        # Remove the namespace from the cloned client, since these
        # query tests rely on the entities to be already stored and indexed,
        # hence ``test_namespace`` set at runtime can't be used.
        cls.CLIENT.namespace = None

        # In the emulator, re-populating the datastore is cheap.
        if os.getenv(DATASTORE_DATASET) is not None:
            # Populate the datastore with the cloned client.
            populate_datastore.add_characters(client=cls.CLIENT)

        cls.CHARACTERS = populate_datastore.CHARACTERS
        # Use the client for this test instead of the global.
        cls.ANCESTOR_KEY = cls.CLIENT.key(*populate_datastore.ANCESTOR)

    @classmethod
    def tearDownClass(cls):
        # In the emulator, destroy the query entities.
        if os.getenv(DATASTORE_DATASET) is not None:
            # Use the client for this test instead of the global.
            clear_datastore.remove_all_entities(client=cls.CLIENT)

    def _base_query(self):
        # Use the client for this test instead of the global.
        return self.CLIENT.query(kind="Character", ancestor=self.ANCESTOR_KEY)


class TestDatastoreQueryOffsets(TestDatastore):
    TOTAL_OBJECTS = 2500
    NAMESPACE = "LargeCharacterEntity"
    KIND = "LargeCharacter"

    @classmethod
    def setUpClass(cls):
        cls.CLIENT = clone_client(Config.CLIENT)
        # Remove the namespace from the cloned client, since these
        # query tests rely on the entities to be already stored
        # cls.CLIENT.namespace = cls.NAMESPACE
        cls.CLIENT.namespace = None

        # Populating the datastore if necessary.
        populate_datastore.add_large_character_entities(client=cls.CLIENT)

    @classmethod
    def tearDownClass(cls):
        # In the emulator, destroy the query entities.
        if os.getenv(DATASTORE_DATASET) is not None:
            # Use the client for this test instead of the global.
            clear_datastore.remove_all_entities(client=cls.CLIENT)

    def _base_query(self):
        # Use the client for this test instead of the global.
        return self.CLIENT.query(kind=self.KIND, namespace=self.NAMESPACE)

    def _verify(self, limit, offset, expected):
        # Query used for all tests
        page_query = self._base_query()
        page_query.add_filter("family", "=", "Stark")
        page_query.add_filter("alive", "=", False)

        iterator = page_query.fetch(limit=limit, offset=offset)
        entities = [e for e in iterator]
        self.assertEqual(len(entities), expected)

    def test_query_in_bounds_offsets(self):
        # Verify that with no offset there are the correct # of results
        self._verify(limit=None, offset=None, expected=self.TOTAL_OBJECTS)

        # Verify that with no limit there are results (offset provided)")
        self._verify(limit=None, offset=900, expected=self.TOTAL_OBJECTS - 900)

        # Offset beyond items larger Verify 200 items found")
        self._verify(limit=200, offset=1100, expected=200)

    def test_query_partially_out_of_bounds_offsets(self):
        # Offset within range, expect 50 despite larger limit")
        self._verify(limit=100, offset=self.TOTAL_OBJECTS - 50, expected=50)

    def test_query_out_of_bounds_offsets(self):
        # Offset beyond items larger Verify no items found")
        self._verify(limit=200, offset=self.TOTAL_OBJECTS + 1000, expected=0)


class TestDatastoreTransaction(TestDatastore):
    def test_transaction_via_with_statement(self):
        entity = datastore.Entity(key=Config.CLIENT.key("Company", "Google"))
        entity["url"] = u"www.google.com"

        with Config.CLIENT.transaction() as xact:
            result = Config.CLIENT.get(entity.key)
            if result is None:
                xact.put(entity)
                self.case_entities_to_delete.append(entity)

        # This will always return after the transaction.
        retrieved_entity = Config.CLIENT.get(entity.key)
        self.case_entities_to_delete.append(retrieved_entity)
        self.assertEqual(retrieved_entity, entity)

    def test_transaction_via_explicit_begin_get_commit(self):
        # See
        # github.com/GoogleCloudPlatform/google-cloud-python/issues/1859
        # Note that this example lacks the threading which provokes the race
        # condition in that issue:  we are basically just exercising the
        # "explict" path for using transactions.
        BEFORE_1 = 100
        BEFORE_2 = 0
        TRANSFER_AMOUNT = 40
        key1 = Config.CLIENT.key("account", "123")
        account1 = datastore.Entity(key=key1)
        account1["balance"] = BEFORE_1
        key2 = Config.CLIENT.key("account", "234")
        account2 = datastore.Entity(key=key2)
        account2["balance"] = BEFORE_2
        Config.CLIENT.put_multi([account1, account2])
        self.case_entities_to_delete.append(account1)
        self.case_entities_to_delete.append(account2)

        xact = Config.CLIENT.transaction()
        xact.begin()
        from_account = Config.CLIENT.get(key1, transaction=xact)
        to_account = Config.CLIENT.get(key2, transaction=xact)
        from_account["balance"] -= TRANSFER_AMOUNT
        to_account["balance"] += TRANSFER_AMOUNT

        xact.put(from_account)
        xact.put(to_account)
        xact.commit()

        after1 = Config.CLIENT.get(key1)
        after2 = Config.CLIENT.get(key2)
        self.assertEqual(after1["balance"], BEFORE_1 - TRANSFER_AMOUNT)
        self.assertEqual(after2["balance"], BEFORE_2 + TRANSFER_AMOUNT)

    def test_failure_with_contention(self):
        contention_prop_name = "baz"
        local_client = clone_client(Config.CLIENT)

        # Insert an entity which will be retrieved in a transaction
        # and updated outside it with a contentious value.
        key = local_client.key("BreakTxn", 1234)
        orig_entity = datastore.Entity(key=key)
        orig_entity["foo"] = u"bar"
        local_client.put(orig_entity)
        self.case_entities_to_delete.append(orig_entity)

        with self.assertRaises(Conflict):
            with local_client.transaction() as txn:
                entity_in_txn = local_client.get(key)

                # Update the original entity outside the transaction.
                orig_entity[contention_prop_name] = u"outside"
                Config.CLIENT.put(orig_entity)

                # Try to update the entity which we already updated outside the
                # transaction.
                entity_in_txn[contention_prop_name] = u"inside"
                txn.put(entity_in_txn)

    def test_empty_array_put(self):
        local_client = clone_client(Config.CLIENT)

        key = local_client.key("EmptyArray", 1234)
        local_client = datastore.Client()
        entity = datastore.Entity(key=key)
        entity["children"] = []
        local_client.put(entity)
        retrieved = local_client.get(entity.key)

        self.assertEqual(entity["children"], retrieved["children"])
