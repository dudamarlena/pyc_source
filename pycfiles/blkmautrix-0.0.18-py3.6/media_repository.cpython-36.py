# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/modules/media_repository.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 6881 bytes
from typing import Optional, AsyncIterable, Union
from ....api import Method, MediaPath
from ....errors import MatrixResponseError
from ..base import BaseClientAPI
from ..types import ContentURI, MediaRepoConfig, SerializerError, MXOpenGraph
try:
    import magic
except ImportError:
    magic = None

class MediaRepositoryMethods(BaseClientAPI):
    __doc__ = '\n    Methods in section 13.8 Content Repository of the spec. These methods are used for uploading and\n    downloading content from the media repository and for getting URL previews without leaking\n    client IPs.\n\n    See also: `API reference <https://matrix.org/docs/spec/client_server/r0.4.0.html#id112>`__'

    async def upload_media(self, data: Union[(bytes, AsyncIterable[bytes])], mime_type: Optional[str]=None, filename: Optional[str]=None, size: Optional[int]=None) -> ContentURI:
        """
        Upload a file to the content repository.

        See also: `API reference <https://matrix.org/docs/spec/client_server/r0.4.0.html#post-matrix-media-r0-upload>`__

        Args:
            data: The data to upload.
            mime_type: The MIME type to send with the upload request.
            filename: The filename to send with the upload request.
            size: The file size to send with the upload request.

        Returns:
            The MXC URI to the uploaded file.

        Raises:
            MatrixResponseError: If the response does not contain a ``content_uri`` field.
        """
        if magic:
            if isinstance(data, bytes):
                mime_type = mime_type or magic.from_buffer(data, mime=True)
            headers = {}
            if mime_type:
                headers['Content-Type'] = mime_type
            if size:
                headers['Content-Length'] = str(size)
        else:
            query = {}
            if filename:
                query['filename'] = filename
            resp = await self.api.request((Method.POST), (MediaPath.upload), content=data, headers=headers,
              query_params=query)
            try:
                return resp['content_uri']
            except KeyError:
                raise MatrixResponseError('`content_uri` not in response.')

    async def download_media--- This code section failed: ---

 L.  76         0  LOAD_FAST                'self'
                2  LOAD_ATTR                api
                4  LOAD_ATTR                get_download_url
                6  LOAD_FAST                'url'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  STORE_FAST               'url'

 L.  77        12  LOAD_FAST                'self'
               14  LOAD_ATTR                api
               16  LOAD_ATTR                session
               18  LOAD_ATTR                get
               20  LOAD_FAST                'url'
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  BEFORE_ASYNC_WITH
               26  GET_AWAITABLE    
               28  LOAD_CONST               None
               30  YIELD_FROM       
               32  SETUP_ASYNC_WITH     50  'to 50'
               34  STORE_FAST               'response'

 L.  78        36  LOAD_FAST                'response'
               38  LOAD_ATTR                read
               40  CALL_FUNCTION_0       0  '0 positional arguments'
               42  GET_AWAITABLE    
               44  LOAD_CONST               None
               46  YIELD_FROM       
               48  RETURN_VALUE     
             50_0  COME_FROM_ASYNC_WITH    32  '32'
               50  WITH_CLEANUP_START
               52  GET_AWAITABLE    
               54  LOAD_CONST               None
               56  YIELD_FROM       
               58  WITH_CLEANUP_FINISH
               60  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 50_0

    async def download_thumbnail--- This code section failed: ---

 L. 102         0  LOAD_FAST                'self'
                2  LOAD_ATTR                api
                4  LOAD_ATTR                get_download_url
                6  LOAD_FAST                'url'
                8  LOAD_STR                 'thumbnail'
               10  LOAD_CONST               ('download_type',)
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  STORE_FAST               'url'

 L. 103        16  BUILD_MAP_0           0 
               18  STORE_FAST               'query_params'

 L. 104        20  LOAD_FAST                'width'
               22  LOAD_CONST               None
               24  COMPARE_OP               is-not
               26  POP_JUMP_IF_FALSE    36  'to 36'

 L. 105        28  LOAD_FAST                'width'
               30  LOAD_FAST                'query_params'
               32  LOAD_STR                 'width'
               34  STORE_SUBSCR     
             36_0  COME_FROM            26  '26'

 L. 106        36  LOAD_FAST                'height'
               38  LOAD_CONST               None
               40  COMPARE_OP               is-not
               42  POP_JUMP_IF_FALSE    52  'to 52'

 L. 107        44  LOAD_FAST                'height'
               46  LOAD_FAST                'query_params'
               48  LOAD_STR                 'height'
               50  STORE_SUBSCR     
             52_0  COME_FROM            42  '42'

 L. 108        52  LOAD_FAST                'resize_method'
               54  LOAD_CONST               None
               56  COMPARE_OP               is-not
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L. 109        60  LOAD_FAST                'resize_method'
               62  LOAD_FAST                'query_params'
               64  LOAD_STR                 'resize_method'
               66  STORE_SUBSCR     
             68_0  COME_FROM            58  '58'

 L. 110        68  LOAD_FAST                'allow_remote'
               70  LOAD_CONST               None
               72  COMPARE_OP               is-not
               74  POP_JUMP_IF_FALSE    84  'to 84'

 L. 111        76  LOAD_FAST                'allow_remote'
               78  LOAD_FAST                'query_params'
               80  LOAD_STR                 'allow_remote'
               82  STORE_SUBSCR     
             84_0  COME_FROM            74  '74'

 L. 112        84  LOAD_FAST                'self'
               86  LOAD_ATTR                api
               88  LOAD_ATTR                session
               90  LOAD_ATTR                get
               92  LOAD_FAST                'url'
               94  LOAD_FAST                'query_params'
               96  LOAD_CONST               ('params',)
               98  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              100  BEFORE_ASYNC_WITH
              102  GET_AWAITABLE    
              104  LOAD_CONST               None
              106  YIELD_FROM       
              108  SETUP_ASYNC_WITH    126  'to 126'
              110  STORE_FAST               'response'

 L. 113       112  LOAD_FAST                'response'
              114  LOAD_ATTR                read
              116  CALL_FUNCTION_0       0  '0 positional arguments'
              118  GET_AWAITABLE    
              120  LOAD_CONST               None
              122  YIELD_FROM       
              124  RETURN_VALUE     
            126_0  COME_FROM_ASYNC_WITH   108  '108'
              126  WITH_CLEANUP_START
              128  GET_AWAITABLE    
              130  LOAD_CONST               None
              132  YIELD_FROM       
              134  WITH_CLEANUP_FINISH
              136  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 126_0

    async def get_url_preview(self, url: str, timestamp: Optional[int]=None) -> MXOpenGraph:
        """
        Get information about a URL for a client.

        See also: `API reference <https://matrix.org/docs/spec/client_server/r0.4.0.html#get-matrix-media-r0-preview-url>`__

        Args:
            url: The URL to get a preview of.
            timestamp: The preferred point in time to return a preview for. The server may return a
                newer version if it does not have the requested version available.
        """
        query_params = {'url': url}
        if timestamp is not None:
            query_params['ts'] = timestamp
        content = await self.api.request((Method.GET), (MediaPath.preview_url), query_params=query_params)
        try:
            return MXOpenGraph.deserialize(content)
        except SerializerError as e:
            raise MatrixResponseError('Invalid MXOpenGraph in response.') from e

    async def get_media_repo_config(self) -> MediaRepoConfig:
        """
        This endpoint allows clients to retrieve the configuration of the content repository, such
        as upload limitations. Clients SHOULD use this as a guide when using content repository
        endpoints. All values are intentionally left optional. Clients SHOULD follow the advice
        given in the field description when the field is not available.

        **NOTE:** Both clients and server administrators should be aware that proxies between the
        client and the server may affect the apparent behaviour of content repository APIs, for
        example, proxies may enforce a lower upload size limit than is advertised by the server on
        this endpoint.

        See also: `API reference <https://matrix.org/docs/spec/client_server/r0.4.0.html#get-matrix-media-r0-config>`__

        Returns:
            The media repository config.
        """
        content = await self.api.request(Method.GET, MediaPath.config)
        try:
            return MediaRepoConfig.deserialize(content)
        except SerializerError as e:
            raise MatrixResponseError('Invalid MediaRepoConfig in response') from e