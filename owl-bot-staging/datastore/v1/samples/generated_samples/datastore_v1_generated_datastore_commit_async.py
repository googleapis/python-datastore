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
# Generated code. DO NOT EDIT!
#
# Snippet for Commit
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-datastore


# [START datastore_v1_generated_Datastore_Commit_async]
from google.cloud import datastore_v1


async def sample_commit():
    # Create a client
    client = datastore_v1.DatastoreAsyncClient()

    # Initialize request argument(s)
    request = datastore_v1.CommitRequest(
        transaction=b'transaction_blob',
        project_id="project_id_value",
    )

    # Make the request
    response = await client.commit(request=request)

    # Handle the response
    print(response)

# [END datastore_v1_generated_Datastore_Commit_async]