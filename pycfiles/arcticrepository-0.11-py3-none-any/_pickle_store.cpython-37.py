# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/store/_pickle_store.py
# Compiled at: 2019-12-06 10:13:42
# Size of source mod 2**32: 4751 bytes
import io, logging
from operator import itemgetter
import bson, six
from bson.binary import Binary
from bson.errors import InvalidDocument
from six.moves import cPickle, xrange
from ._version_store_utils import checksum, pickle_compat_load, version_base_or_id
from .._compression import decompress, compress_array
from ..exceptions import UnsupportedPickleStoreVersion
from .._config import SKIP_BSON_ENCODE_PICKLE_STORE, MAX_BSON_ENCODE
_MAGIC_CHUNKED = '__chunked__'
_MAGIC_CHUNKEDV2 = '__chunked__V2'
_CHUNK_SIZE = 15728640
_HARD_MAX_BSON_ENCODE = 10485760
logger = logging.getLogger(__name__)

class PickleStore(object):

    @classmethod
    def initialize_library(cls, *args, **kwargs):
        pass

    def get_info(self, _version):
        return {'type':'blob', 
         'handler':self.__class__.__name__}

    def read(self, mongoose_lib, version, symbol, **kwargs):
        blob = version.get('blob')
        if blob is not None:
            if blob == _MAGIC_CHUNKEDV2:
                collection = mongoose_lib.get_top_level_collection()
                data = ''.join((decompress(x['data']) for x in sorted((collection.find({'symbol':symbol,  'parent':version_base_or_id(version)})),
                  key=(itemgetter('segment')))))
            elif blob == _MAGIC_CHUNKED:
                collection = mongoose_lib.get_top_level_collection()
                data = ''.join((x['data'] for x in sorted((collection.find({'symbol':symbol,  'parent':version_base_or_id(version)})),
                  key=(itemgetter('segment')))))
                data = decompress(data)
            elif blob[:len(_MAGIC_CHUNKED)] == _MAGIC_CHUNKED:
                logger.error('Data was written by unsupported version of pickle store for symbol %s. Upgrade Arctic and try again' % symbol)
                raise UnsupportedPickleStoreVersion('Data was written by unsupported version of pickle store')
            try:
                data = decompress(blob)
            except:
                logger.error('Failed to read symbol %s' % symbol)

            if six.PY2:
                return pickle_compat_load(io.BytesIO(data))
            try:
                return pickle_compat_load(io.BytesIO(data))
            except UnicodeDecodeError as ue:
                try:
                    logger.info('Could not Unpickle with ascii, Using latin1.')
                    encoding = kwargs.get('encoding', 'latin_1')
                    return pickle_compat_load((io.BytesIO(data)), encoding=encoding)
                finally:
                    ue = None
                    del ue

        return version['data']

    @staticmethod
    def read_options():
        return []

    def write(self, arctic_lib, version, symbol, item, _previous_version):
        if not SKIP_BSON_ENCODE_PICKLE_STORE:
            try:
                b = bson.BSON.encode({'data': item})
                if len(b) < min(MAX_BSON_ENCODE, _HARD_MAX_BSON_ENCODE):
                    version['data'] = item
                    return
            except InvalidDocument:
                pass

        collection = arctic_lib.get_top_level_collection()
        version['blob'] = _MAGIC_CHUNKEDV2
        pickled = cPickle.dumps(item, protocol=(cPickle.HIGHEST_PROTOCOL))
        data = compress_array([pickled[i * _CHUNK_SIZE:(i + 1) * _CHUNK_SIZE] for i in xrange(int(len(pickled) / _CHUNK_SIZE + 1))])
        for seg, d in enumerate(data):
            segment = {'data': Binary(d)}
            segment['segment'] = seg
            seg += 1
            sha = checksum(symbol, segment)
            collection.update_one({'symbol':symbol,  'sha':sha}, {'$set':segment, 
             '$addToSet':{'parent': version['_id']}},
              upsert=True)