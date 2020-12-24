# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/misc/file_3ds.py
# Compiled at: 2009-09-07 17:44:28
"""
3D Studio Max file (.3ds) parser.
Author: Victor Stinner
"""
from hachoir_parser import Parser
from hachoir_core.field import StaticFieldSet, FieldSet, UInt16, UInt32, RawBytes, Enum, CString
from hachoir_parser.image.common import RGB
from hachoir_core.endian import LITTLE_ENDIAN
from hachoir_core.text_handler import textHandler, hexadecimal
from hachoir_parser.misc.common import Vertex, MapUV

def readObject(parent):
    yield CString(parent, 'name', 'Object name')
    size = parent['size'].value * 8
    while parent.current_size < size:
        yield Chunk(parent, 'chunk[]')


def readTextureFilename(parent):
    yield CString(parent, 'filename', 'Texture filename')


def readVersion(parent):
    yield UInt32(parent, 'version', '3DS file format version')


def readMaterialName(parent):
    yield CString(parent, 'name', 'Material name')


class Polygon(StaticFieldSet):
    __module__ = __name__
    format = ((UInt16, 'a', 'Vertex A'), (UInt16, 'b', 'Vertex B'), (UInt16, 'c', 'Vertex C'), (UInt16, 'flags', 'Flags'))


def readMapList(parent):
    yield UInt16(parent, 'count', 'Map count')
    for index in xrange(parent['count'].value):
        yield MapUV(parent, 'map_uv[]', 'Mapping UV')


def readColor(parent):
    yield RGB(parent, 'color')


def readVertexList(parent):
    yield UInt16(parent, 'count', 'Vertex count')
    for index in range(0, parent['count'].value):
        yield Vertex(parent, 'vertex[]', 'Vertex')


def readPolygonList(parent):
    count = UInt16(parent, 'count', 'Vertex count')
    yield count
    for i in range(0, count.value):
        yield Polygon(parent, 'polygon[]')

    size = parent['size'].value * 8
    while parent.current_size < size:
        yield Chunk(parent, 'chunk[]')


class Chunk(FieldSet):
    __module__ = __name__
    type_name = {17: 'Color', 19789: 'Main chunk', 2: 'File version', 15677: 'Materials and objects', 16384: 'Object', 16640: 'Mesh (triangular)', 16656: 'Vertices list', 16672: 'Polygon (faces) list', 16704: 'Map UV list', 16688: 'Object material', 45055: 'New material', 40960: 'Material name', 40976: 'Material ambient', 40992: 'Material diffuse', 41008: 'Texture specular', 41472: 'Texture', 41728: 'Texture filename', 45056: 'Keyframes', 45058: 'Object node tag', 45062: 'Light target node tag', 45063: 'Spot light node tag', 45066: 'Keyframes header', 45065: 'Keyframe current time', 45104: 'Node identifier', 45072: 'Node header', 28673: 'Viewport layout'}
    chunk_id_by_type = {19789: 'main', 2: 'version', 15677: 'obj_mat', 45056: 'keyframes', 45055: 'material[]', 16384: 'object[]', 16656: 'vertices_list', 16672: 'polygon_list', 16704: 'mapuv_list', 16640: 'mesh'}
    sub_chunks = (19789, 16640, 15677, 45055, 41472, 45058, 45062, 45063, 40976, 41008,
                  40992, 45056)
    handlers = {40960: readMaterialName, 16384: readObject, 41728: readTextureFilename, 17: readColor, 2: readVersion, 16656: readVertexList, 16672: readPolygonList, 16704: readMapList}

    def __init__(self, *args):
        FieldSet.__init__(self, *args)
        self._description = 'Chunk: %s' % self['type'].display
        type = self['type'].value
        if type in Chunk.chunk_id_by_type:
            self._name = Chunk.chunk_id_by_type[type]
        else:
            self._name = 'chunk_%04x' % type
        self._size = self['size'].value * 8

    def createFields(self):
        yield Enum(textHandler(UInt16(self, 'type', 'Chunk type'), hexadecimal), Chunk.type_name)
        yield UInt32(self, 'size', 'Chunk size (in bytes)')
        content_size = self['size'].value - 6
        if content_size == 0:
            return
        type = self['type'].value
        if type in Chunk.sub_chunks:
            while self.current_size < self.size:
                yield Chunk(self, 'chunk[]')

        elif type in Chunk.handlers:
            fields = Chunk.handlers[type](self)
            for field in fields:
                yield field

        else:
            yield RawBytes(self, 'data', content_size)


class File3ds(Parser):
    __module__ = __name__
    endian = LITTLE_ENDIAN
    PARSER_TAGS = {'id': '3ds', 'category': 'misc', 'file_ext': ('3ds', ), 'mime': ('image/x-3ds', ), 'min_size': 16 * 8, 'description': '3D Studio Max model'}

    def validate(self):
        if self.stream.readBytes(0, 2) != 'MM':
            return 'Wrong signature'
        if self['main/version/version'].value not in (2, 3):
            return 'Unknown format version'
        return True

    def createFields(self):
        while not self.eof:
            yield Chunk(self, 'chunk[]')