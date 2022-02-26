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
import warnings
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import gapic_v1
from google.api_core import grpc_helpers_async
from google.api_core import operations_v1
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.datastore_admin_v1.types import datastore_admin
from google.cloud.datastore_admin_v1.types import index
from google.longrunning import operations_pb2  # type: ignore
from .base import DatastoreAdminTransport, DEFAULT_CLIENT_INFO
from .grpc import DatastoreAdminGrpcTransport


class DatastoreAdminGrpcAsyncIOTransport(DatastoreAdminTransport):
    """gRPC AsyncIO backend transport for DatastoreAdmin.

    Google Cloud Datastore Admin API
    The Datastore Admin API provides several admin services for
    Cloud Datastore.
    -----------------------------------------------------------------------------
    ## Concepts

    Project, namespace, kind, and entity as defined in the Google
    Cloud Datastore API.

    Operation: An Operation represents work being performed in the
    background.
    EntityFilter: Allows specifying a subset of entities in a
    project. This is specified as a combination of kinds and
    namespaces (either or both of which may be all).

    -----------------------------------------------------------------------------
    ## Services

    # Export/Import

    The Export/Import service provides the ability to copy all or a
    subset of entities to/from Google Cloud Storage.

    Exported data may be imported into Cloud Datastore for any
    Google Cloud Platform project. It is not restricted to the
    export source project. It is possible to export from one project
    and then import into another.
    Exported data can also be loaded into Google BigQuery for
    analysis.
    Exports and imports are performed asynchronously. An Operation
    resource is created for each export/import. The state (including
    any errors encountered) of the export/import may be queried via
    the Operation resource.
    # Index

    The index service manages Cloud Datastore composite indexes.
    Index creation and deletion are performed asynchronously. An
    Operation resource is created for each such asynchronous
    operation. The state of the operation (including any errors
    encountered) may be queried via the Operation resource.

    # Operation

    The Operations collection provides a record of actions performed
    for the specified project (including any operations in
    progress). Operations are not created directly but through calls
    on other collections or resources.
    An operation that is not yet done may be cancelled. The request
    to cancel is asynchronous and the operation may continue to run
    for some time after the request to cancel is made.

    An operation that is done may be deleted so that it is no longer
    listed as part of the Operation collection.

    ListOperations returns all pending operations, but not completed
    operations.
    Operations are created by service DatastoreAdmin,
    but are accessed via service google.longrunning.Operations.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "datastore.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "datastore.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None,
        ssl_channel_credentials: grpc.ChannelCredentials = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id=None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsAsyncClient] = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def export_entities(
        self,
    ) -> Callable[
        [datastore_admin.ExportEntitiesRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the export entities method over gRPC.

        Exports a copy of all or a subset of entities from
        Google Cloud Datastore to another storage system, such
        as Google Cloud Storage. Recent updates to entities may
        not be reflected in the export. The export occurs in the
        background and its progress can be monitored and managed
        via the Operation resource that is created. The output
        of an export may only be used once the associated
        operation is done. If an export operation is cancelled
        before completion it may leave partial data behind in
        Google Cloud Storage.

        Returns:
            Callable[[~.ExportEntitiesRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_entities" not in self._stubs:
            self._stubs["export_entities"] = self.grpc_channel.unary_unary(
                "/google.datastore.admin.v1.DatastoreAdmin/ExportEntities",
                request_serializer=datastore_admin.ExportEntitiesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["export_entities"]

    @property
    def import_entities(
        self,
    ) -> Callable[
        [datastore_admin.ImportEntitiesRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the import entities method over gRPC.

        Imports entities into Google Cloud Datastore.
        Existing entities with the same key are overwritten. The
        import occurs in the background and its progress can be
        monitored and managed via the Operation resource that is
        created. If an ImportEntities operation is cancelled, it
        is possible that a subset of the data has already been
        imported to Cloud Datastore.

        Returns:
            Callable[[~.ImportEntitiesRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_entities" not in self._stubs:
            self._stubs["import_entities"] = self.grpc_channel.unary_unary(
                "/google.datastore.admin.v1.DatastoreAdmin/ImportEntities",
                request_serializer=datastore_admin.ImportEntitiesRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["import_entities"]

    @property
    def create_index(
        self,
    ) -> Callable[
        [datastore_admin.CreateIndexRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the create index method over gRPC.

        Creates the specified index. A newly created index's initial
        state is ``CREATING``. On completion of the returned
        [google.longrunning.Operation][google.longrunning.Operation],
        the state will be ``READY``. If the index already exists, the
        call will return an ``ALREADY_EXISTS`` status.

        During index creation, the process could result in an error, in
        which case the index will move to the ``ERROR`` state. The
        process can be recovered by fixing the data that caused the
        error, removing the index with
        [delete][google.datastore.admin.v1.DatastoreAdmin.DeleteIndex],
        then re-creating the index with [create]
        [google.datastore.admin.v1.DatastoreAdmin.CreateIndex].

        Indexes with a single property cannot be created.

        Returns:
            Callable[[~.CreateIndexRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_index" not in self._stubs:
            self._stubs["create_index"] = self.grpc_channel.unary_unary(
                "/google.datastore.admin.v1.DatastoreAdmin/CreateIndex",
                request_serializer=datastore_admin.CreateIndexRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["create_index"]

    @property
    def delete_index(
        self,
    ) -> Callable[
        [datastore_admin.DeleteIndexRequest], Awaitable[operations_pb2.Operation]
    ]:
        r"""Return a callable for the delete index method over gRPC.

        Deletes an existing index. An index can only be deleted if it is
        in a ``READY`` or ``ERROR`` state. On successful execution of
        the request, the index will be in a ``DELETING``
        [state][google.datastore.admin.v1.Index.State]. And on
        completion of the returned
        [google.longrunning.Operation][google.longrunning.Operation],
        the index will be removed.

        During index deletion, the process could result in an error, in
        which case the index will move to the ``ERROR`` state. The
        process can be recovered by fixing the data that caused the
        error, followed by calling
        [delete][google.datastore.admin.v1.DatastoreAdmin.DeleteIndex]
        again.

        Returns:
            Callable[[~.DeleteIndexRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_index" not in self._stubs:
            self._stubs["delete_index"] = self.grpc_channel.unary_unary(
                "/google.datastore.admin.v1.DatastoreAdmin/DeleteIndex",
                request_serializer=datastore_admin.DeleteIndexRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_index"]

    @property
    def get_index(
        self,
    ) -> Callable[[datastore_admin.GetIndexRequest], Awaitable[index.Index]]:
        r"""Return a callable for the get index method over gRPC.

        Gets an index.

        Returns:
            Callable[[~.GetIndexRequest],
                    Awaitable[~.Index]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_index" not in self._stubs:
            self._stubs["get_index"] = self.grpc_channel.unary_unary(
                "/google.datastore.admin.v1.DatastoreAdmin/GetIndex",
                request_serializer=datastore_admin.GetIndexRequest.serialize,
                response_deserializer=index.Index.deserialize,
            )
        return self._stubs["get_index"]

    @property
    def list_indexes(
        self,
    ) -> Callable[
        [datastore_admin.ListIndexesRequest],
        Awaitable[datastore_admin.ListIndexesResponse],
    ]:
        r"""Return a callable for the list indexes method over gRPC.

        Lists the indexes that match the specified filters.
        Datastore uses an eventually consistent query to fetch
        the list of indexes and may occasionally return stale
        results.

        Returns:
            Callable[[~.ListIndexesRequest],
                    Awaitable[~.ListIndexesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_indexes" not in self._stubs:
            self._stubs["list_indexes"] = self.grpc_channel.unary_unary(
                "/google.datastore.admin.v1.DatastoreAdmin/ListIndexes",
                request_serializer=datastore_admin.ListIndexesRequest.serialize,
                response_deserializer=datastore_admin.ListIndexesResponse.deserialize,
            )
        return self._stubs["list_indexes"]

    def close(self):
        return self.grpc_channel.close()


__all__ = ("DatastoreAdminGrpcAsyncIOTransport",)
