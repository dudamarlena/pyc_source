# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dev\pylib\visvis\utils\ssdf\ssdf_bin.py
# Compiled at: 2017-05-31 20:05:28
# Size of source mod 2**32: 15657 bytes
""" ssdf.ssdf_bin.py

Implements functionality to read/write binary ssdf (.bsdf) files.
"""
import struct, zlib
from . import ClassManager
from .ssdf_base import Struct, VirtualArray, SSDFReader, SSDFWriter, Block, _CLASS_NAME
from .ssdf_base import np, binary_type, ascii_type
_SMALL_NUMBER_FMT = '<B'
_LARGE_NUMBER_FMT = '<Q'
_TYPE_FMT = '<B'
_PARTITION_LEN_FMT = '<I'
_PARTITION_SIZE = 1048576
_TYPE_NONE = ord('N')
_TYPE_INT = ord('I')
_TYPE_FLOAT = ord('F')
_TYPE_UNICODE = ord('U')
_TYPE_ARRAY = ord('A')
_TYPE_LIST = ord('L')
_TYPE_DICT = ord('D')

class BinarySSDFReader(SSDFReader):

    def read_binary_blocks(self, f):
        """ read_binary_blocks(f)
        
        Given a file, creates the block instances.
        This is a generator function.
        
        """
        count = 0
        while True:
            count += 1
            try:
                type_id, = struct.unpack(_TYPE_FMT, f.read(1))
            except StopIteration:
                break

            indent = f.read_number()
            name_len = f.read_number()
            if name_len:
                name = f.read(name_len).decode('utf-8')
            else:
                name = None
            data_len = f.read_number()
            data = f.read(data_len)
            yield BinaryBlock(indent, count, name, type_id, data=data)

    def read(self, file_or_bytes):
        """ read(file_or_bytes)
        
        Given a file or bytes, convert it to a struct by reading the
        blocks, building the tree and converting each block to its
        Python object.
        
        """
        if isinstance(file_or_bytes, binary_type):
            f = _VirtualFile(file_or_bytes)
        else:
            f = file_or_bytes
        bb1 = 'BSDF'.encode('utf-8')
        try:
            bb2 = f.read(len(bb1))
        except Exception:
            raise ValueError('Could not read header of binary SSDF file.')

        if bb1 != bb2:
            raise ValueError('Given SSDF bytes/file does not have the right header.')
        fc = _CompressedFile(f)
        root = BinaryBlock((-1), (-1), type=_TYPE_DICT)
        block_gen = self.read_binary_blocks(fc)
        self.build_tree(root, block_gen)
        return root.to_object()


class BinarySSDFWriter(SSDFWriter):

    def write_binary_blocks(self, blocks, f):
        """ write_binary_blocks(blocks, f)
        
        Writes the given blocks to a binary file.
        
        """
        for block in blocks[1:]:
            f.write(struct.pack(_TYPE_FMT, block._type))
            f.write_number(block._indent)
            if block._name:
                name = block._name.encode('utf-8')
                f.write_number(len(name))
                f.write(name)
            else:
                f.write_number(0)
            if isinstance(block._data, list):
                data_len = sum([len(d) for d in block._data])
                f.write_number(data_len)
                for part in block._data:
                    f.write(part)

            else:
                data_len = len(block._data)
                f.write_number(data_len)
                f.write(block._data)

    def write(self, object, f=None):
        """ write(object, f=None)
        
        Serializes the given struct. If a file is given, writes bytes
        to that file, otherwise returns a bytes instance.
        
        """
        if f is None:
            f = _VirtualFile()
            return_bytes = True
        else:
            return_bytes = False
        f.write('BSDF'.encode('utf-8'))
        fc = _CompressedFile(f)
        root = BinaryBlock.from_object(-1, binary_type(), object)
        blocks = self.flatten_tree(root)
        self.write_binary_blocks(blocks, fc)
        fc.flush()
        if return_bytes:
            return f.get_bytes()


