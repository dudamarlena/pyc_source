# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\pylib\visvis\utils\ssdf\ssdf_text.py
# Compiled at: 2016-03-22 04:56:47
# Size of source mod 2**32: 16027 bytes
""" ssdf.ssdf_text.py

Implements functionality to read/write text ssdf files.
"""
import sys, struct, base64, zlib, re
from . import ClassManager
from .ssdf_base import Struct, VirtualArray, SSDFReader, SSDFWriter, Block, _CLASS_NAME
from .ssdf_base import _shapeString, _FLOAT_TYPES, _INT_TYPES, _TYPE_DICT
from .ssdf_base import np, string_types, binary_type, ascii_type, reduce
PY3 = sys.version_info[0] == 3
if PY3:
    base64encode = base64.encodebytes
    base64decode = base64.decodebytes
else:
    base64encode = base64.encodestring
    base64decode = base64.decodestring
_DTYPES = {'uint8': '<B', 'int8': '<b', 
 'uint16': '<H', 'int16': '<h', 
 'uint32': '<L', 'int32': '<l', 
 'float32': '<f', 'float64': '<d'}

class TextSSDFReader(SSDFReader):

    def read_text_blocks(self, lines):
        """ read_text_blocks(lines)
        
        Given a list of Unicode lines, create the block instances. 
        This is a generator function.
        
        """
        for i in range(len(lines)):
            line = lines[i]
            count = i + 1
            line2 = line.lstrip()
            if not len(line2) == 0:
                if line2[0] == '#':
                    pass
                else:
                    indent = len(line) - len(line2)
                    m = re.search('^\\w+? *?=', line2)
                    if m:
                        i = m.end(0)
                        name = line2[:i - 1].strip()
                        data = line2[i:].lstrip()
                    else:
                        name = None
                        data = line2
                    yield TextBlock(indent, count, name, data=data)

    def read(self, file_or_string):
        """ read(file_or_string)
        
        Given a file or string, convert it to a struct by reading the
        blocks, building the tree and converting each block to its
        Python object.
        
        """
        if isinstance(file_or_string, string_types):
            lines = file_or_string.splitlines()
        else:
            lines = file_or_string.readlines()
            lines = [line.decode('utf-8') for line in lines]
        root = TextBlock(-1, -1, data='dict:')
        block_gen = self.read_text_blocks(lines)
        self.build_tree(root, block_gen)
        return root.to_object()


class TextSSDFWriter(SSDFWriter):

    def write_text_blocks(self, blocks):
        """ write_text_blocks(blocks)
        
        Converts the given blocks to a list of string lines.
        
        """
        lines = []
        for block in blocks[1:]:
            line = str(' ') * block._indent
            if block._name:
                line += '%s = ' % block._name
            line += block._data
            lines.append(line)

        return lines

    def write(self, object, f=None):
        """ write(object, f=None)
        
        Serializes the given struct. If a file is given, writes 
        (utf-8 encoded)text to that file, otherwise returns a string.
        
        """
        root = TextBlock.from_object(-1, '', object)
        blocks = self.flatten_tree(root, True)
        lines = self.write_text_blocks(blocks)
        if f is None:
            return '\n'.join(lines)
        NL = '\n'.encode('utf-8')
        for line in lines:
            f.write(line.encode('utf-8'))
            f.write(NL)


