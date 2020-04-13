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

"""Script to populate datastore with system test data."""


from __future__ import print_function

import os
import string
import sys
import time
import uuid

import six

from google.cloud import datastore


ANCESTOR = ("Book", "GoT")
RICKARD = ANCESTOR + ("Character", "Rickard")
EDDARD = RICKARD + ("Character", "Eddard")
KEY_PATHS = (
    RICKARD,
    EDDARD,
    ANCESTOR + ("Character", "Catelyn"),
    EDDARD + ("Character", "Arya"),
    EDDARD + ("Character", "Sansa"),
    EDDARD + ("Character", "Robb"),
    EDDARD + ("Character", "Bran"),
    EDDARD + ("Character", "Jon Snow"),
)
CHARACTERS = (
    {"name": u"Rickard", "family": u"Stark", "appearances": 0, "alive": False},
    {"name": u"Eddard", "family": u"Stark", "appearances": 9, "alive": False},
    {
        "name": u"Catelyn",
        "family": [u"Stark", u"Tully"],
        "appearances": 26,
        "alive": False,
    },
    {"name": u"Arya", "family": u"Stark", "appearances": 33, "alive": True},
    {"name": u"Sansa", "family": u"Stark", "appearances": 31, "alive": True},
    {"name": u"Robb", "family": u"Stark", "appearances": 22, "alive": False},
    {"name": u"Bran", "family": u"Stark", "appearances": 25, "alive": True},
    {"name": u"Jon Snow", "family": u"Stark", "appearances": 32, "alive": True},
)


def print_func(message):
    if os.getenv("GOOGLE_CLOUD_NO_PRINT") != "true":
        print(message)


def _estimate_entity_size(entity):
    def _estimate_value_size(value):
        if isinstance(value, six.integer_types):
            return 9  # Max varint size
        elif isinstance(value, float):
            return 8
        elif isinstance(value, six.string_types) or isinstance(value, six.binary_type):
            return len(value)
        elif isinstance(value, (list, tuple)):
            return sum(_estimate_entity_size(elem) for elem in value)
        elif isinstance(value, dict):
            return _estimate_entity_size(value)
    result = 0
    for key, value in entity.items():
        result += len(key)  # The number of runes is fine, no point forcing a utf-8 encoding here.
        result += _estimate_value_size(value)
    return result

def add_large_character_entities(client=None):
    TOTAL_OBJECTS = 2500
    NAMESPACE = "LargeCharacterEntity"
    KIND = "LargeCharacter"
    MAX_STRING = (string.ascii_lowercase * 58)[:1500]

    BATCH_SIZE = 500  # Datastore API only allows 500 mutations in a single call.
    RPC_BYTES_LIMIT = 3 << 20 # grpc limit is ~4MiB, so use a 3MiB limit (to work around any encoding issues)

    client.namespace = NAMESPACE

    # Query used for all tests
    page_query = client.query(kind=KIND, namespace=NAMESPACE)
    page_query.keys_only()

    def put_objects(count):
        remaining = count
        entities = []
        # The name/ID for the new entity
        for i in range(count):
            name = "character{0:05d}".format(i)
            # The Cloud Datastore key for the new entity
            task_key = client.key(KIND, name)

            # Prepares the new entity
            task = datastore.Entity(key=task_key)
            task["name"] = "{0:05d}".format(i)
            task["family"] = "Stark"
            task["alive"] = False
            for i in string.ascii_lowercase:
                task["space-{}".format(i)] = MAX_STRING
            entities.append(task)

        # Now lets try to insert all of the entities, in batches.
        while entities:
            approx_rpc_bytes = 0
            batch = []
            while entities and len(batch) < BATCH_SIZE and approx_rpc_bytes < RPC_BYTES_LIMIT:
                batch.append(entities.pop())
                approx_rpc_bytes += _estimate_entity_size(batch[-1])
            # These entities are all in different entity groups, so there is no
            # benefit in placing them in a transaction.
            client.put_multi(batch)

    # Ensure we have 2500 entities for tests. If not, clean up type and add
    # new entities equal to TOTAL_OBJECTS
    all_keys = [e.key for e in page_query.fetch()]
    if len(all_keys) != TOTAL_OBJECTS:
        # Remove all of the entites that exist of this kind in this namespace.
        while all_keys:
            key_bytes = 0
            batch = []
            # Grab keys to delete, while ensuring we stay within our bounds.
            while len(batch) < BATCH_SIZE and key_bytes < RPC_BYTES_LIMIT and all_keys:
                batch.append(all_keys.pop())
                if batch[-1].name is None:
                    key_bytes += 9  # It takes 9 bytes for the largest varint encoded number
                else:
                    key_bytes += len(batch[-1].name)
            client.delete_multi(batch)
        # Put objects
        put_objects(TOTAL_OBJECTS)


def add_characters(client=None):
    if client is None:
        # Get a client that uses the test dataset.
        client = datastore.Client()
    with client.transaction() as xact:
        for key_path, character in six.moves.zip(KEY_PATHS, CHARACTERS):
            if key_path[-1] != character["name"]:
                raise ValueError(("Character and key don't agree", key_path, character))
            entity = datastore.Entity(key=client.key(*key_path))
            entity.update(character)
            xact.put(entity)
            print_func(
                "Adding Character %s %s" % (character["name"], character["family"])
            )


def add_uid_keys(client=None):
    if client is None:
        # Get a client that uses the test dataset.
        client = datastore.Client()

    num_batches = 2
    batch_size = 500

    for batch_num in range(num_batches):
        with client.batch() as batch:
            for seq_no in range(batch_size):
                uid = str(uuid.uuid4())
                key = client.key("uuid_key", uid)
                entity = datastore.Entity(key=key)
                entity["batch_num"] = batch_num
                entity["seq_no"] = seq_no
                batch.put(entity)


def add_timestamp_keys(client=None):
    if client is None:
        # Get a client that uses the test dataset.
        client = datastore.Client()

    num_batches = 21
    batch_size = 500
    assert num_batches * batch_size > 10000, 'test_query_offset_timestamp_keys requires at least 10k entries, otherwise it fails'

    timestamp_micros = set()
    for batch_num in range(num_batches):
        with client.batch() as batch:
            for seq_no in range(batch_size):
                print("time_time: batch: {}, sequence: {}".format(batch_num, seq_no))
                now_micros = int(time.time() * 1e6)
                while now_micros in timestamp_micros:
                    now_micros = int(time.time() * 1e6)
                timestamp_micros.add(now_micros)
                key = client.key("timestamp_key", now_micros)
                entity = datastore.Entity(key=key)
                entity["batch_num"] = batch_num
                entity["seq_no"] = seq_no
                batch.put(entity)


def main():
    client = datastore.Client()
    flags = sys.argv[1:]

    if len(flags) == 0:
        flags = ["--characters", "--uuid", "--timestamps"]

    if "--characters" in flags:
        add_characters(client)

    if "--uuid" in flags:
        add_uid_keys(client)

    if "--timestamps" in flags:
        add_timestamp_keys(client)


if __name__ == "__main__":
    main()