class BinaryBlock(Block):

    def to_object(self):
        type = self._type
        if type == _TYPE_INT:
            return self._to_int()
        if type == _TYPE_FLOAT:
            return self._to_float()
        if type == _TYPE_UNICODE:
            return self._to_unicode()
        if type == _TYPE_ARRAY:
            return self._to_array()
        if type == _TYPE_LIST:
            return self._to_list()
        if type == _TYPE_DICT:
            return self._to_dict()
        if type == _TYPE_NONE:
            return self._to_none()
        print('SSDF: invalid type %s in block %i.' % (repr(type), self._blocknr))
        return

    def _from_none(self, value=None):
        self._type = _TYPE_NONE
        self._data = binary_type()

    def _to_none(self):
        pass

    def _from_int(self, value):
        self._type = _TYPE_INT
        self._data = struct.pack('<q', int(value))

    def _to_int(self):
        return struct.unpack('<q', self._data)[0]

    def _from_float(self, value):
        self._type = _TYPE_FLOAT
        self._data = struct.pack('<d', float(value))

    def _to_float(self):
        return struct.unpack('<d', self._data)[0]

    def _from_unicode(self, value):
        self._type = _TYPE_UNICODE
        self._data = value.encode('utf-8')

    def _to_unicode(self):
        return self._data.decode('utf-8')

    def _from_array(self, value):
        self._type = _TYPE_ARRAY
        f = _VirtualFile()
        f.write_number(value.ndim)
        for s in value.shape:
            f.write_number(s)

        f.write_string(str(value.dtype))
        self._data = [
         f.get_bytes(), value.tostring()]

    def _to_array(self):
        f = _VirtualFile(self._data)
        ndim = f.read_number()
        shape = [f.read_number() for i in range(ndim)]
        dtypestr = ascii_type(f.read_string())
        i = f._fp
        if not np:
            return VirtualArray(shape, dtypestr, self._data[i:])
        else:
            if i < len(self._data):
                value = np.frombuffer((self._data), dtype=dtypestr, offset=i)
            else:
                value = np.array([], dtype=dtypestr)
            if np.prod(shape) == value.size:
                value.shape = tuple(shape)
            else:
                print('SSDF: prod(shape)!=size on line %i.' % self._blocknr)
        return value

    def _from_dict(self, value):
        self._type = _TYPE_DICT
        self._data = binary_type()
        keys = [key for key in value]
        keys.sort()
        for key in keys:
            if key.startswith('__'):
                continue
            val = value[key]
            if hasattr(val, '__call__'):
                if not hasattr(val, '__to_ssdf__'):
                    continue
            subBlock = BinaryBlock.from_object(self._indent + 1, key, val)
            self._children.append(subBlock)

    def _to_dict(self):
        value = Struct()
        for child in self._children:
            val = child.to_object()
            if child._name:
                value[child._name] = val
            else:
                print('SSDF: unnamed element in dict in block %i.' % child._blocknr)

        if _CLASS_NAME in value:
            className = value[_CLASS_NAME]
            if className in ClassManager._registered_classes:
                value = ClassManager._registered_classes[className].__from_ssdf__(value)
            else:
                print('SSDF: class %s not registered.' % className)
        return value

    def _from_list(self, value):
        self._type = _TYPE_LIST
        self._data = binary_type()
        for element in value:
            subBlock = BinaryBlock.from_object(self._indent + 1, None, element)
            self._children.append(subBlock)

    def _to_list(self):
        value = []
        for child in self._children:
            val = child.to_object()
            if child._name:
                print('SSDF: named element in list in block %i.' % child._blocknr)
            else:
                value.append(val)

        return value


