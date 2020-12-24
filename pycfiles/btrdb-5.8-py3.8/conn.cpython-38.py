# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/btrdb/conn.py
# Compiled at: 2019-06-20 16:48:30
# Size of source mod 2**32: 10995 bytes
"""
Connection related objects for the BTrDB library
"""
import os, re, json, uuid as uuidlib, grpc
from grpc._cython.cygrpc import CompressionAlgorithm
from btrdb.stream import Stream, StreamSet
from btrdb.utils.general import unpack_stream_descriptor
from btrdb.utils.conversion import to_uuid
from btrdb.exceptions import NotFound
MIN_TIME = -1152921504606846976
MAX_TIME = 3458764513820540928
MAX_POINTWIDTH = 63

class Connection(object):

    def __init__(self, addrportstr, apikey=None):
        """
        Connects to a BTrDB server

        Parameters
        ----------
        addrportstr: str
            The address of the cluster to connect to, e.g 123.123.123:4411
        apikey: str
            The option API key to authenticate requests

        """
        addrport = addrportstr.split(':', 2)
        chan_ops = [('grpc.default_compression_algorithm', CompressionAlgorithm.gzip)]
        if len(addrport) != 2:
            raise ValueError('expecting address:port')
        elif addrport[1] == '4411':
            ca_bundle = os.getenv('BTRDB_CA_BUNDLE', '')
            if ca_bundle != '':
                with open(ca_bundle, 'rb') as (f):
                    contents = f.read()
            else:
                contents = None
            if apikey is None:
                self.channel = grpc.secure_channel(addrportstr,
                  (grpc.ssl_channel_credentials(contents)),
                  options=chan_ops)
            else:
                self.channel = grpc.secure_channel(addrportstr,
                  (grpc.composite_channel_credentials(grpc.ssl_channel_credentials(contents), grpc.access_token_call_credentials(apikey))),
                  options=chan_ops)
        else:
            if apikey is not None:
                raise ValueError('cannot use an API key with an insecure (port 4410) BTrDB API. Try port 4411')
            self.channel = grpc.insecure_channel(addrportstr, chan_ops)


