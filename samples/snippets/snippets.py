# Copyright 2022 Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from datetime import datetime, timedelta, timezone
from pprint import pprint

from google.cloud import datastore  # noqa: I100


def _preamble():
    # [START datastore_size_coloration_query]
    from google.cloud import datastore

    # For help authenticating your client, visit
    # https://cloud.google.com/docs/authentication/getting-started
    client = datastore.Client()

    # [END datastore_size_coloration_query]
    assert client is not None


def in_query(client):
    # [START datastore_in_query]
    query = client.query(kind="Task")
    query.add_filter("tag", "IN", ["learn", "study"])
    # [END datastore_in_query]

    return list(query.fetch())


def not_equals_query(client):
    # [START datastore_not_equals_query]
    query = client.query(kind="Task")
    query.add_filter("category", "!=", "work")
    # [END datastore_not_equals_query]

    return list(query.fetch())


def not_in_query(client):
    # [START datastore_not_in_query]
    query = client.query(kind="Task")
    query.add_filter("category", "NOT_IN", ["work", "chores", "school"])
    # [END datastore_not_in_query]

    return list(query.fetch())


def query_with_readtime(client):
    # [START datastore_snapshot_read]
    # Create a read time of 120 seconds in the past
    read_time = datetime.now(timezone.utc) - timedelta(seconds=120)

    # Fetch an entity at time read_time
    task_key = client.key('Task', 'sampletask')
    entity = client.get(task_key, read_time=read_time)

    # Query Task entities at time read_time
    query = client.query(kind="Task")
    tasks = query.fetch(read_time=read_time, limit=10)
    # [END datastore_snapshot_read]

    results = list(tasks)
    results.append(entity)

    return results


def main(project_id):
    client = datastore.Client(project_id)

    for name, function in globals().items():
        if name in ("main", "_preamble", "defaultdict", "datetime", "timezone", "timedelta") or not callable(function):
            continue

        print(name)
        pprint(function(client))
        print("\n-----------------\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Demonstrates datastore API operations."
    )
    parser.add_argument("project_id", help="Your cloud project ID.")

    args = parser.parse_args()

    main(args.project_id)