class _FileWithExtraMethods:

    def write_number(self, n):
        if n < 255:
            self.write(struct.pack(_SMALL_NUMBER_FMT, n))
        else:
            self.write(struct.pack(_SMALL_NUMBER_FMT, 255))
            self.write(struct.pack(_LARGE_NUMBER_FMT, n))

    def write_bytes(self, bb):
        self.write_number(len(bb))
        self.write(bb)

    def write_string(self, ss):
        self.write_bytes(ss.encode('utf-8'))

    def read_number(self):
        n, = struct.unpack(_SMALL_NUMBER_FMT, self.read(1))
        if n == 255:
            n, = struct.unpack(_LARGE_NUMBER_FMT, self.read(8))
        return n

    def read_bytes(self):
        n = self.read_number()
        return self.read(n)

    def read_string(self):
        return self.read_bytes().decode('utf-8')


class _VirtualFile(_FileWithExtraMethods):
    __doc__ = ' _VirtualFile(bb=None)\n    \n    Wraps a bytes instance to provide a file-like interface. Also\n    represents a file like object to which bytes can be written, and\n    the resulting bytes can be obtained using get_bytes().\n    \n    '

    def __init__(self, bb=None):
        self._bb = bb
        self._fp = 0
        self._parts = []

    def read(self, n):
        i1 = self._fp
        self._fp = i2 = self._fp + n
        return self._bb[i1:i2]

    def write(self, data):
        self._parts.append(data)

    def close(self):
        pass

    def get_bytes(self):
        return binary_type().join(self._parts)


class _CompressedFile(_FileWithExtraMethods):
    __doc__ = " _CompressedFile(file)\n    \n    Wraps a file object to transparantly support reading and writing\n    data from/to a compressed file.\n    \n    Data is compressed in partitions of say 1MB. A partition in the file\n    consists of a small header and a body. The header consists of 4 bytes\n    representing the body's length (little endian unsigned 32 bit int).\n    The body consists of bytes compressed using DEFLATE (i.e. zip).\n    \n    "

    def __init__(self, f):
        self._file = f
        self._buffer = binary_type()
        self._bp = 0
        self._parts = []
        self._pp = 0

    def _read_new_partition(self):
        """ _read_new_partition()
        
        Returns the data in the next partition.
        Returns false if no new partition is available.
        
        """
        bb = self._file.read(4)
        if not bb:
            self._buffer = binary_type()
            self._bp = 0
            return False
        n, = struct.unpack(_PARTITION_LEN_FMT, bb)
        bb = self._file.read(n)
        data = zlib.decompress(bb)
        del bb
        return data

    def _write_new_partition(self):
        """ _write_new_partition()
        
        Compress the buffered data and write to file. Reset buffer.
        
        """
        data = binary_type().join(self._parts)
        self._parts = []
        self._pp = 0
        bb = zlib.compress(data)
        del data
        header = struct.pack(_PARTITION_LEN_FMT, len(bb))
        self._file.write(header)
        self._file.write(bb)

    def read(self, n):
        """ read(n)
        
        Read n bytes. Partitions are automatically decompressed on the fly.
        If the end of the file is reached, raises StopIteration.
        
        """
        bytes_in_buffer = len(self._buffer) - self._bp
        if bytes_in_buffer < n:
            localBuffer = [
             self._buffer[self._bp:]]
            bufferCount = len(localBuffer[0])
            while bufferCount < n:
                partition = self._read_new_partition()
                if partition:
                    localBuffer.append(partition)
                    bufferCount += len(partition)
                else:
                    raise StopIteration

            offset = len(partition) - (bufferCount - n)
            self._bp = offset
            self._buffer = partition
            localBuffer[-1] = partition[:offset]
            data = binary_type().join(localBuffer)
        else:
            i1 = self._bp
            self._bp = i2 = i1 + n
            data = self._buffer[i1:i2]
        return data

    def write(self, data):
        """ write(data)
        
        Write data. The data is buffered until the accumulated size
        exceeds the partition size. When this happens, the data is compressed
        and written to the real underlying file/data.
        
        """
        i = self._pp + len(data) - _PARTITION_SIZE
        if i > 0:
            self._parts.append(data[:i])
            data = data[i:]
            self._write_new_partition()
        self._parts.append(data)
        self._pp += len(data)

    def flush(self):
        """ flush()
        
        After the last write, use this to compress and write
        the last partition.
        
        """
        self._write_new_partition()