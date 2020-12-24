# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/env/lib/python3.5/site-packages/idb/fileformat.py
# Compiled at: 2017-12-10 19:15:14
# Size of source mod 2**32: 37938 bytes
"""
lots of inspiration from: https://github.com/nlitsme/pyidbutil
"""
import abc, zlib, struct, logging, functools
from collections import namedtuple
import vstruct
from vstruct.primitives import v_bytes
from vstruct.primitives import v_uint8
from vstruct.primitives import v_uint16
from vstruct.primitives import v_uint32
from vstruct.primitives import v_uint64
import idb, idb.netnode
logger = logging.getLogger(__name__)

class FileHeader(vstruct.VStruct):

    def __init__(self):
        vstruct.VStruct.__init__(self)
        self.offsets = []
        self.checksums = []
        self.signature = v_bytes(size=4)
        self.unk04 = v_uint16()
        self.offset1 = v_uint64()
        self.offset2 = v_uint64()
        self.unk16 = v_uint32()
        self.sig2 = v_uint32()
        self.version = v_uint16()
        self.offset3 = v_uint64()
        self.offset4 = v_uint64()
        self.offset5 = v_uint64()
        self.checksum1 = v_uint32()
        self.checksum2 = v_uint32()
        self.checksum3 = v_uint32()
        self.checksum4 = v_uint32()
        self.checksum5 = v_uint32()
        self.offset6 = v_uint64()
        self.checksum6 = v_uint32()

    def pcb_version(self):
        if self.version != 6:
            raise NotImplementedError('unsupported version: %d' % self.version)

    def pcb_offset6(self):
        self.offsets.append(self.offset1)
        self.offsets.append(self.offset2)
        self.offsets.append(self.offset3)
        self.offsets.append(self.offset4)
        self.offsets.append(self.offset5)
        self.offsets.append(self.offset6)

    def pcb_checksum6(self):
        self.checksums.append(self.checksum1)
        self.checksums.append(self.checksum2)
        self.checksums.append(self.checksum3)
        self.checksums.append(self.checksum4)
        self.checksums.append(self.checksum5)
        self.checksums.append(self.checksum6)

    def validate(self):
        if self.signature not in (b'IDA1', b'IDA2'):
            raise ValueError('bad signature')
        if self.sig2 != 2864434397:
            raise ValueError('bad sig2')
        if self.version != 6:
            raise ValueError('unsupported version')
        return True


class COMPRESSION_METHOD:
    NONE = 0
    ZLIB = 2


class SectionHeader(vstruct.VStruct):

    def __init__(self):
        vstruct.VStruct.__init__(self)
        self.compression_method = v_uint8()
        self.length = v_uint64()
        self.is_compressed = False

    def pcb_compression_method(self):
        if self.compression_method == COMPRESSION_METHOD.NONE:
            self.is_compressed = False
        else:
            self.is_compressed = True


class Section(vstruct.VStruct):

    def __init__(self):
        vstruct.VStruct.__init__(self)
        self.header = SectionHeader()
        self._contents = v_bytes()
        self.contents = b''

    def vsEmit(self, **kwargs):
        if self.header.is_compressed:
            raise NotImplementedError('Section may not be serialized because it was compressed')
        vstruct.VStruct.vsEmit(self, **kwargs)

    def pcb_header(self):
        self['_contents'].vsSetLength(self.header.length)

    def pcb__contents(self):
        if not self.header.is_compressed:
            self.contents = self._contents
        else:
            self.contents = zlib.decompress(self._contents)
            logger.debug('decompressed parsed section.')

    def validate(self):
        if self.header.length == 0:
            raise ValueError('zero size')
        return True


SIZEOF_ENTRY = 6

class BranchEntryPointer(vstruct.VStruct):

    def __init__(self):
        vstruct.VStruct.__init__(self)
        self.page = v_uint32()
        self.offset = v_uint16()


class BranchEntry(vstruct.VStruct):

    def __init__(self, page):
        vstruct.VStruct.__init__(self)
        self.page = page
        self.key_length = v_uint16()
        self.key = v_bytes()
        self.value_length = v_uint16()
        self.value = v_bytes()

    def pcb_key_length(self):
        self['key'].vsSetLength(self.key_length)

    def pcb_value_length(self):
        self['value'].vsSetLength(self.value_length)