class TextBlock(Block):

    def to_object(self):
        data = self._data
        if not data:
            print('SSDF: no value specified at line %i.' % self._blocknr)
        else:
            if data[0] in '-.0123456789':
                if '.' in data:
                    return self._to_float()
                else:
                    return self._to_int()
            else:
                if data[0] == "'":
                    return self._to_unicode()
                else:
                    if data.startswith('array'):
                        return self._to_array()
                    if data.startswith('dict:'):
                        return self._to_dict()
                    if data.startswith('list:') or data[0] == '[':
                        return self._to_list()
                    if data.startswith('Null') or data.startswith('None'):
                        return self._to_none()
                    print('SSDF: invalid type on line %i.' % self._blocknr)
                    return

    def _from_none(self, value=None):
        self._data = 'Null'

    def _to_none(self):
        pass

    def _from_int(self, value):
        self._data = '%i' % int(value)

    def _to_int(self):
        line = self._data
        i = line.find('#')
        if i > 0:
            line = line[:i].strip()
        try:
            return int(line)
        except Exception:
            print('SSDF: could not parse integer on line %i.' % self._blocknr)
            return

    def _from_float(self, value):
        self._data = '%0.20g' % value

    def _to_float(self):
        line = self._data
        i = line.find('#')
        if i > 0:
            line = line[:i].strip()
        try:
            return float(line)
        except Exception:
            print('SSDF: could not parse float on line %i.' % self._blocknr)
            return

    def _from_unicode(self, value):
        value = value.replace('\\', '\\\\')
        value = value.replace('\n', '\\n')
        value = value.replace('\r', '\\r')
        value = value.replace('\x0b', '\\x0b').replace('\x0c', '\\x0c')
        value = value.replace("'", "\\'")
        self._data = "'" + value + "'"

    def _to_unicode(self):
        line = self._data.replace('\\\\', '0x07')
        m = re.search("'.*?[^\\\\]'|''", line)
        if not m:
            print('SSDF: string not ended correctly on line %i.' % self._blocknr)
            return
        line = m.group(0)[1:-1]
        line = line.replace('\\n', '\n')
        line = line.replace('\\r', '\r')
        line = line.replace('\\x0b', '\x0b').replace('\\x0c', '\x0c')
        line = line.replace("\\'", "'")
        line = line.replace('0x07', '\\')
        return line

    def _from_dict(self, value):
        self._data = 'dict:'
        self._type = _TYPE_DICT
        keys = [key for key in value]
        keys.sort()
        for key in keys:
            if key.startswith('__'):
                pass
            else:
                val = value[key]
                if hasattr(val, '__call__') and not hasattr(val, '__to_ssdf__'):
                    pass
                else:
                    subBlock = TextBlock.from_object(self._indent + 1, key, val)
                    self._children.append(subBlock)

    def _to_dict(self):
        value = Struct()
        for child in self._children:
            val = child.to_object()
            if child._name:
                value[child._name] = val
            else:
                print('SSDF: unnamed element in dict on line %i.' % child._blocknr)

        if _CLASS_NAME in value:
            className = value[_CLASS_NAME]
            if className in ClassManager._registered_classes:
                value = ClassManager._registered_classes[className].__from_ssdf__(value)
        else:
            print('SSDF: class %s not registered.' % className)
        return value

    def _from_list(self, value):
        isSmallList = True
        allowedTypes = _INT_TYPES + _FLOAT_TYPES + (string_types,)
        subBlocks = []
        for element in value:
            subBlock = TextBlock.from_object(self._indent + 1, None, element)
            subBlocks.append(subBlock)
            if not isinstance(element, allowedTypes):
                isSmallList = False

        if isSmallList:
            elements = [subBlock._data.strip() for subBlock in subBlocks]
            self._data = '[%s]' % ', '.join(elements)
        else:
            self._data = 'list:'
            for subBlock in subBlocks:
                self._children.append(subBlock)

    def _to_list(self):
        value = []
        if self._data[0] == 'l':
            for child in self._children:
                val = child.to_object()
                if child._name:
                    print('SSDF: named element in list on line %i.' % child._blocknr)
                else:
                    value.append(val)

            return value
        else:
            return self._to_list2()

    def _to_list2(self):
        i0 = 1
        pieces = []
        inString = False
        escapeThis = False
        line = self._data
        for i in range(1, len(line)):
            if inString:
                if escapeThis:
                    escapeThis = False
                    continue
                else:
                    if line[i] == '\\':
                        escapeThis = True
                    elif line[i] == "'":
                        inString = False
            else:
                if line[i] == "'":
                    inString = True
                else:
                    if line[i] == ',':
                        pieces.append(line[i0:i])
                        i0 = i + 1
                    elif line[i] == ']':
                        piece = line[i0:i]
                        if piece.strip():
                            pieces.append(piece)
                        break
        else:
            print('SSDF: one-line list not closed correctly on line %i.' % self._blocknr)

        value = []
        for piece in pieces:
            lo = TextBlock(self._indent, self._blocknr, data=piece.strip())
            value.append(lo.to_object())

        return value

    def _from_array(self, value):
        shapestr = _shapeString(value)
        dtypestr = str(value.dtype)
        if value.size < 33 and not isinstance(value, VirtualArray):
            if 'int' in dtypestr:
                elements = ['%i' % v for v in value.ravel()]
            else:
                elements = ['%0.20g' % v for v in value.ravel()]
            if elements:
                elements.append('')
            self._data = 'array %s %s %s' % (shapestr, dtypestr,
             ', '.join(elements))
        else:
            data = value.tostring()
            BS = 1048576
            texts = []
            i = 0
            while i < len(data):
                block = data[i:i + BS]
                blockc = zlib.compress(block)
                text = base64encode(blockc).decode('utf-8')
                texts.append(text.replace('\n', ''))
                i += BS

            text = ';'.join(texts)
            self._data = 'array %s %s %s' % (shapestr, dtypestr, text)

    def _to_array(self):
        tmp = self._data.split(' ', 3)
        if len(tmp) < 4:
            print('SSDF: invalid array definition on line %i.' % self._blocknr)
            return
        word2 = tmp[1]
        word3 = tmp[2]
        word4 = tmp[3]
        try:
            shape = [int(i) for i in word2.split('x') if i]
        except Exception:
            print('SSDF: invalid array shape on line %i.' % self._blocknr)
            return

        if shape:
            size = reduce(lambda a, b: a * b, shape)
        else:
            size = 1
        dtypestr = ascii_type(word3)
        if dtypestr not in _DTYPES.keys():
            print('SSDF: invalid array data type on line %i.' % self._blocknr)
            return
        asAscii = word4.find(',', 0, 100) > 0 or word4.endswith(',')
        if size == 0:
            data = binary_type()
        else:
            if asAscii:
                dataparts = []
                fmt = _DTYPES[dtypestr]
                for val in word4.split(','):
                    if not val.strip():
                        pass
                    else:
                        try:
                            if 'int' in dtypestr:
                                val = int(val)
                            else:
                                val = float(val)
                            dataparts.append(struct.pack(fmt, val))
                        except Exception:
                            if 'int' in dtypestr:
                                dataparts.append(struct.pack(fmt, 0))
                            else:
                                dataparts.append(struct.pack(fmt, float('nan')))

                data = binary_type().join(dataparts)
            else:
                dataparts = []
                for blockt in word4.split(';'):
                    blockc = base64decode(blockt.encode('utf-8'))
                    block = zlib.decompress(blockc)
                    dataparts.append(block)

                data = binary_type().join(dataparts)
        if not np:
            return VirtualArray(shape, dtypestr, data)
        else:
            if data:
                value = np.frombuffer(data, dtype=dtypestr)
                if size == value.size:
                    value.shape = tuple(shape)
                else:
                    print('SSDF: prod(shape)!=size on line %i.' % self._blocknr)
                return value
            return np.zeros(shape, dtype=dtypestr)