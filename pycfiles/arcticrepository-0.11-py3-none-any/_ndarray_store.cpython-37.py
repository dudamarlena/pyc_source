# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/store/_ndarray_store.py
# Compiled at: 2019-05-18 09:07:34
# Size of source mod 2**32: 36810 bytes
import hashlib, logging
from operator import itemgetter
import numpy as np, pymongo
from bson.binary import Binary
from pymongo.errors import OperationFailure, DuplicateKeyError, BulkWriteError
from six.moves import xrange
from ._version_store_utils import checksum, version_base_or_id, _fast_check_corruption
from .._compression import compress_array, decompress
from .._config import CHECK_CORRUPTION_ON_APPEND, FW_POINTERS_CONFIG_KEY, FW_POINTERS_REFS_KEY, ARCTIC_FORWARD_POINTERS_CFG, ARCTIC_FORWARD_POINTERS_RECONCILE, FwPointersCfg
from .._util import mongo_count, get_fwptr_config
from ..decorators import mongo_retry
from ..exceptions import UnhandledDtypeException, DataIntegrityException
logger = logging.getLogger(__name__)
_CHUNK_SIZE = 2095104
_APPEND_SIZE = 1048576
_APPEND_COUNT = 60

def _promote_struct_dtypes(dtype1, dtype2):
    if not set(dtype1.names).issuperset(set(dtype2.names)):
        raise Exception('Removing columns from dtype not handled')

    def _promote(type1, type2):
        if type2 is None:
            return type1
        if type1.shape is not None:
            if not type1.shape == type2.shape:
                raise Exception('We do not handle changes to dtypes that have shape')
            return (np.promote_types(type1.base, type2.base), type1.shape)
        return np.promote_types(type1, type2)

    return np.dtype([(n, _promote(dtype1.fields[n][0], dtype2.fields.get(n, (None, ))[0])) for n in dtype1.names])


def _attempt_update_unchanged(symbol, unchanged_segment_ids, collection, version, previous_version):
    if not (unchanged_segment_ids and collection and version):
        return
        parent_id = version_base_or_id(version)
        result = collection.update_many({'symbol':symbol, 
         '_id':{'$in': [x['_id'] for x in unchanged_segment_ids]}}, {'$addToSet': {'parent': parent_id}})
        if result.matched_count == len(unchanged_segment_ids):
            return
        unchanged_ids = set([x['_id'] for x in unchanged_segment_ids])
        spec = {'symbol':symbol,  'parent':parent_id, 
         'segment':{'$lte': unchanged_segment_ids[(-1)]['segment']}}
        matched_segments_ids = set([x['_id'] for x in collection.find(spec)])
        if unchanged_ids != matched_segments_ids:
            logger.error('Mismatched unchanged segments for {}: {} != {} (query spec={})'.format(symbol, unchanged_ids, matched_segments_ids, spec))
            raise DataIntegrityException('Symbol: {}:{} update_many updated {} segments instead of {}'.format(symbol, previous_version['version'], result.matched_count, len(unchanged_segment_ids)))


def _resize_with_dtype(arr, dtype):
    """
    This function will transform arr into an array with the same type as dtype. It will do this by
    filling new columns with zeros (or NaNs, if it is a float column). Also, columns that are not
    in the new dtype will be dropped.
    """
    structured_arrays = dtype.names is not None and arr.dtype.names is not None
    old_columns = arr.dtype.names or 
    new_columns = dtype.names or 
    if structured_arrays:
        if old_columns != new_columns:
            old_columns = set(old_columns)
            new_columns = set(new_columns)
            new_arr = np.zeros(arr.shape, dtype)
            for c in old_columns & new_columns:
                new_arr[c] = arr[c]

            _is_float_type = lambda _dtype: _dtype.type in (np.float32, np.float64)
            _is_void_float_type = lambda _dtype: _dtype.type == np.void and _is_float_type(_dtype.subdtype[0])
            _is_float_or_void_float_type = lambda _dtype: _is_float_type(_dtype) or 
            _is_float = lambda column: _is_float_or_void_float_type(dtype.fields[column][0])
            for new_column in filter(_is_float, new_columns - old_columns):
                new_arr[new_column] = np.nan

            return new_arr.astype(dtype)
    return arr.astype(dtype)