class LeafEntryPointer(vstruct.VStruct):

    def __init__(self):
        vstruct.VStruct.__init__(self)
        self.common_prefix = v_uint16()
        self.unk02 = v_uint16()
        self.offset = v_uint16()


class LeafEntry(vstruct.VStruct):

    def __init__(self, key, common_prefix):
        vstruct.VStruct.__init__(self)
        self.pkey = key
        self.common_prefix = common_prefix
        self.key_length = v_uint16()
        self._key = v_bytes()
        self.value_length = v_uint16()
        self.value = v_bytes()
        self.key = None

    def pcb_key_length(self):
        self['_key'].vsSetLength(self.key_length)

    def pcb_value_length(self):
        self['value'].vsSetLength(self.value_length)

    def pcb__key(self):
        self.key = self.pkey[:self.common_prefix] + self._key


class Page(vstruct.VStruct):
    __doc__ = '\n    single node in the b-tree.\n    has a bunch of key-value entries that may point to other pages.\n    binary search these keys and traverse pointers to efficienty query the index.\n\n    branch node::\n\n                                      +-------------+\n        +-----------------------------+ ppointer    |  ----> [ node with keys less than entry1.key]\n        | entry1.key | entry1.value   |-------------+\n        +-----------------------------+ entry1.page |  ----> [ node with entry1.key < X < entry2.key]\n        | entry2.key | entry2.value   |-------------+\n        +-----------------------------+ entry2.page |  ----> [ node with entry2.key < X < entry3.key]\n        | ...        | ...            |-------------+\n        +-----------------------------+ ...         |\n        | entryN.key | entryN.value   |-------------+\n        +-----------------------------+ entryN.key  |  ----> [ node with keys greater than entryN.key]\n                                      +-------------+\n\n    leaf node::\n\n        +-----------------------------+\n        | entry1.key | entry1.value   |\n        +-----------------------------+\n        | entry2.key | entry2.value   |\n        +-----------------------------+\n        | ...        | ...            |\n        +-----------------------------+\n        | entryN.key | entryN.value   |\n        +-----------------------------+\n\n    '

    def __init__(self, page_size, page_number):
        vstruct.VStruct.__init__(self)
        self.page_number = page_number
        self.ppointer = v_uint32()
        self.entry_count = v_uint16()
        self.contents = v_bytes(page_size)
        self._entries = []

    def is_leaf(self):
        """
        return True if this is a leaf node.

        Returns:
          bool: True if this is a leaf node.
        """
        return self.ppointer == 0

    def _load_entries(self):
        if not self._entries:
            key = b''
            for i in range(self.entry_count):
                if self.is_leaf():
                    ptr = LeafEntryPointer()
                    ptr.vsParse(self.contents, offset=i * SIZEOF_ENTRY)
                    entry = LeafEntry(key, ptr.common_prefix)
                    entry.vsParse(self.contents, offset=ptr.offset - SIZEOF_ENTRY)
                else:
                    ptr = BranchEntryPointer()
                    ptr.vsParse(self.contents, offset=i * SIZEOF_ENTRY)
                    entry = BranchEntry(int(ptr.page))
                    entry.vsParse(self.contents, offset=ptr.offset - SIZEOF_ENTRY)
                self._entries.append(entry)
                key = entry.key

    def get_entries(self):
        """
        generate the entries from this page in order.
        each entry is guaranteed to have the following fields:
          - key
          - value

        Yields:
          Union[BranchEntry, LeafEntry]: the b-tree entries from this page.
        """
        self._load_entries()
        for entry in self._entries:
            yield entry

    def find_index(self, key):
        """
        find the index of the exact match, or in the case of a branch node,
         the index of the least-greater entry.
        """
        if self.is_leaf():
            for i, entry in enumerate(self.get_entries()):
                if key == bytes(entry.key):
                    return i

        else:
            for i, entry in enumerate(self.get_entries()):
                entry_key = bytes(entry.key)
                if key == entry_key:
                    return i
                if key < entry_key:
                    return i
                    continue

        raise KeyError(key)

    def get_entry(self, entry_number):
        """
        get the entry at the given index.

        Arguments:
          entry_number (int): the entry index.

        Returns:
          Union[BranchEntry, LeafEntry]: the b-tree entry.

        Raises:
          KeyError: if the entry number is not in the range of entries.
        """
        self._load_entries()
        if entry_number >= len(self._entries):
            raise KeyError(entry_number)
        return self._entries[entry_number]

    def validate(self):
        last = None
        for entry in self.get_entries():
            if last is None:
                pass
            else:
                if last.key >= entry.key:
                    raise ValueError('bad page entry sort order')
                last = entry

        return True


