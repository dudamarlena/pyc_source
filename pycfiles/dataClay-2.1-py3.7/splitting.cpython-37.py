# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/contrib/splitting.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 11731 bytes
""" Class description goes here. """
from dataclay import StorageObject
from dataclay import dclayMethod
import logging
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2016 Barcelona Supercomputing Center (BSC-CNS)'
CLASSES_TO_REGISTER = ('GenericSplit', 'WorkStealingSplit', 'WorkMovingSplit')
logger = logging.getLogger(__name__)

def split(iterable, **split_options):
    """Perform a split on iterable.

    This method is highly inspired in the `iter` global method (in conjunction
    with its __iter__ counterpart method) for iterable classes.

    :param iterable: An iterable, which will typically be a Storage<Collection>
    :param split_options: The optional additional arguments to the split method.
    May be ignored.
    :return: A collection of Split, or something similar. If iterable is not a
    Storage<Collection>, returns a tuple with a single element, the iterable
    argument itself
    """
    try:
        return (iterable.split)(**split_options)
    except AttributeError:
        return (
         iterable,)


class GenericSplit(StorageObject):
    __doc__ = 'Iterator to chain several chunks.\n\n    @ClassField _chunks list<storageobject>\n    @ClassField split_brothers list<storageobject>\n    @ClassField storage_location anything\n    @ClassField _current_chunk_idx int\n    @ClassField _last_chunk_idx int\n    '

    @dclayMethod(chunks='list<storageobject>', storage_location='anything')
    def __init__(self, chunks, storage_location):
        """Build a LocalIterator through a list of chunks.

        :param chunks: Sequence of (iterable) chunks.
        """
        self._chunks = list(chunks)
        self.storage_location = storage_location
        self.split_brothers = list()
        self._current_chunk_idx = -1
        self._last_chunk_idx = -1
        self._current_iter_chunk = None

    @dclayMethod(return_=bool, _local=True)
    def _go_next_chunk(self):
        """Advance to next chunk.

        Prepare the internal chunk iterator. This is typically called when the
        current chunk iterator has finished. Return True if everything is ok,
        False if there is no valid next chunk.

        :return bool: Whether the advance is a success
        """
        self._current_chunk_idx += 1
        if self._current_chunk_idx < self._last_chunk_idx:
            self._current_iter_chunk = iter(self._chunks[self._current_chunk_idx])
            return True
        return False

    @dclayMethod(_local=True)
    def __next__(self):
        try:
            return next(self._current_iter_chunk)
        except StopIteration:
            logger.info('Iterator %s passing the chunk_idx %d', self.getID(), self._current_chunk_idx)

        if self._go_next_chunk():
            return next(self)
        raise StopIteration

    @dclayMethod(_local=True)
    def next(self):
        return self.__next__()

    @dclayMethod()
    def _remote_iteration_init(self):
        """This method is used for remote initialization.

        This registered method is used by the local-execution `__iter__`. Given
        that that method is _local, a certain remote initialization must be
        ensured in order for the iteration to work smoothly.
        """
        self._current_chunk_idx = 0 if self._chunks else -1
        self._last_chunk_idx = len(self._chunks)

    @dclayMethod(return_='anything', _local=True)
    def __iter__(self):
        self._remote_iteration_init()
        if self._chunks:
            self._current_iter_chunk = iter(self._chunks[0])
        else:
            self._current_iter_chunk = iter(list())
        return self


class WorkStealingSplit(GenericSplit):
    __doc__ = 'Iterator to chain several chunks with simple Work Stealing addendum.\n\n    The Work Stealing performed by this split is a simple one in which the\n    chunk is returned to the thief, but no modifications are done (no movement,\n    no reorganization of objects).\n\n    @ClassField _chunks list<storageobject>\n    @ClassField split_brothers list<storageobject>\n    @ClassField storage_location anything\n    @ClassField _current_chunk_idx int\n    @ClassField _last_chunk_idx int\n    '

    @dclayMethod(stolen_object='storageobject', return_='storageobject')
    def _post_stealing(self, stolen_object):
        """Not used by the simple base class WorkStealingSplit."""
        return stolen_object

    @dclayMethod(return_='storageobject')
    def steal_me(self):
        if self._current_chunk_idx < self._last_chunk_idx - 2:
            self._last_chunk_idx -= 1
            return self._chunks[self._last_chunk_idx]
        return

    @dclayMethod(_local=True)
    def __next__(self):
        try:
            return next(self._current_iter_chunk)
        except StopIteration:
            logger.info('Iterator %s passing the chunk_idx %d', self.getID(), self._current_chunk_idx)

        if self._go_next_chunk():
            return next(self)
        import random
        brothers = self.split_brothers
        while 1:
            if brothers:
                logger.info('Trying a brother...')
                victim_idx = random.randint(0, len(brothers) - 1)
                steal = brothers[victim_idx].steal_me()
                if steal is None:
                    logger.info('Split method could not steal from brother, removing')
                    brothers.pop(victim_idx)
                else:
                    logger.info('received %r', steal)
                    chunk_to_use = self._post_stealing(steal)
                    logger.info('using %r', chunk_to_use)
                    self._current_iter_chunk = iter(chunk_to_use)
                    break
        else:
            logger.info('No valid targets to steal')
            raise StopIteration

        self.split_brothers = brothers
        return next(self)


