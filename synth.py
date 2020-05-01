# Copyright 2018 Google LLC
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

"""This script is used to synthesize generated parts of this library."""
import synthtool as s
from synthtool import gcp

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate datastore GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="datastore",
    version="v1",
    bazel_target="//google/datastore/v1:datastore-v1-py",
    include_protos=True,
)

s.move(library / "google/cloud/datastore_v1/proto")
s.move(library / "google/cloud/datastore_v1/gapic")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(unit_cov_level=97, cov_level=99)
s.move(templated_files, excludes=["docs/conf.py"])

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