class FindStrategy(object):
    __doc__ = '\n    defines the interface for strategies of searching the btree.\n\n    implementors will provide a `.find()` method that operates on a `Cursor` instance.\n    the method will update the cursor as it navigates the btree.\n    '
    __meta__ = abc.ABCMeta

    @abc.abstractmethod
    def find(self, cursor, key):
        raise NotImplementedError()


class ExactMatchStrategy(FindStrategy):
    __doc__ = '\n    strategy used to find the entry with exactly the key provided.\n    if the exact key is not found, `KeyError` is raised.\n    '

    def _find(self, cursor, page_number, key):
        page = cursor.index.get_page(page_number)
        cursor.path.append(page)
        is_largest = False
        try:
            entry_number = page.find_index(key)
        except KeyError:
            is_largest = True
            entry_number = page.entry_count - 1

        entry = page.get_entry(entry_number)
        if bytes(entry.key) == key:
            cursor.entry = entry
            cursor.entry_number = entry_number
            return
        if page.is_leaf():
            raise KeyError(key)
        else:
            if is_largest:
                next_page_number = page.get_entry(page.entry_count - 1).page
            else:
                if entry_number == 0:
                    next_page_number = page.ppointer
                else:
                    next_page_number = page.get_entry(entry_number - 1).page
                self._find(cursor, next_page_number, key)
                return

    def find(self, cursor, key):
        self._find(cursor, cursor.index.root_page, key)


class PrefixMatchStrategy(FindStrategy):
    __doc__ = '\n    strategy used to find the first entry that begins with the given key.\n    it may be an exact match, or an exact match does not exist, and the result starts with the given key.\n    if no entries start with the given key, `KeyError` is raised.\n    '

    def _find(self, cursor, page_number, key):
        page = cursor.index.get_page(page_number)
        cursor.path.append(page)
        if page.is_leaf():
            for i, entry in enumerate(page.get_entries()):
                entry_key = bytes(entry.key)
                if entry_key.startswith(key):
                    cursor.entry = entry
                    cursor.entry_number = i
                    return
                if entry_key > key:
                    break

            cursor.path = cursor.path[:-1]
            raise KeyError(key)
        else:
            next_page = page.ppointer
            for i, entry in enumerate(page.get_entries()):
                entry_key = bytes(entry.key)
                if entry_key == key:
                    cursor.entry = entry
                    cursor.entry_number = i
                    return
                if entry_key.startswith(key):
                    try:
                        return self._find(cursor, next_page, key)
                    except KeyError:
                        cursor.entry = entry
                        cursor.entry_number = i
                        return

                else:
                    if entry_key > key:
                        return self._find(cursor, next_page, key)
                    next_page = entry.page

            last_entry = page.get_entry(page.entry_count - 1)
            return self._find(cursor, last_entry.page, key)

    def find(self, cursor, key):
        self._find(cursor, cursor.index.root_page, key)