class WorkMovingSplit(WorkStealingSplit):
    __doc__ = 'Iterator to chain several chunks with Work Stealing through movement.\n\n    The balancing performed by this split is similar to the simple Work Stealing\n    but in this scenario the chunks are reorganized through movement. When there\n    is a steal, the chunk is "physically" moved to the receiving end.\n\n    @ClassField _chunks list<storageobject>\n    @ClassField split_brothers list<storageobject>\n    @ClassField storage_location anything\n    @ClassField _current_chunk_idx int\n    @ClassField _last_chunk_idx int\n    '

    @dclayMethod(stolen_object='storageobject', return_='storageobject')
    def _post_stealing(self, stolen_object):
        """Once an object has been stolen, perform the movement."""
        from dataclay.commonruntime.Runtime import getRuntime
        from dataclay.commonruntime.Settings import settings
        getRuntime().move_object(stolen_object, settings.storage_id)
        return stolen_object


class SplittableCollectionMixin(object):
    __doc__ = 'Mixin to help the model programmer.\n\n    This mixin is intended to be use with Collections that have "chunks" (or\n    some kind of internal partitioning) and desire to use them to provide high\n    level "split iteration" abstractions.\n\n    To provide support for SplittableCollections, include a get_chunks method\n    which must return the list of chunks. Note that each chunk must have an\n    iteration mechanism, with an structure that should resemble the original\n    collection.\n    '

    @dclayMethod(return_='anything')
    def get_chunks(self):
        try:
            return self.chunks
        except AttributeError:
            raise NotImplementedError('ChunkedCollections must either implement the get_chunks method or contain a `chunks` attribute.')

    @dclayMethod(return_='list<storageobject>', split_class='anything', _local=True)
    def split--- This code section failed: ---

 L. 247         0  LOAD_CONST               0
                2  LOAD_CONST               ('getRuntime',)
                4  IMPORT_NAME_ATTR         dataclay.commonruntime.Runtime
                6  IMPORT_FROM              getRuntime
                8  STORE_DEREF              'getRuntime'
               10  POP_TOP          

 L. 248        12  LOAD_GLOBAL              sorted

 L. 249        14  LOAD_CLOSURE             'getRuntime'
               16  BUILD_TUPLE_1         1 
               18  LOAD_GENEXPR             '<code_object <genexpr>>'
               20  LOAD_STR                 'SplittableCollectionMixin.split.<locals>.<genexpr>'
               22  MAKE_FUNCTION_8          'closure'

 L. 254        24  LOAD_FAST                'self'
               26  LOAD_METHOD              get_chunks
               28  CALL_METHOD_0         0  '0 positional arguments'
               30  GET_ITER         
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  STORE_FAST               'location_chunks'

 L. 257        38  LOAD_GLOBAL              list
               40  CALL_FUNCTION_0       0  '0 positional arguments'
               42  STORE_FAST               'result'

 L. 260        44  LOAD_CONST               0
               46  LOAD_CONST               ('groupby',)
               48  IMPORT_NAME              itertools
               50  IMPORT_FROM              groupby
               52  STORE_FAST               'groupby'
               54  POP_TOP          

 L. 261        56  LOAD_CONST               0
               58  LOAD_CONST               ('itemgetter',)
               60  IMPORT_NAME              operator
               62  IMPORT_FROM              itemgetter
               64  STORE_FAST               'itemgetter'
               66  POP_TOP          

 L. 262        68  LOAD_CONST               0
               70  LOAD_CONST               ('splitting',)
               72  IMPORT_NAME_ATTR         dataclay.contrib
               74  IMPORT_FROM              splitting
               76  STORE_FAST               'splitting'
               78  POP_TOP          

 L. 264        80  LOAD_FAST                'split_class'
               82  LOAD_CONST               None
               84  COMPARE_OP               is
               86  POP_JUMP_IF_FALSE    96  'to 96'

 L. 265        88  LOAD_FAST                'splitting'
               90  LOAD_ATTR                GenericSplit
               92  STORE_FAST               'split_class'
               94  JUMP_FORWARD        138  'to 138'
             96_0  COME_FROM            86  '86'

 L. 266        96  LOAD_GLOBAL              isinstance
               98  LOAD_FAST                'split_class'
              100  LOAD_GLOBAL              basestring
              102  CALL_FUNCTION_2       2  '2 positional arguments'
              104  POP_JUMP_IF_FALSE   118  'to 118'

 L. 267       106  LOAD_GLOBAL              getattr
              108  LOAD_FAST                'splitting'
              110  LOAD_FAST                'split_class'
              112  CALL_FUNCTION_2       2  '2 positional arguments'
              114  STORE_FAST               'split_class'
              116  JUMP_FORWARD        138  'to 138'
            118_0  COME_FROM           104  '104'

 L. 269       118  LOAD_GLOBAL              NotImplementedError
              120  LOAD_STR                 'I could not understand %s (of type %s)'

 L. 270       122  LOAD_FAST                'split_class'
              124  LOAD_GLOBAL              type
              126  LOAD_FAST                'split_class'
              128  CALL_FUNCTION_1       1  '1 positional argument'
              130  BUILD_TUPLE_2         2 
              132  BINARY_MODULO    
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  RAISE_VARARGS_1       1  'exception instance'
            138_0  COME_FROM           116  '116'
            138_1  COME_FROM            94  '94'

 L. 272       138  LOAD_GLOBAL              set
              140  LOAD_DEREF               'getRuntime'
              142  CALL_FUNCTION_0       0  '0 positional arguments'
              144  LOAD_METHOD              get_execution_environments_info
              146  CALL_METHOD_0         0  '0 positional arguments'
              148  LOAD_METHOD              keys
              150  CALL_METHOD_0         0  '0 positional arguments'
              152  CALL_FUNCTION_1       1  '1 positional argument'
              154  STORE_FAST               'unused_exec_envs'

 L. 278       156  SETUP_LOOP          206  'to 206'
              158  LOAD_FAST                'groupby'
              160  LOAD_FAST                'location_chunks'
              162  LOAD_FAST                'itemgetter'
              164  LOAD_CONST               0
              166  CALL_FUNCTION_1       1  '1 positional argument'
              168  LOAD_CONST               ('key',)
              170  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              172  GET_ITER         
              174  FOR_ITER            204  'to 204'
              176  UNPACK_SEQUENCE_2     2 
              178  STORE_FAST               'loc'
              180  STORE_FAST               'chunks'

 L. 286       182  LOAD_FAST                'result'
              184  LOAD_METHOD              append
              186  LOAD_GLOBAL              map
              188  LOAD_FAST                'itemgetter'
              190  LOAD_CONST               1
              192  CALL_FUNCTION_1       1  '1 positional argument'
              194  LOAD_FAST                'chunks'
              196  CALL_FUNCTION_2       2  '2 positional arguments'
              198  CALL_METHOD_1         1  '1 positional argument'
              200  POP_TOP          
              202  JUMP_BACK           174  'to 174'
              204  POP_BLOCK        
            206_0  COME_FROM_LOOP      156  '156'

 L. 289       206  LOAD_FAST                'result'
              208  RETURN_VALUE     

 L. 292       210  FOR_ITER            250  'to 250'
              212  STORE_FAST               'ee'

 L. 293       214  LOAD_FAST                'split_class'
              216  LOAD_GLOBAL              list
              218  CALL_FUNCTION_0       0  '0 positional arguments'
              220  LOAD_FAST                'ee'
              222  CALL_FUNCTION_2       2  '2 positional arguments'
              224  STORE_FAST               'split_object'

 L. 294       226  LOAD_FAST                'split_object'
              228  LOAD_ATTR                make_persistent
              230  LOAD_FAST                'ee'
              232  LOAD_CONST               ('backend_id',)
              234  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              236  POP_TOP          

 L. 295       238  LOAD_FAST                'result'
              240  LOAD_METHOD              append
              242  LOAD_FAST                'split_object'
              244  CALL_METHOD_1         1  '1 positional argument'
              246  POP_TOP          
              248  JUMP_BACK           210  'to 210'
              250  POP_BLOCK        

 L. 297       252  SETUP_LOOP          274  'to 274'
              254  LOAD_FAST                'result'
              256  GET_ITER         
              258  FOR_ITER            272  'to 272'
              260  STORE_FAST               'split_object'

 L. 300       262  LOAD_FAST                'result'
              264  LOAD_FAST                'split_object'
              266  STORE_ATTR               split_brothers
          268_270  JUMP_BACK           258  'to 258'
              272  POP_BLOCK        
            274_0  COME_FROM_LOOP      252  '252'

 L. 302       274  LOAD_FAST                'result'
              276  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `FOR_ITER' instruction at offset 210