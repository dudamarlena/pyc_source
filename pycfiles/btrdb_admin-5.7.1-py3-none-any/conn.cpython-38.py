# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/btrdb/conn.py
# Compiled at: 2019-06-20 16:48:30
# Size of source mod 2**32: 10995 bytes
__doc__ = '\nConnection related objects for the BTrDB library\n'
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

    def __init__--- This code section failed: ---

 L.  58         0  LOAD_FAST                'addrportstr'
                2  LOAD_METHOD              split
                4  LOAD_STR                 ':'
                6  LOAD_CONST               2
                8  CALL_METHOD_2         2  ''
               10  STORE_FAST               'addrport'

 L.  59        12  LOAD_STR                 'grpc.default_compression_algorithm'
               14  LOAD_GLOBAL              CompressionAlgorithm
               16  LOAD_ATTR                gzip
               18  BUILD_TUPLE_2         2 
               20  BUILD_LIST_1          1 
               22  STORE_FAST               'chan_ops'

 L.  61        24  LOAD_GLOBAL              len
               26  LOAD_FAST                'addrport'
               28  CALL_FUNCTION_1       1  ''
               30  LOAD_CONST               2
               32  COMPARE_OP               !=
               34  POP_JUMP_IF_FALSE    44  'to 44'

 L.  62        36  LOAD_GLOBAL              ValueError
               38  LOAD_STR                 'expecting address:port'
               40  CALL_FUNCTION_1       1  ''
               42  RAISE_VARARGS_1       1  ''
             44_0  COME_FROM            34  '34'

 L.  64        44  LOAD_FAST                'addrport'
               46  LOAD_CONST               1
               48  BINARY_SUBSCR    
               50  LOAD_STR                 '4411'
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE   186  'to 186'

 L.  68        56  LOAD_GLOBAL              os
               58  LOAD_METHOD              getenv
               60  LOAD_STR                 'BTRDB_CA_BUNDLE'
               62  LOAD_STR                 ''
               64  CALL_METHOD_2         2  ''
               66  STORE_FAST               'ca_bundle'

 L.  69        68  LOAD_FAST                'ca_bundle'
               70  LOAD_STR                 ''
               72  COMPARE_OP               !=
               74  POP_JUMP_IF_FALSE   108  'to 108'

 L.  70        76  LOAD_GLOBAL              open
               78  LOAD_FAST                'ca_bundle'
               80  LOAD_STR                 'rb'
               82  CALL_FUNCTION_2       2  ''
               84  SETUP_WITH          100  'to 100'
               86  STORE_FAST               'f'

 L.  71        88  LOAD_FAST                'f'
               90  LOAD_METHOD              read
               92  CALL_METHOD_0         0  ''
               94  STORE_FAST               'contents'
               96  POP_BLOCK        
               98  BEGIN_FINALLY    
            100_0  COME_FROM_WITH       84  '84'
              100  WITH_CLEANUP_START
              102  WITH_CLEANUP_FINISH
              104  END_FINALLY      
              106  JUMP_FORWARD        112  'to 112'
            108_0  COME_FROM            74  '74'

 L.  73       108  LOAD_CONST               None
              110  STORE_FAST               'contents'
            112_0  COME_FROM           106  '106'

 L.  75       112  LOAD_FAST                'apikey'
              114  LOAD_CONST               None
              116  COMPARE_OP               is
              118  POP_JUMP_IF_FALSE   146  'to 146'

 L.  76       120  LOAD_GLOBAL              grpc
              122  LOAD_ATTR                secure_channel

 L.  77       124  LOAD_FAST                'addrportstr'

 L.  78       126  LOAD_GLOBAL              grpc
              128  LOAD_METHOD              ssl_channel_credentials
              130  LOAD_FAST                'contents'
              132  CALL_METHOD_1         1  ''

 L.  79       134  LOAD_FAST                'chan_ops'

 L.  76       136  LOAD_CONST               ('options',)
              138  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              140  LOAD_FAST                'self'
              142  STORE_ATTR               channel
              144  JUMP_ABSOLUTE       216  'to 216'
            146_0  COME_FROM           118  '118'

 L.  82       146  LOAD_GLOBAL              grpc
              148  LOAD_ATTR                secure_channel

 L.  83       150  LOAD_FAST                'addrportstr'

 L.  84       152  LOAD_GLOBAL              grpc
              154  LOAD_METHOD              composite_channel_credentials

 L.  85       156  LOAD_GLOBAL              grpc
              158  LOAD_METHOD              ssl_channel_credentials
              160  LOAD_FAST                'contents'
              162  CALL_METHOD_1         1  ''

 L.  86       164  LOAD_GLOBAL              grpc
              166  LOAD_METHOD              access_token_call_credentials
              168  LOAD_FAST                'apikey'
              170  CALL_METHOD_1         1  ''

 L.  84       172  CALL_METHOD_2         2  ''

 L.  88       174  LOAD_FAST                'chan_ops'

 L.  82       176  LOAD_CONST               ('options',)
              178  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              180  LOAD_FAST                'self'
              182  STORE_ATTR               channel
              184  JUMP_FORWARD        216  'to 216'
            186_0  COME_FROM            54  '54'

 L.  91       186  LOAD_FAST                'apikey'
              188  LOAD_CONST               None
              190  COMPARE_OP               is-not
              192  POP_JUMP_IF_FALSE   202  'to 202'

 L.  92       194  LOAD_GLOBAL              ValueError
              196  LOAD_STR                 'cannot use an API key with an insecure (port 4410) BTrDB API. Try port 4411'
              198  CALL_FUNCTION_1       1  ''
              200  RAISE_VARARGS_1       1  ''
            202_0  COME_FROM           192  '192'

 L.  93       202  LOAD_GLOBAL              grpc
              204  LOAD_METHOD              insecure_channel
              206  LOAD_FAST                'addrportstr'
              208  LOAD_FAST                'chan_ops'
              210  CALL_METHOD_2         2  ''
              212  LOAD_FAST                'self'
              214  STORE_ATTR               channel
            216_0  COME_FROM           184  '184'