class BTrDB(object):
    __doc__ = '\n    The primary server connection object for communicating with a BTrDB server.\n    '

    def __init__(self, endpoint):
        self.ep = endpoint

    def query(self, stmt, params=[]):
        """
        Performs a SQL query on the database metadata and returns a list of
        dictionaries from the resulting cursor.

        Parameters
        ----------
        stmt: str
            a SQL statement to be executed on the BTrDB metadata.  Available
            tables are noted below.  To sanitize inputs use a `$1` style parameter such as
            `select * from streams where name = $1 or name = $2`.
        params: list or tuple
            a list of parameter values to be sanitized and interpolated into the
            SQL statement. Using parameters forces value/type checking and is
            considered a best practice at the very least.

        Returns
        -------
        list
            a list of dictionary object representing the cursor results.

        Notes
        -------
        Parameters will be inserted into the SQL statement as noted by the
        paramter number such as `$1`, `$2`, or `$3`.  The `streams` table is
        available for `SELECT` statements only.

        See https://btrdb.readthedocs.io/en/latest/ for more info.
        """
        return [json.loads(row.decode('utf-8')) for page in self.ep.sql_query(stmt, params) for row in page]

    def streams--- This code section failed: ---

 L. 160         0  LOAD_DEREF               'versions'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
                6  POP_JUMP_IF_FALSE    26  'to 26'
                8  LOAD_GLOBAL              isinstance
               10  LOAD_DEREF               'versions'
               12  LOAD_GLOBAL              list
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_TRUE     26  'to 26'

 L. 161        18  LOAD_GLOBAL              TypeError
               20  LOAD_STR                 'versions argument must be of type list'
               22  CALL_FUNCTION_1       1  ''
               24  RAISE_VARARGS_1       1  'exception instance'
             26_0  COME_FROM            16  '16'
             26_1  COME_FROM             6  '6'

 L. 163        26  LOAD_DEREF               'versions'
               28  POP_JUMP_IF_FALSE    54  'to 54'
               30  LOAD_GLOBAL              len
               32  LOAD_DEREF               'versions'
               34  CALL_FUNCTION_1       1  ''
               36  LOAD_GLOBAL              len
               38  LOAD_FAST                'identifiers'
               40  CALL_FUNCTION_1       1  ''
               42  COMPARE_OP               !=
               44  POP_JUMP_IF_FALSE    54  'to 54'

 L. 164        46  LOAD_GLOBAL              ValueError
               48  LOAD_STR                 'number of versions does not match identifiers'
               50  CALL_FUNCTION_1       1  ''
               52  RAISE_VARARGS_1       1  'exception instance'
             54_0  COME_FROM            44  '44'
             54_1  COME_FROM            28  '28'

 L. 166        54  BUILD_LIST_0          0 
               56  STORE_DEREF              'streams'

 L. 167        58  LOAD_FAST                'identifiers'
               60  GET_ITER         
               62  FOR_ITER            256  'to 256'
               64  STORE_FAST               'ident'

 L. 168        66  LOAD_GLOBAL              isinstance
               68  LOAD_FAST                'ident'
               70  LOAD_GLOBAL              uuidlib
               72  LOAD_ATTR                UUID
               74  CALL_FUNCTION_2       2  ''
               76  POP_JUMP_IF_FALSE    96  'to 96'

 L. 169        78  LOAD_DEREF               'streams'
               80  LOAD_METHOD              append
               82  LOAD_FAST                'self'
               84  LOAD_METHOD              stream_from_uuid
               86  LOAD_FAST                'ident'
               88  CALL_METHOD_1         1  ''
               90  CALL_METHOD_1         1  ''
               92  POP_TOP          

 L. 170        94  JUMP_BACK            62  'to 62'
             96_0  COME_FROM            76  '76'

 L. 172        96  LOAD_GLOBAL              isinstance
               98  LOAD_FAST                'ident'
              100  LOAD_GLOBAL              str
              102  CALL_FUNCTION_2       2  ''
              104  POP_JUMP_IF_FALSE   238  'to 238'

 L. 174       106  LOAD_STR                 '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
              108  STORE_FAST               'pattern'

 L. 175       110  LOAD_GLOBAL              re
              112  LOAD_METHOD              match
              114  LOAD_FAST                'pattern'
              116  LOAD_FAST                'ident'
              118  CALL_METHOD_2         2  ''
              120  POP_JUMP_IF_FALSE   140  'to 140'

 L. 176       122  LOAD_DEREF               'streams'
              124  LOAD_METHOD              append
              126  LOAD_FAST                'self'
              128  LOAD_METHOD              stream_from_uuid
              130  LOAD_FAST                'ident'
              132  CALL_METHOD_1         1  ''
              134  CALL_METHOD_1         1  ''
              136  POP_TOP          

 L. 177       138  JUMP_BACK            62  'to 62'
            140_0  COME_FROM           120  '120'

 L. 180       140  LOAD_STR                 '/'
              142  LOAD_FAST                'ident'
              144  COMPARE_OP               in
              146  POP_JUMP_IF_FALSE   238  'to 238'

 L. 181       148  LOAD_FAST                'ident'
              150  LOAD_METHOD              split
              152  LOAD_STR                 '/'
              154  CALL_METHOD_1         1  ''
              156  STORE_FAST               'parts'

 L. 182       158  LOAD_FAST                'self'
              160  LOAD_ATTR                streams_in_collection
              162  LOAD_STR                 '/'
              164  LOAD_METHOD              join
              166  LOAD_FAST                'parts'
              168  LOAD_CONST               None
              170  LOAD_CONST               -1
              172  BUILD_SLICE_2         2 
              174  BINARY_SUBSCR    
              176  CALL_METHOD_1         1  ''
              178  LOAD_STR                 'name'
              180  LOAD_FAST                'parts'
              182  LOAD_CONST               -1
              184  BINARY_SUBSCR    
              186  BUILD_MAP_1           1 
              188  LOAD_CONST               ('tags',)
              190  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              192  STORE_FAST               'found'

 L. 183       194  LOAD_GLOBAL              len
              196  LOAD_FAST                'found'
              198  CALL_FUNCTION_1       1  ''
              200  LOAD_CONST               1
              202  COMPARE_OP               ==
              204  POP_JUMP_IF_FALSE   222  'to 222'

 L. 184       206  LOAD_DEREF               'streams'
              208  LOAD_METHOD              append
              210  LOAD_FAST                'found'
              212  LOAD_CONST               0
              214  BINARY_SUBSCR    
              216  CALL_METHOD_1         1  ''
              218  POP_TOP          

 L. 185       220  JUMP_BACK            62  'to 62'
            222_0  COME_FROM           204  '204'

 L. 186       222  LOAD_GLOBAL              NotFound
              224  LOAD_STR                 'Could not identify stream `'
              226  LOAD_FAST                'ident'
              228  FORMAT_VALUE          0  ''
              230  LOAD_STR                 '`'
              232  BUILD_STRING_3        3 
              234  CALL_FUNCTION_1       1  ''
              236  RAISE_VARARGS_1       1  'exception instance'
            238_0  COME_FROM           146  '146'
            238_1  COME_FROM           104  '104'

 L. 188       238  LOAD_GLOBAL              ValueError
              240  LOAD_STR                 'Could not identify stream based on `'
              242  LOAD_FAST                'ident'
              244  FORMAT_VALUE          0  ''
              246  LOAD_STR                 '`.  Identifier must be UUID or collection/name.'
              248  BUILD_STRING_3        3 
              250  CALL_FUNCTION_1       1  ''
              252  RAISE_VARARGS_1       1  'exception instance'
              254  JUMP_BACK            62  'to 62'

 L. 191       256  LOAD_GLOBAL              StreamSet
              258  LOAD_DEREF               'streams'
              260  CALL_FUNCTION_1       1  ''
              262  STORE_FAST               'obj'

 L. 193       264  LOAD_DEREF               'versions'
          266_268  POP_JUMP_IF_FALSE   308  'to 308'

 L. 194       270  LOAD_CLOSURE             'streams'
              272  LOAD_CLOSURE             'versions'
              274  BUILD_TUPLE_2         2 
              276  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              278  LOAD_STR                 'BTrDB.streams.<locals>.<dictcomp>'
              280  MAKE_FUNCTION_8          'closure'
              282  LOAD_GLOBAL              range
              284  LOAD_GLOBAL              len
              286  LOAD_DEREF               'versions'
              288  CALL_FUNCTION_1       1  ''
              290  CALL_FUNCTION_1       1  ''
              292  GET_ITER         
              294  CALL_FUNCTION_1       1  ''
              296  STORE_FAST               'version_dict'

 L. 195       298  LOAD_FAST                'obj'
              300  LOAD_METHOD              pin_versions
              302  LOAD_FAST                'version_dict'
              304  CALL_METHOD_1         1  ''
              306  POP_TOP          
            308_0  COME_FROM           266  '266'

 L. 197       308  LOAD_FAST                'obj'
              310  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 276

    def stream_from_uuid(self, uuid):
        """
        Creates a stream handle to the BTrDB stream with the UUID `uuid`. This
        method does not check whether a stream with the specified UUID exists.
        It is always good form to check whether the stream existed using
        `stream.exists()`.

        Parameters
        ----------
        uuid: UUID
            The uuid of the requested stream.

        Returns
        -------
        Stream
            instance of Stream class or None

        """
        return Stream(self, to_uuid(uuid))

    def create(self, uuid, collection, tags=None, annotations=None):
        """
        Tells BTrDB to create a new stream with UUID `uuid` in `collection` with specified `tags` and `annotations`.

        Parameters
        ----------
        uuid: UUID
            The uuid of the requested stream.

        Returns
        -------
        Stream
            instance of Stream class
        """
        if tags is None:
            tags = {}
        if annotations is None:
            annotations = {}
        self.ep.create(uuid, collection, tags, annotations)
        return Stream(self, uuid, known_to_exist=True,
          collection=collection,
          tags=(tags.copy()),
          annotations=(annotations.copy()),
          property_version=0)

    def info(self):
        """
        Returns information about the connected BTrDB srerver.

        Returns
        -------
        dict
            server connection and status information

        """
        info = self.ep.info()
        return {'majorVersion':info.majorVersion, 
         'build':info.build, 
         'proxy':{'proxyEndpoints': [ep for ep in info.proxy.proxyEndpoints]}}

    def list_collections(self, starts_with=''):
        """
        Returns a list of collection paths using the `starts_with` argument for
        filtering.

        Returns
        -------
        collection paths: list[str]

        """
        return [c for some in self.ep.listCollections(starts_with) for c in some]

    def streams_in_collection(self, *collection, is_collection_prefix=True, tags=None, annotations=None):
        """
        Search for streams matching given parameters

        This function allows for searching

        Parameters
        ----------
        collection: str
            collections to use when searching for streams, case sensitive.
        is_collection_prefix: bool
            Whether the collection is a prefix.
        tags: Dict[str, str]
            The tags to identify the stream.
        annotations: Dict[str, str]
            The annotations to identify the stream.

        Returns
        ------
        list
            A list of stream objects found with the provided search arguments.

        """
        result = []
        if tags is None:
            tags = {}
        if annotations is None:
            annotations = {}
        if not collection:
            collection = [
             None]
        for item in collection:
            streams = self.ep.lookupStreams(item, is_collection_prefix, tags, annotations)
            for desclist in streams:
                for desc in desclist:
                    tagsanns = unpack_stream_descriptor(desc)
                    result.append(Stream(self,
                      uuidlib.UUID(bytes=(desc.uuid)), known_to_exist=True,
                      collection=(desc.collection),
                      tags=(tagsanns[0]),
                      annotations=(tagsanns[1]),
                      property_version=(desc.propertyVersion)))

            else:
                return result

    def collection_metadata(self, prefix):
        """
        Gives statistics about metadata for collections that match a
        prefix.

        Parameters
        ----------
        prefix: str
            A prefix of the collection names to look at

        Returns
        -------
        tuple
            A tuple of dictionaries containing metadata on the streams in the
            provided collection.

        """
        ep = self.ep
        tags, annotations = ep.getMetadataUsage(prefix)
        pyTags = {tag.count:tag.key for tag in tags}
        pyAnn = {ann.count:ann.key for ann in annotations}
        return (pyTags, pyAnn)