class RoundDownMatchStrategy(FindStrategy):
    __doc__ = '\n    strategy used to find the matching key, or the key just less than the given key.\n    it may be an exact match, or an exact match does not exist,\n     and the result is less than the given key.\n    if no entries are less than the given key, `KeyError` is raised.\n    '

    def _find(self, cursor, page_number, key):
        page = cursor.index.get_page(page_number)
        cursor.path.append(page)
        if page.is_leaf():
            for i, entry in enumerate(page.get_entries()):
                entry_key = bytes(entry.key)
                if entry_key == key:
                    cursor.entry = entry
                    cursor.entry_number = i
                    return
                if entry_key > key:
                    if i == 0:
                        raise KeyError(key)
                    else:
                        cursor.entry = page.get_entry(i - 1)
                        cursor.entry_number = i - 1

            entry_number = page.entry_count - 1
            cursor.entry = page.get_entry(entry_number)
            cursor.entry_number = entry_number
        else:
            for i, entry in enumerate(page.get_entries()):
                entry_key = bytes(entry.key)
                if entry_key == key:
                    cursor.entry = entry
                    cursor.entry_number = i
                    return
                if entry_key > key:
                    if i == 0:
                        return self._find(cursor, page.ppointer, key)
                        try:
                            entry = page.get_entry(i - 1)
                            return self._find(cursor, entry.page, key)
                        except KeyError:
                            cursor.entry = entry
                            cursor.entry_number = i - 1
                            return

                    continue

        try:
            entry = page.get_entry(page.entry_count - 1)
            return self._find(cursor, entry.page, key)
        except KeyError:
            cursor.entry = entry
            cursor.entry_number = page.entry_count - 1
            return

    def find(self, cursor, key):
        self._find(cursor, cursor.index.root_page, key)


class MinKeyStrategy(FindStrategy):
    __doc__ = '\n    strategy used to find the minimum key in the index.\n    note: this completely ignores the provided key.\n    '

    def _find(self, cursor, page_number):
        page = cursor.index.get_page(page_number)
        cursor.path.append(page)
        if page.is_leaf():
            entry = page.get_entry(0)
            cursor.entry = entry
            cursor.entry_number = 0
        else:
            return self._find(cursor, page.ppointer)

    def find(self, cursor, _):
        self._find(cursor, cursor.index.root_page)


class MaxKeyStrategy(FindStrategy):
    __doc__ = '\n    strategy used to find the maximum key in the index.\n    note: this completely ignores the provided key.\n    '

    def _find(self, cursor, page_number):
        page = cursor.index.get_page(page_number)
        cursor.path.append(page)
        if page.is_leaf():
            entry_number = page.entry_count - 1
            entry = page.get_entry(entry_number)
            cursor.entry = entry
            cursor.entry_number = entry_number
        else:
            entry_number = page.entry_count - 1
            entry = page.get_entry(entry_number)
            return self._find(cursor, entry.page)

    def find(self, cursor, _):
        self._find(cursor, cursor.index.root_page)


EXACT_MATCH = ExactMatchStrategy
PREFIX_MATCH = PrefixMatchStrategy
ROUND_DOWN_MATCH = RoundDownMatchStrategy
MIN_KEY = MinKeyStrategy
MAX_KEY = MaxKeyStrategy