Parse error at or near `BEGIN_FINALLY' instruction at offset 98


class BTrDB(object):
    """BTrDB"""

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
        return [json.loadsrow.decode'utf-8' for page in self.ep.sql_querystmtparams for row in page]

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
               24  RAISE_VARARGS_1       1  ''
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
               52  RAISE_VARARGS_1       1  ''
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
              236  RAISE_VARARGS_1       1  ''
            238_0  COME_FROM           146  '146'
            238_1  COME_FROM           104  '104'

 L. 188       238  LOAD_GLOBAL              ValueError
              240  LOAD_STR                 'Could not identify stream based on `'
              242  LOAD_FAST                'ident'
              244  FORMAT_VALUE          0  ''
              246  LOAD_STR                 '`.  Identifier must be UUID or collection/name.'
              248  BUILD_STRING_3        3 
              250  CALL_FUNCTION_1       1  ''
              252  RAISE_VARARGS_1       1  ''
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
        return Streamselfto_uuid(uuid)

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
          tags=(tags.copy),
          annotations=(annotations.copy),
          property_version=0)

    def info(self):
        """
        Returns information about the connected BTrDB srerver.

        Returns
        -------
        dict
            server connection and status information

        """
        info = self.ep.info
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
        return [c for some in self.ep.listCollectionsstarts_with for c in some]

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
                    result.appendStream(self,
                      uuidlib.UUID(bytes=(desc.uuid)), known_to_exist=True,
                      collection=(desc.collection),
                      tags=(tagsanns[0]),
                      annotations=(tagsanns[1]),
                      property_version=(desc.propertyVersion))

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
        tags, annotations = ep.getMetadataUsageprefix
        pyTags = {tag.count:tag.key for tag in tags}
        pyAnn = {ann.count:ann.key for ann in annotations}
        return (
         pyTags, pyAnn)