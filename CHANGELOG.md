# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-datastore/#history

### [1.13.2](https://www.github.com/googleapis/python-datastore/compare/v1.13.1...v1.13.2) (2020-07-17)


### Bug Fixes

* modify admin pkg name in gapic ([#47](https://www.github.com/googleapis/python-datastore/issues/47)) ([5b5011d](https://www.github.com/googleapis/python-datastore/commit/5b5011daf74133ecdd579bf19bbcf356e6f40dad))

### [1.13.1](https://www.github.com/googleapis/python-datastore/compare/v1.13.0...v1.13.1) (2020-07-13)


### Bug Fixes

* add missing datastore admin client files ([#43](https://www.github.com/googleapis/python-datastore/issues/43)) ([0d40f87](https://www.github.com/googleapis/python-datastore/commit/0d40f87eeacd2a256d4b45ccb742599b5df93096))

## [1.13.0](https://www.github.com/googleapis/python-datastore/compare/v1.12.0...v1.13.0) (2020-07-01)


### Features

* add datastore admin client ([#39](https://www.github.com/googleapis/python-datastore/issues/39)) ([1963fd8](https://www.github.com/googleapis/python-datastore/commit/1963fd84c012cc7985e44ed0fc03c15a6429833b))
* add synth config to generate datastore_admin_v1 ([#27](https://www.github.com/googleapis/python-datastore/issues/27)) ([83c636e](https://www.github.com/googleapis/python-datastore/commit/83c636efc6e5bd02bd8dc614e4114f9477c74972))
* Create CODEOWNERS ([#28](https://www.github.com/googleapis/python-datastore/issues/28)) ([0198419](https://www.github.com/googleapis/python-datastore/commit/0198419a759d4d3932fa92c268772f18aa29e2ca))

## [1.12.0](https://www.github.com/googleapis/python-datastore/compare/v1.11.0...v1.12.0) (2020-04-07)


### Features

* **datastore:** add missing method for system test with emulator ([#19](https://www.github.com/googleapis/python-datastore/issues/19)) ([bf8b897](https://www.github.com/googleapis/python-datastore/commit/bf8b897dc86e28e4ad79e05f24383c1387eddbf6))


### Bug Fixes

* Address queries not fully satisfying requested offset ([#18](https://www.github.com/googleapis/python-datastore/issues/18)) ([e7b5fc9](https://www.github.com/googleapis/python-datastore/commit/e7b5fc99e91078e94d1eaab64e1ea2158220ae98))

## [1.11.0](https://www.github.com/googleapis/python-datastore/compare/v1.10.0...v1.11.0) (2020-02-27)


### Features

* **datastore:** add return query object in add filter method ([#12](https://www.github.com/googleapis/python-datastore/issues/12)) ([6a9efab](https://www.github.com/googleapis/python-datastore/commit/6a9efabe1560d5137986df70f1b4f79731deac02))

## 1.10.0

10-10-2019 12:20 PDT


### Implementation Changes
- Remove send / receive message size limit (via synth). ([#8952](https://github.com/googleapis/google-cloud-python/pull/8952))

### New Features
- Add `client_options` to constructors for manual clients. ([#9055](https://github.com/googleapis/google-cloud-python/pull/9055))

### Dependencies
- Pin `google-cloud-core >= 1.0.3, < 2.0.0dev`. ([#9055](https://github.com/googleapis/google-cloud-python/pull/9055))

### Documentation
- Fix intersphinx reference to requests. ([#9294](https://github.com/googleapis/google-cloud-python/pull/9294))
- Remove CI for gh-pages, use googleapis.dev for `api_core` refs. ([#9085](https://github.com/googleapis/google-cloud-python/pull/9085))
- Remove compatability badges from READMEs. ([#9035](https://github.com/googleapis/google-cloud-python/pull/9035))
- Update docs for building datastore indexes. ([#8707](https://github.com/googleapis/google-cloud-python/pull/8707))
- Update intersphinx mapping for requests. ([#8805](https://github.com/googleapis/google-cloud-python/pull/8805))

## 1.9.0

07-24-2019 16:04 PDT


### Implementation Changes
- Allow kwargs to be passed to create_channel (via synth). ([#8388](https://github.com/googleapis/google-cloud-python/pull/8388))

### New Features
- Add 'client_options' support (via synth). ([#8506](https://github.com/googleapis/google-cloud-python/pull/8506))
- Add 'Client.reserve_ids' API wrapper. ([#8178](https://github.com/googleapis/google-cloud-python/pull/8178))

### Dependencies
- Bump minimum version for google-api-core to 1.14.0. ([#8709](https://github.com/googleapis/google-cloud-python/pull/8709))

### Documentation
- Link to googleapis.dev documentation in READMEs. ([#8705](https://github.com/googleapis/google-cloud-python/pull/8705))
- Add compatibility check badges to READMEs. ([#8288](https://github.com/googleapis/google-cloud-python/pull/8288))

### Internal / Testing Changes
- Pin black version (via synth). ([#8580](https://github.com/googleapis/google-cloud-python/pull/8580))
- Remove typing information for kwargs to not conflict with type checkers ([#8546](https://github.com/googleapis/google-cloud-python/pull/8546))
- Add docs job to publish to googleapis.dev. ([#8464](https://github.com/googleapis/google-cloud-python/pull/8464))
- Declare encoding as utf-8 in pb2 files (via synth). ([#8350](https://github.com/googleapis/google-cloud-python/pull/8350))
- Add disclaimer to auto-generated template files (via synth). ([#8312](https://github.com/googleapis/google-cloud-python/pull/8312))
- Suppress checking 'cov-fail-under' in nox default session (via synth). ([#8238](https://github.com/googleapis/google-cloud-python/pull/8238))
- Blacken noxfile.py, setup.py (via synth). ([#8120](https://github.com/googleapis/google-cloud-python/pull/8120))
- Add empty lines (via synth). ([#8055](https://github.com/googleapis/google-cloud-python/pull/8055))

## 1.8.0

05-17-2019 08:28 PDT

### Implementation Changes
- Add routing header to method metadata (via synth). ([#7593](https://github.com/googleapis/google-cloud-python/pull/7593))
- Remove classifier for Python 3.4 for end-of-life. ([#7535](https://github.com/googleapis/google-cloud-python/pull/7535))

### New Features
- Add `client_info` support to client. ([#8013](https://github.com/googleapis/google-cloud-python/pull/8013))

### Dependencies
- Pin `google-cloud-core >= 1.0.0, < 2.0dev`. ([#7993](https://github.com/googleapis/google-cloud-python/pull/7993))

### Documentation
- Update client library documentation URLs. ([#7307](https://github.com/googleapis/google-cloud-python/pull/7307))
- Pick up stub docstring fix in GAPIC generator. ([#6968](https://github.com/googleapis/google-cloud-python/pull/6968))

### Internal / Testing Changes
- Add nox session `docs` (via synth). ([#7768](https://github.com/googleapis/google-cloud-python/pull/7768))
- Copy lintified proto files (via synth). ([#7446](https://github.com/googleapis/google-cloud-python/pull/7446))
- Add clarifying comment to blacken nox target. ([#7389](https://github.com/googleapis/google-cloud-python/pull/7389))
- Add protos as an artifact to library ([#7205](https://github.com/googleapis/google-cloud-python/pull/7205))
- Update copyright headers ([#7142](https://github.com/googleapis/google-cloud-python/pull/7142))
- Protoc-generated serialization update. ([#7080](https://github.com/googleapis/google-cloud-python/pull/7080))

## 1.7.3

12-17-2018 16:45 PST


### Documentation
- Show use of 'batch.begin()' in docstring example. ([#6932](https://github.com/googleapis/google-cloud-python/pull/6932))
- Document Python 2 deprecation ([#6910](https://github.com/googleapis/google-cloud-python/pull/6910))

## 1.7.2

12-10-2018 12:37 PST


### Implementation Changes
- Fix client_info bug, update docstrings. ([#6409](https://github.com/googleapis/google-cloud-python/pull/6409))
- Pick up fixes in GAPIC generator. ([#6494](https://github.com/googleapis/google-cloud-python/pull/6494))
- Import `iam.policy` from `google.api_core`. ([#6741](https://github.com/googleapis/google-cloud-python/pull/6741))
- Pick up enum fixes in the GAPIC generator. ([#6610](https://github.com/googleapis/google-cloud-python/pull/6610))

### Dependencies
- Bump minimum `api_core` version for all GAPIC libs to 1.4.1. ([#6391](https://github.com/googleapis/google-cloud-python/pull/6391))
- Update version of google-cloud-core ([#6858](https://github.com/googleapis/google-cloud-python/pull/6858))

### Internal / Testing Changes
- Update noxfile.
- Add synth metadata. ([#6564](https://github.com/googleapis/google-cloud-python/pull/6564))
- blacken all gen'd libs ([#6792](https://github.com/googleapis/google-cloud-python/pull/6792))
- omit local deps ([#6701](https://github.com/googleapis/google-cloud-python/pull/6701))
- Run black at end of synth.py ([#6698](https://github.com/googleapis/google-cloud-python/pull/6698))
- Run Black on Generated libraries ([#6666](https://github.com/googleapis/google-cloud-python/pull/6666))
- Add templates for flake8, coveragerc, noxfile, and black. ([#6642](https://github.com/googleapis/google-cloud-python/pull/6642))

## 1.7.1

10-29-2018 10:38 PDT

### Implementation Changes
- Propagate empty arrays in entity values. ([#6285](https://github.com/googleapis/google-cloud-python/pull/6285))
- Expose 'Client.base_url' property to allow alternate endpoints. ([#5821](https://github.com/googleapis/google-cloud-python/pull/5821))

### Documentation
- Normalize use of support level badges ([#6159](https://github.com/googleapis/google-cloud-python/pull/6159))
- Redirect renamed 'usage.html'/'client.html' -> 'index.html'. ([#5996](https://github.com/googleapis/google-cloud-python/pull/5996))
- Replace links to '/stable/' with '/latest/'. ([#5901](https://github.com/googleapis/google-cloud-python/pull/5901))

### Internal / Testing Changes
- Use new Nox ([#6175](https://github.com/googleapis/google-cloud-python/pull/6175))
- Add 'synth.py'. ([#6078](https://github.com/googleapis/google-cloud-python/pull/6078))
- Prep datastore docs for repo split. ([#5919](https://github.com/googleapis/google-cloud-python/pull/5919))
- Use inplace installs under `nox` ([#5865](https://github.com/googleapis/google-cloud-python/pull/5865))

## 1.7.0

### Implementation Changes

- Do not pass 'offset' once the query iterator has a cursor (#5503)
- Add test runs for Python 3.7 and remove run for 3.4 (#5295)

### Documentation

- minor fix to datastore example (#5452)
- Add example showing explicit unicode for text values in entities. (#5263)

### Internal / Testing Changes

- Modify system tests to use prerelease versions of grpcio (#5304)
- Avoid overwriting '__module__' of messages from shared modules. (#5364)
- Attempt again to reproduce #4264. (#5403)
- Fix bad trove classifier

## 1.6.0

### Implementation changes

- Don't check `exclude_from_indexes` for empty lists. (#4915)

### Dependencies

- The minimum version for `google-api-core` has been updated to version 1.0.0. This may cause some incompatibility with older google-cloud libraries, you will need to update those libraries if you have a dependency conflict. (#4944, #4946)

### Testing and internal changes

- Install local dependencies when running lint (#4936)
- Re-enable lint for tests, remove usage of pylint (#4921)
- Normalize all setup.py files (#4909)
- Exercise datastore query result paging (#4905)
- Pass `*session.posargs` through on command line for system tests. (#4904)

## 1.5.0

### Interface additions

- Added `Entity.id` property (#4640)
- Added optional `location_prefix` kwarg in `to_legacy_urlsafe` (#4635)
- Added support for transaction options (#4357)
- Added the ability to specify read consistency (#4343, #4376)

### Implementation changes

- The underlying autogenerated code was rengereated to pick up new features and bugfixes. (#4348, #4877)
- Updated the HTTP implementation to match the gRPC implementation. (#4388)
- Set `next_page_token` to `None` if there are no more results (#4349)

### Documentation

- Entity doc consistency (#4641)
- Fixing "Fore" -> "For" typo in README docs. (#4317)

### Testing

- Update datastore doctests to reflect change in cursor behavior. (#4382)
- Making a `nox -s default` session for all packages. (#4324)
- Shorten test names (#4321)


## 1.4.0

### Interface changes / additions

- Allowing `dict` (as an `Entity`) for property values. (#3927)

### Documentation

- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-datastore/1.4.0/
