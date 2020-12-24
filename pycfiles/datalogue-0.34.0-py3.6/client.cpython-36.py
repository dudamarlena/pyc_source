# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/anduin/client.py
# Compiled at: 2020-04-24 18:45:43
# Size of source mod 2**32: 1415 bytes
from typing import Optional, Union
from datalogue.clients.http import _HttpClient, HttpMethod
from datalogue.anduin.models.stream import Stream, StreamStatus
from datalogue.errors import DtlError
from uuid import UUID

class _AnduinClient:
    __doc__ = '\n    Client to interact with the Anduin APIs\n    '

    def __init__(self, http_client: _HttpClient):
        self.http_client = http_client

    def run(self, stream: Stream, stream_id: Optional[UUID]=None) -> Union[(DtlError, UUID)]:
        """
        Run given stream directly through Anduin
        :param stream: Stream to run
        :param stream_id: Id to be used by the stream
        :return: Returns stream id
        """
        params = {}
        if id is not None:
            params = {'id': stream_id}
        res = self.http_client.make_authed_request('/run', (HttpMethod.POST), (stream._as_payload()), params=params)
        if isinstance(res, DtlError):
            return res
        else:
            return res['streamId']

    def status(self, stream_id: UUID) -> Union[(DtlError, StreamStatus)]:
        """
        Returns the status of given stream id
        :param stream_id: Id of the stream
        :return: Returns status of the stream
        """
        res = self.http_client.make_authed_request('/status/' + str(stream_id), HttpMethod.GET)
        if isinstance(res, DtlError):
            return res
        else:
            return StreamStatus.from_payload(res)