def set_corruption_check_on_append(enable):
    global CHECK_CORRUPTION_ON_APPEND
    CHECK_CORRUPTION_ON_APPEND = bool(enable)


def _update_fw_pointers(collection, symbol, version, previous_version, is_append, shas_to_add=None):
    """
    This function will decide whether to update the version document with forward pointers to segments.
    It detects cases where no prior writes/appends have been performed with FW pointers, and extracts the segment IDs.
    It also sets the metadata which indicate the mode of operation at the time of the version creation.
    """
    version[FW_POINTERS_CONFIG_KEY] = ARCTIC_FORWARD_POINTERS_CFG.name
    if ARCTIC_FORWARD_POINTERS_CFG is FwPointersCfg.DISABLED:
        return
        version_shas = set()
        if is_append:
            prev_fw_cfg = get_fwptr_config(previous_version)
            if prev_fw_cfg is FwPointersCfg.DISABLED.name:
                version_shas.update((Binary(sha) for sha in collection.find({'symbol':symbol, 
                 'parent':version_base_or_id(previous_version), 
                 'segment':{'$lt': previous_version['up_to']}}, {'sha': 1})))
    else:
        version_shas.update(previous_version[FW_POINTERS_REFS_KEY])
    version_shas.update(shas_to_add)
    if len(version_shas) != version['segment_count']:
        raise pymongo.errors.OperationFailure('Mismatched number of forward pointers to segments for {}: {} != {})Is append: {}. Previous version: {}. Gathered forward pointers segment shas: {}.'.format(symbol, len(version_shas), version['segment_count'], is_append, previous_version['_id'], version_shas))
    version[FW_POINTERS_REFS_KEY] = list(version_shas)


def _spec_fw_pointers_aware(symbol, version, from_index=None, to_index=None):
    """
    This method updates the find query filter spec used to read the segment for a version.
    It chooses whether to query via forward pointers or not based on the version details and current mode of operation.
    """
    spec = {'symbol':symbol, 
     'segment':{'$lt': version['up_to'] if to_index is None else to_index}}
    if from_index is not None:
        spec['segment']['$gte'] = from_index
    if FW_POINTERS_CONFIG_KEY not in version or version[FW_POINTERS_CONFIG_KEY] == FwPointersCfg.DISABLED.name:
        spec['parent'] = version_base_or_id(version)
        return spec
    v_fw_config = FwPointersCfg[version[FW_POINTERS_CONFIG_KEY]]
    if v_fw_config is FwPointersCfg.ENABLED:
        if from_index is None:
            if to_index is None:
                del spec['segment']
        spec['sha'] = {'$in': version[FW_POINTERS_REFS_KEY]}
        return spec
    if v_fw_config is FwPointersCfg.HYBRID:
        if ARCTIC_FORWARD_POINTERS_CFG is FwPointersCfg.DISABLED:
            spec['parent'] = version_base_or_id(version)
        else:
            if from_index is None:
                if to_index is None:
                    del spec['segment']
            spec['sha'] = {'$in': version[FW_POINTERS_REFS_KEY]}
        return spec
    raise DataIntegrityException('Unhandled FW pointers configuration ({}: {}/{}/{})'.format(version.get('symbol'), version.get('_id'), version.get('version'), v_fw_config))


def _fw_pointers_convert_append_to_write(previous_version):
    """
    This method decides whether to convert an append to a full write  in order to avoid data integrity errors
    """
    prev_fw_config = get_fwptr_config(previous_version)
    return prev_fw_config is FwPointersCfg.ENABLED and ARCTIC_FORWARD_POINTERS_CFG is not FwPointersCfg.ENABLED