class Cursor(object):
    __doc__ = '\n    represents a particular location in the b-tree.\n    can be navigated "forward" and "backwards".\n    '

    def __init__(self, index):
        super(Cursor, self).__init__()
        self.index = index
        self.path = []
        self.entry = None
        self.entry_number = None

    def next(self):
        """
        traverse to the next entry.
        updates this current cursor instance.

        Raises:
          IndexError: if the entry does not exist. the cursor is in an unknown state afterwards.
        """
        current_page = self.path[(-1)]
        if current_page.is_leaf():
            if self.entry_number == current_page.entry_count - 1:
                start_key = self.entry.key
                while True:
                    if len(self.path) <= 1:
                        raise IndexError()
                    self.path = self.path[:-1]
                    current_page = self.path[(-1)]
                    try:
                        entry_number = current_page.find_index(start_key)
                    except KeyError:
                        continue
                    else:
                        break

                self.entry = current_page.get_entry(entry_number)
                self.entry_number = entry_number
                return
            else:
                next_entry_number = self.entry_number + 1
                next_entry = current_page.get_entry(next_entry_number)
                self.entry = next_entry
                self.entry_number = next_entry_number
                return
        else:
            next_page = self.index.get_page(self.entry.page)
            while not next_page.is_leaf():
                self.path.append(next_page)
                next_page = self.index.get_page(next_page.ppointer)

            self.path.append(next_page)
            self.entry = next_page.get_entry(0)
            self.entry_number = 0
            return

    def prev(self):
        """
        traverse to the previous entry.
        updates this current cursor instance.

        Raises:
          IndexError: if the entry does not exist. the cursor is in an unknown state afterwards.
        """
        current_page = self.path[(-1)]
        if current_page.is_leaf():
            if self.entry_number == 0:
                start_key = self.entry.key
                while True:
                    if len(self.path) <= 1:
                        raise IndexError()
                    self.path = self.path[:-1]
                    current_page = self.path[(-1)]
                    try:
                        entry_number = current_page.find_index(start_key)
                    except KeyError:
                        entry_number = current_page.entry_count

                    if entry_number == 0:
                        continue
                    else:
                        break

                self.entry = current_page.get_entry(entry_number - 1)
                self.entry_number = entry_number - 1
                return
            else:
                next_entry_number = self.entry_number - 1
                next_entry = current_page.get_entry(next_entry_number)
                self.entry = next_entry
                self.entry_number = next_entry_number
                return
        else:
            current_page = self.path[(-1)]
            if self.entry_number == 0:
                next_page_number = current_page.ppointer
            else:
                next_page_number = current_page.get_entry(self.entry_number - 1).page
            next_page = self.index.get_page(next_page_number)
            while not next_page.is_leaf():
                self.path.append(next_page)
                next_page = self.index.get_page(next_page.get_entry(next_page.entry_count - 1).page)

            self.path.append(next_page)
            self.entry = next_page.get_entry(next_page.entry_count - 1)
            self.entry_number = next_page.entry_count - 1
            return

    @property
    def key(self):
        return self.entry.key

    @property
    def value(self):
        return self.entry.value


class ID0(vstruct.VStruct):
    __doc__ = '\n    a b-tree index.\n    keys and values are arbitrary byte strings.\n\n    use `.find()` to identify a matching entry, and use the resulting cursor\n     instance to access the value, or traverse to less/greater entries.\n    '

    def __init__(self, buf, wordsize):
        vstruct.VStruct.__init__(self)
        self.buf = idb.memview(buf)
        self.wordsize = wordsize
        self.next_free_offset = v_uint32()
        self.page_size = v_uint16()
        self.root_page = v_uint32()
        self.record_count = v_uint32()
        self.page_count = v_uint32()
        self.unk12 = v_uint8()
        self.signature = v_bytes(size=9)
        self._page_cache = {}

    def get_page_buffer(self, page_number):
        if page_number < 1:
            logger.warning('unexpected page number requested: %d', page_number)
        offset = self.page_size * page_number
        return self.buf[offset:offset + self.page_size]

    def get_page(self, page_number):
        page = self._page_cache.get(page_number, None)
        if page is not None:
            return page
        buf = self.get_page_buffer(page_number)
        page = Page(self.page_size, page_number)
        page.vsParse(buf)
        self._page_cache[page_number] = page
        return page

    def find(self, key, strategy=EXACT_MATCH):
        """
        Args:
          key (bytes): the index key for which to search.
          strategy (Type[MatchStrategy]): the strategy to use to do the search.
            some possible strategies:
              - EXACT_MATCH (default)
              - PREFIX_MATCH

        Returns:
          cursor: the cursor that points to the match.

        Raises:
          KeyError: if the match failes to find a result.
        """
        c = Cursor(self)
        s = strategy()
        s.find(c, key)
        return c

    def find_prefix(self, key):
        """
        convenience shortcut for prefix match search.
        """
        return self.find(key, strategy=PREFIX_MATCH)

    def get_min(self):
        """
        find the minimum entry in the index.

        Returns:
          cursor: the cursor that points to the match.
        """
        return self.find(None, strategy=MIN_KEY)

    def get_max(self):
        """
        find the maximum entry in the index.

        Returns:
          cursor: the cursor that points to the match.
        """
        return self.find(None, strategy=MAX_KEY)

    def validate(self):
        if self.signature != b'B-tree v2':
            raise ValueError('bad signature')
        return True


class SegmentBounds(vstruct.VStruct):
    __doc__ = '\n    specifies the range of a segment.\n    '

    def __init__(self, wordsize):
        vstruct.VStruct.__init__(self)
        self.wordsize = wordsize
        if wordsize == 4:
            self.v_word = v_uint32
        else:
            if wordsize == 8:
                self.v_word = v_uint64
            else:
                raise RuntimeError('unexpected wordsize')
        self.start = self.v_word()
        self.end = self.v_word()


class ID1(vstruct.VStruct):
    __doc__ = '\n    contains flags for each byte.\n    '
    PAGE_SIZE = 8192

    def __init__(self, wordsize, buf=None):
        vstruct.VStruct.__init__(self)
        self.wordsize = wordsize
        if wordsize == 4:
            self.v_word = v_uint32
        else:
            if wordsize == 8:
                self.v_word = v_uint64
            else:
                raise RuntimeError('unexpected wordsize')
        self.signature = v_bytes(size=4)
        self.unk04 = v_uint32()
        self.segment_count = v_uint32()
        self.unk0C = v_uint32()
        self.page_count = v_uint32()
        self._segments = vstruct.VArray()
        self.segments = []
        self.padding = v_bytes()
        self.buffer = v_bytes()

    SegmentDescriptor = namedtuple('SegmentDescriptor', ['bounds', 'offset'])

    def pcb_segment_count(self):
        self['_segments'].vsAddElements(self.segment_count, functools.partial(SegmentBounds, self.wordsize))

    def pcb__segments(self):
        offset = 0
        for i in range(self.segment_count):
            segment = self._segments[i]
            segment_byte_count = segment.end - segment.start
            segment_length = 4 * segment_byte_count
            self.segments.append(ID1.SegmentDescriptor(segment, offset))
            offset += segment_length

        offset = 20 + self.segment_count * (2 * self.wordsize)
        padsize = ID1.PAGE_SIZE - offset
        self['padding'].vsSetLength(padsize)

    def pcb_page_count(self):
        self['buffer'].vsSetLength(ID1.PAGE_SIZE * self.page_count)

    def get_segment(self, ea):
        """
        find the segment that contains the given effective address.

        Returns:
          SegmentDescriptor: segment metadata and location.

        Raises:
          KeyError: if the given address is not in a segment.
        """
        for segment in self.segments:
            if segment.bounds.start <= ea < segment.bounds.end:
                return segment

        raise KeyError(ea)

    def get_next_segment(self, ea):
        """
        Fetch the next segment.

        Arguments:
          ea (int): an effective address that should fall within a segment.

        Returns:
          int: the effective address of the start of a segment.

        Raises:
          IndexError: if no more segments are found after the given segment.
          KeyError: if the given effective address does not fall within a segment.
        """
        for i, segment in enumerate(self.segments):
            if segment.bounds.start <= ea < segment.bounds.end:
                if i == len(self.segments):
                    raise IndexError(ea)
                else:
                    return self.segments[(i + 1)]

        raise KeyError(ea)

    def get_flags(self, ea):
        """
        Fetch the flags for the given effective address.

        > Each byte of the program has 32-bit flags (low 8 bits keep the byte value).
        > These 32 bits are used in GetFlags/SetFlags functions.
        via: https://www.hex-rays.com/products/ida/support/idapython_docs/idc-module.html

        Arguments:
          ea (int): the effective address.

        Returns:
          int: the flags for the given address.

        Raises:
          KeyError: if the given address does not fall within a segment.
        """
        seg = self.get_segment(ea)
        offset = seg.offset + 4 * (ea - seg.bounds.start)
        return struct.unpack_from('<I', self.buffer, offset)[0]

    def validate(self):
        if self.signature != b'VA*\x00':
            raise ValueError('bad signature')
        if self.unk04 != 3:
            raise ValueError('unexpected unk04 value')
        if self.unk0C != 2048:
            raise ValueError('unexpected unk0C value')
        for segment in self.segments:
            if segment.bounds.start > segment.bounds.end:
                raise ValueError('segment ends before it starts')

        return True