class NdarrayStore(object):
    """NdarrayStore"""
    TYPE = 'ndarray'

    @classmethod
    def initialize_library(cls, *args, **kwargs):
        pass

    @staticmethod
    def _ensure_index(collection):
        try:
            collection.create_index([('symbol', pymongo.HASHED)], background=True)
            collection.create_index([('symbol', pymongo.ASCENDING),
             (
              'sha', pymongo.ASCENDING)],
              unique=True, background=True)
            collection.create_index([('symbol', pymongo.ASCENDING),
             (
              'parent', pymongo.ASCENDING),
             (
              'segment', pymongo.ASCENDING)],
              unique=True, background=True)
            collection.create_index([('symbol', pymongo.ASCENDING),
             (
              'sha', pymongo.ASCENDING),
             (
              'segment', pymongo.ASCENDING)],
              unique=True, background=True)
        except OperationFailure as e:
            try:
                if "can't use unique indexes" in str(e):
                    return
                raise
            finally:
                e = None
                del e

    @mongo_retry
    def can_delete(self, version, symbol):
        return self.can_read(version, symbol)

    def can_read(self, version, symbol):
        return version['type'] == self.TYPE

    @staticmethod
    def can_write_type(data):
        return isinstance(data, np.ndarray)

    def can_write(self, version, symbol, data):
        return self.can_write_type(data) and not data.dtype.hasobject

    def _dtype(self, string, metadata=None):
        if metadata is None:
            metadata = {}
        if string.startswith('['):
            return np.dtype((eval(string)), metadata=metadata)
        return np.dtype(string, metadata=metadata)

    def _index_range(self, version, symbol, from_version=None, **kwargs):
        """
        Tuple describing range to read from the ndarray - closed:open
        """
        from_index = None
        if from_version:
            from_index = from_version['up_to']
        return (from_index, None)

    def get_info(self, version):
        ret = {}
        dtype = self._dtype(version['dtype'], version.get('dtype_metadata', {}))
        length = int(version['up_to'])
        ret['size'] = dtype.itemsize * length
        ret['segment_count'] = version['segment_count']
        ret['dtype'] = version['dtype']
        ret['type'] = version['type']
        ret['handler'] = self.__class__.__name__
        ret['rows'] = int(version['up_to'])
        return ret

    @staticmethod
    def read_options():
        return [
         'from_version']

    def read(self, arctic_lib, version, symbol, read_preference=None, **kwargs):
        index_range = (self._index_range)(version, symbol, **kwargs)
        collection = arctic_lib.get_top_level_collection()
        if read_preference:
            collection = collection.with_options(read_preference=read_preference)
        return self._do_read(collection, version, symbol, index_range=index_range)

    def _do_read(self, collection, version, symbol, index_range=None):
        """
        index_range is a 2-tuple of integers - a [from, to) range of segments to be read.
            Either from or to can be None, indicating no bound.
        """
        from_index = index_range[0] if index_range else None
        to_index = version['up_to']
        if index_range:
            if index_range[1]:
                if index_range[1] < version['up_to']:
                    to_index = index_range[1]
        segment_count = version.get('segment_count') if from_index is None else None
        spec = _spec_fw_pointers_aware(symbol, version, from_index, to_index)
        data = bytearray()
        i = -1
        for i, x in enumerate(sorted((collection.find(spec)), key=(itemgetter('segment')))):
            data.extend(decompress(x['data']) if x['compressed'] else x['data'])

        if segment_count is not None:
            if i + 1 != segment_count:
                raise OperationFailure('Incorrect number of segments returned for {}:{}.  Expected: {}, but got {}. {}'.format(symbol, version['version'], segment_count, i + 1, collection.database.name + '.' + collection.name))
        dtype = self._dtype(version['dtype'], version.get('dtype_metadata', {}))
        rtn = np.frombuffer(data, dtype=dtype).reshape(version.get('shape', -1))
        return rtn

    def _promote_types(self, dtype, dtype_str):
        if dtype_str == str(dtype):
            return dtype
        else:
            prev_dtype = self._dtype(dtype_str)
            if dtype.names is None:
                rtn = np.promote_types(dtype, prev_dtype)
            else:
                rtn = _promote_struct_dtypes(dtype, prev_dtype)
        rtn = np.dtype(rtn, metadata=(dict(dtype.metadata or )))
        return rtn

    def append(self, arctic_lib, version, symbol, item, previous_version, dtype=None, dirty_append=True):
        collection = arctic_lib.get_top_level_collection()
        if previous_version.get('shape', [-1]) != [-1] + list(item.shape)[1:]:
            raise UnhandledDtypeException()
        elif not dtype:
            dtype = item.dtype
        else:
            if (self._dtype(previous_version['dtype']).fields is None) != (dtype.fields is None):
                raise ValueError('type changes to or from structured array not supported')
            if previous_version['up_to'] == 0:
                dtype = dtype
            elif len(item) == 0:
                dtype = self._dtype(previous_version['dtype'])
            else:
                dtype = self._promote_types(dtype, previous_version['dtype'])
        item = item.astype(dtype)
        version['type'] = self.TYPE
        version[FW_POINTERS_CONFIG_KEY] = ARCTIC_FORWARD_POINTERS_CFG.name
        if version[FW_POINTERS_CONFIG_KEY] != FwPointersCfg.DISABLED.name:
            version[FW_POINTERS_REFS_KEY] = list()
        if str(dtype) != previous_version['dtype'] or _fw_pointers_convert_append_to_write(previous_version):
            logger.debug('Converting %s from %s to %s' % (symbol, previous_version['dtype'], str(dtype)))
            if item.dtype.hasobject:
                raise UnhandledDtypeException()
            version['dtype'] = str(dtype)
            version['dtype_metadata'] = dict(dtype.metadata or )
            old_arr = _resize_with_dtype(self._do_read(collection, previous_version, symbol), dtype)
            item = np.concatenate([old_arr, item])
            version['up_to'] = len(item)
            version['sha'] = self.checksum(item)
            version['base_sha'] = version['sha']
            self._do_write(collection, version, symbol, item, previous_version)
        else:
            version['dtype'] = previous_version['dtype']
            version['dtype_metadata'] = previous_version['dtype_metadata']
            if CHECK_CORRUPTION_ON_APPEND:
                if _fast_check_corruption(collection,
                  symbol, previous_version, check_count=False,
                  check_last_segment=True,
                  check_append_safe=True):
                    logging.warning('Found mismatched segments for {} (version={}). Converting append to concat and rewrite'.format(symbol, previous_version['version']))
                    dirty_append = True
            self._do_append(collection, version, symbol, item, previous_version, dirty_append)

    def _do_append(self, collection, version, symbol, item, previous_version, dirty_append):
        data = item.tostring()
        version['base_sha'] = previous_version.get('base_sha', Binary(''))
        version['up_to'] = previous_version['up_to'] + len(item)
        if len(item) > 0:
            version['segment_count'] = previous_version['segment_count'] + 1
            version['append_count'] = previous_version['append_count'] + 1
            version['append_size'] = previous_version['append_size'] + len(data)
        else:
            version['segment_count'] = previous_version['segment_count']
            version['append_count'] = previous_version['append_count']
            version['append_size'] = previous_version['append_size']
        if not dirty_append:
            if version['append_count'] < _APPEND_COUNT:
                if version['append_size'] < _APPEND_SIZE:
                    version['base_version_id'] = version_base_or_id(previous_version)
                    if len(item) > 0:
                        segment = {'data':Binary(data), 
                         'compressed':False,  'segment':version['up_to'] - 1}
                        sha = checksum(symbol, segment)
                        try:
                            if ARCTIC_FORWARD_POINTERS_CFG is FwPointersCfg.DISABLED:
                                collection.update_one({'symbol':symbol, 
                                 'sha':sha},
                                  {'$set':segment, 
                                 '$addToSet':{'parent': version['base_version_id']}},
                                  upsert=True)
                            else:
                                set_spec = {'$set': segment}
                                if ARCTIC_FORWARD_POINTERS_CFG is FwPointersCfg.HYBRID:
                                    set_spec['$addToSet'] = {'parent': version['base_version_id']}
                                else:
                                    set_spec['$addToSet'] = {'parent': version['_id']}
                                collection.update_one({'symbol':symbol,  'sha':sha}, set_spec, upsert=True)
                                _update_fw_pointers(collection, symbol, version, previous_version, is_append=True, shas_to_add=(
                                 sha,))
                        except DuplicateKeyError:
                            self._concat_and_rewrite(collection, version, symbol, item, previous_version)
                            return
                        else:
                            if 'segment_index' in previous_version:
                                segment_index = self._segment_index(item, existing_index=(previous_version.get('segment_index')),
                                  start=(previous_version['up_to']),
                                  new_segments=[
                                 segment['segment']])
                                if segment_index:
                                    version['segment_index'] = segment_index
                            logger.debug('Appended segment %d for parent %s' % (segment['segment'], version['_id']))
                elif 'segment_index' in previous_version:
                    version['segment_index'] = previous_version['segment_index']
        else:
            self._concat_and_rewrite(collection, version, symbol, item, previous_version)

    def _concat_and_rewrite(self, collection, version, symbol, item, previous_version):
        version.pop('base_version_id', None)
        spec = _spec_fw_pointers_aware(symbol, previous_version)
        read_index_range = [
         0, None]
        unchanged_segments = []
        for segment in sorted(collection.find(spec, projection={'_id':1,  'segment':1,  'compressed':1,  'sha':1}), key=(itemgetter('segment'))):
            if not segment['compressed']:
                if unchanged_segments:
                    unchanged_segments.pop()
                break
            unchanged_segments.append(segment)

        if len(unchanged_segments) < previous_version['segment_count'] - previous_version['append_count'] - 1:
            raise DataIntegrityException('Symbol: %s:%s expected %s segments but found %s' % (
             symbol, previous_version['version'],
             previous_version['segment_count'] - previous_version['append_count'] - 1,
             len(unchanged_segments)))
        elif unchanged_segments:
            read_index_range[0] = unchanged_segments[(-1)]['segment'] + 1
        else:
            old_arr = self._do_read(collection, previous_version, symbol, index_range=read_index_range)
            if len(item) == 0:
                logger.debug('Rewrite and compress/chunk item %s, rewrote old_arr' % symbol)
                self._do_write(collection, version, symbol, old_arr, previous_version, segment_offset=(read_index_range[0]))
            elif len(old_arr) == 0:
                logger.debug('Rewrite and compress/chunk item %s, wrote item' % symbol)
                self._do_write(collection, version, symbol, item, previous_version, segment_offset=(read_index_range[0]))
            else:
                logger.debug('Rewrite and compress/chunk %s, np.concatenate %s to %s' % (symbol,
                 item.dtype, old_arr.dtype))
                self._do_write(collection, version, symbol, (np.concatenate([old_arr, item])), previous_version, segment_offset=(read_index_range[0]))
        if unchanged_segments:
            if version.get(FW_POINTERS_CONFIG_KEY) != FwPointersCfg.ENABLED.name:
                _attempt_update_unchanged(symbol, unchanged_segments, collection, version, previous_version)
            version['segment_count'] += len(unchanged_segments)
            _update_fw_pointers(collection,
              symbol, version, previous_version, is_append=False, shas_to_add=(version.get(FW_POINTERS_REFS_KEY, []) + [s['sha'] for s in unchanged_segments]))
            self.check_written(collection, symbol, version)

    @staticmethod
    def check_written(collection, symbol, version):
        parent_id = version_base_or_id(version)
        if version.get(FW_POINTERS_CONFIG_KEY) == FwPointersCfg.DISABLED.name:
            spec = {'symbol':symbol, 
             'parent':parent_id}
        else:
            spec = {'symbol':symbol, 
             'sha':{'$in': version[FW_POINTERS_REFS_KEY]}}
        seen_chunks = mongo_count(collection, filter=spec)
        if seen_chunks != version['segment_count']:
            raise pymongo.errors.OperationFailure('Failed to write all the chunks. Saw %s expecting %s. Parent: %s. Segments: %s' % (
             seen_chunks, version['segment_count'], parent_id,
             list(collection.find(spec, projection={'_id':1,  'segment':1}))))
        if version.get(FW_POINTERS_CONFIG_KEY) == FwPointersCfg.HYBRID.name:
            if ARCTIC_FORWARD_POINTERS_RECONCILE:
                seen_chunks_reverse_pointers = mongo_count(collection, filter={'symbol':symbol,  'parent':parent_id})
                if seen_chunks != seen_chunks_reverse_pointers:
                    raise pymongo.errors.OperationFailure('Failed to reconcile forward pointer chunks ({}). Parent {}. Reverse pointers segments #: {}. Forward pointers segments #: {}.'.format(symbol, parent_id, seen_chunks_reverse_pointers, seen_chunks))

    def checksum(self, item):
        sha = hashlib.sha1()
        sha.update(item.tostring())
        return Binary(sha.digest())

    def write(self, arctic_lib, version, symbol, item, previous_version, dtype=None):
        collection = arctic_lib.get_top_level_collection()
        if item.dtype.hasobject:
            raise UnhandledDtypeException()
        if not dtype:
            dtype = item.dtype
        version['dtype'] = str(dtype)
        version['shape'] = (-1, ) + item.shape[1:]
        version['dtype_metadata'] = dict(dtype.metadata or )
        version['type'] = self.TYPE
        version['up_to'] = len(item)
        version['sha'] = self.checksum(item)
        version[FW_POINTERS_CONFIG_KEY] = ARCTIC_FORWARD_POINTERS_CFG.name
        if version[FW_POINTERS_CONFIG_KEY] != FwPointersCfg.DISABLED.name:
            version[FW_POINTERS_REFS_KEY] = list()
        if previous_version:
            if 'sha' in previous_version:
                if previous_version['dtype'] == version['dtype']:
                    if self.checksum(item[:previous_version['up_to']]) == previous_version['sha']:
                        self._do_append(collection, version, symbol, (item[previous_version['up_to']:]), previous_version, dirty_append=True)
                        return
        version['base_sha'] = version['sha']
        self._do_write(collection, version, symbol, item, previous_version)

    def _do_write(self, collection, version, symbol, item, previous_version, segment_offset=0):
        row_size = int(item.dtype.itemsize * np.prod(item.shape[1:]))
        rows_per_chunk = int(_CHUNK_SIZE / row_size)
        symbol_all_previous_shas, version_shas = set(), set()
        if previous_version:
            symbol_all_previous_shas.update((Binary(x['sha']) for x in collection.find({'symbol': symbol}, projection={'sha':1,  '_id':0})))
        length = len(item)
        if segment_offset > 0 and 'segment_index' in previous_version:
            existing_index = previous_version['segment_index']
        else:
            existing_index = None
        segment_index = []
        idxs = xrange(int(np.ceil(float(length) / rows_per_chunk)))
        chunks = [item[i * rows_per_chunk:(i + 1) * rows_per_chunk].tostring() for i in idxs]
        compressed_chunks = compress_array(chunks)
        bulk = []
        for i, chunk in zip(idxs, compressed_chunks):
            segment = {'data':Binary(chunk), 
             'compressed':True, 
             'segment':min((i + 1) * rows_per_chunk - 1, length - 1) + segment_offset}
            segment_index.append(segment['segment'])
            sha = checksum(symbol, segment)
            segment_spec = {'symbol':symbol,  'sha':sha,  'segment':segment['segment']}
            if ARCTIC_FORWARD_POINTERS_CFG is FwPointersCfg.DISABLED:
                if sha not in symbol_all_previous_shas:
                    segment['sha'] = sha
                    bulk.append(pymongo.UpdateOne(segment_spec, {'$set':segment, 
                     '$addToSet':{'parent': version['_id']}},
                      upsert=True))
                else:
                    bulk.append(pymongo.UpdateOne(segment_spec, {'$addToSet': {'parent': version['_id']}}))
            else:
                version_shas.add(sha)
                set_spec = {'$addToSet': {'parent': version['_id']}}
                if sha not in symbol_all_previous_shas:
                    segment['sha'] = sha
                    set_spec['$set'] = segment
                    bulk.append(pymongo.UpdateOne(segment_spec, set_spec, upsert=True))
                elif ARCTIC_FORWARD_POINTERS_CFG is FwPointersCfg.HYBRID:
                    bulk.append(pymongo.UpdateOne(segment_spec, set_spec))

        if bulk:
            try:
                collection.bulk_write(bulk, ordered=False)
            except BulkWriteError as bwe:
                try:
                    logger.error('Bulk write failed with details: %s (Exception: %s)' % (bwe.details, bwe))
                    raise
                finally:
                    bwe = None
                    del bwe

        segment_index = self._segment_index(item, existing_index=existing_index, start=segment_offset, new_segments=segment_index)
        if segment_index:
            version['segment_index'] = segment_index
        version['segment_count'] = len(chunks)
        version['append_size'] = 0
        version['append_count'] = 0
        _update_fw_pointers(collection, symbol, version, previous_version, is_append=False, shas_to_add=version_shas)
        self.check_written(collection, symbol, version)

    def _segment_index(self, new_data, existing_index, start, new_segments):
        """
        Generate a segment index which can be used in subselect data in _index_range.
        This function must handle both generation of the index and appending to an existing index

        Parameters:
        -----------
        new_data: new data being written (or appended)
        existing_index: index field from the versions document of the previous version
        start: first (0-based) offset of the new data
        segments: list of offsets. Each offset is the row index of the
                  the last row of a particular chunk relative to the start of the _original_ item.
                  array(new_data) - segments = array(offsets in item)

        Returns:
        --------
        Library specific index metadata to be stored in the version document.
        """
        pass