class NAM(vstruct.VStruct):
    __doc__ = '\n    contains pointers to named items.\n    '
    PAGE_SIZE = 8192

    def __init__(self, wordsize, buf=None):
        vstruct.VStruct.__init__(self)
        self.wordsize = wordsize
        if wordsize == 4:
            self.v_word = v_uint32
            self.word_fmt = 'I'
        else:
            if wordsize == 8:
                self.v_word = v_uint64
                self.word_fmt = 'Q'
            else:
                raise RuntimeError('unexpected wordsize')
        self.signature = v_bytes(size=4)
        self.unk04 = v_uint32()
        self.non_empty = v_uint32()
        self.unk0C = v_uint32()
        self.page_count = v_uint32()
        self.unk14 = self.v_word()
        self.name_count = v_uint32()
        self.padding = v_bytes(size=NAM.PAGE_SIZE - (24 + wordsize))
        self.buffer = v_bytes()

    def pcb_page_count(self):
        self['buffer'].vsSetLength(self.page_count * NAM.PAGE_SIZE)

    def validate(self):
        if self.signature != b'VA*\x00':
            raise ValueError('bad signature')
        if self.unk04 != 3:
            raise ValueError('unexpected unk04 value')
        if self.non_empty not in (0, 1):
            raise ValueError('unexpected non_empty value')
        if self.unk0C != 2048:
            raise ValueError('unexpected unk0C value')
        if self.unk14 != 0:
            raise ValueError('unexpected unk14 value')
        return True

    def names(self):
        count = self.name_count
        if self.wordsize == 8:
            count //= 2
        fmt = '<{count:d}{word_fmt:s}'.format(count=count, word_fmt=self.word_fmt)
        size = struct.calcsize(fmt)
        if size > len(self.buffer):
            raise ValueError('buffer too small')
        return struct.unpack(fmt, self.buffer[:size])


class TIL(vstruct.VStruct):

    def __init__(self, buf=None, wordsize=4):
        vstruct.VStruct.__init__(self)
        self.wordsize = wordsize
        self.signature = v_bytes(size=6)

    def validate(self):
        if self.signature != b'IDATIL':
            raise ValueError('bad signature')
        return True


SectionDescriptor = namedtuple('SectionDescriptor', ['name', 'cls'])
SECTIONS = [
 SectionDescriptor('id0', ID0),
 SectionDescriptor('id1', ID1),
 SectionDescriptor('nam', NAM),
 SectionDescriptor('seg', None),
 SectionDescriptor('til', TIL),
 SectionDescriptor('id2', None)]

class IDB(vstruct.VStruct):

    def __init__(self, buf):
        vstruct.VStruct.__init__(self)
        self.buf = idb.memview(buf)
        self.sections = []
        self.id0 = None
        self.id1 = None
        self.nam = None
        self.seg = None
        self.til = None
        self.id2 = None
        self.header = FileHeader()
        self.wordsize = 0
        self.uint = ValueError

    def pcb_header(self):
        if self.header.signature == b'IDA1':
            self.wordsize = 4
            self.uint = idb.netnode.uint32
        else:
            if self.header.signature == b'IDA2':
                self.wordsize = 8
                self.uint = idb.netnode.uint64
            else:
                raise RuntimeError('unexpected file signature: %s' % self.header.signature)
        for offset in self.header.offsets:
            if offset == 0:
                self.sections.append(None)
                continue
                sectionbuf = self.buf[offset:]
                section = Section()
                section.vsParse(sectionbuf)
                self.sections.append(section)

        for i, sectiondef in enumerate(SECTIONS):
            if i > len(self.sections):
                logger.debug('missing section: %s', sectiondef.name)
                continue
            section = self.sections[i]
            if not section:
                logger.debug('missing section: %s', sectiondef.name)
                continue
                if not sectiondef.cls:
                    logger.warn('section class not implemented: %s', sectiondef.name)
                    continue
                    s = sectiondef.cls(buf=section.contents, wordsize=self.wordsize)
                    s.vsParse(section.contents)
                    object.__setattr__(self, sectiondef.name, s)
                    logger.debug('parsed section: %s', sectiondef.name)

    def validate(self):
        self.header.validate()
        self.id0.validate()
        self.id1.validate()
        self.nam.validate()
        self.til.validate()
        return True