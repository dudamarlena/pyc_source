# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/misc/file_3do.py
# Compiled at: 2009-09-07 17:44:28
"""
3do model parser.

Author: Cyril Zorin
Creation date: 28 september 2006
"""
from hachoir_parser import Parser
from hachoir_core.field import FieldSet, UInt32, Int32, String, Float32, RawBytes, PaddingBytes
from hachoir_core.endian import LITTLE_ENDIAN, BIG_ENDIAN
from hachoir_parser.misc.common import Vertex, MapUV

class Vector(FieldSet):
    __module__ = __name__

    def __init__(self, parent, name, count, type, ename, edesc=None, description=None):
        FieldSet.__init__(self, parent, name, description)
        self.count = count
        self.type = type
        self.ename = ename + '[]'
        self.edesc = edesc
        try:
            item_size = self.type.static_size(self.ename, self.edesc)
        except TypeError:
            item_size = self.type.static_size

        if item_size:
            self._size = item_size * self.count

    def createFields(self):
        for index in xrange(self.count):
            yield self.type(self, self.ename, self.edesc)


class Face(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield UInt32(self, 'id')
        yield UInt32(self, 'type')
        yield UInt32(self, 'geometry_mode')
        yield UInt32(self, 'lighting_mode')
        yield UInt32(self, 'texture_mode')
        yield UInt32(self, 'nvertices')
        yield Float32(self, 'unknown[]', 'unknown')
        yield UInt32(self, 'has_texture', 'Has texture?')
        yield UInt32(self, 'has_material', 'Has material?')
        yield Vertex(self, 'unknown[]')
        yield Float32(self, 'extra_light')
        yield Vertex(self, 'unknown[]')
        yield Vertex(self, 'normal')
        if self['nvertices'].value:
            yield Vector(self, 'vertex_indices', self['nvertices'].value, UInt32, 'vertex')
        if self['has_texture'].value:
            yield Vector(self, 'texture_vertex_indices', self['nvertices'].value, UInt32, 'texture_vertex')
        if self['has_material'].value:
            yield UInt32(self, 'material_index', 'material index')

    def createDescription(self):
        return 'Face: id=%s' % self['id'].value


class Mesh(FieldSet):
    __module__ = __name__

    def __init__(self, *args):
        FieldSet.__init__(self, *args)

    def createFields(self):
        yield String(self, 'name', 32, strip='\x00')
        yield UInt32(self, 'id')
        yield UInt32(self, 'geometry_mode')
        yield UInt32(self, 'lighting_mode')
        yield UInt32(self, 'texture_mode')
        yield UInt32(self, 'nmesh_vertices')
        yield UInt32(self, 'ntexture_vertices')
        yield UInt32(self, 'nfaces')
        nb_vert = self['nmesh_vertices'].value
        if nb_vert:
            yield Vector(self, 'vertices', nb_vert, Vertex, 'vertex')
        if self['ntexture_vertices'].value:
            yield Vector(self, 'texture vertices', self['ntexture_vertices'].value, MapUV, 'texture_vertex')
        if nb_vert:
            yield Vector(self, 'light vertices', nb_vert, Float32, 'extra_light')
            yield Vector(self, 'unknown[]', nb_vert, Float32, 'unknown')
        if self['nfaces'].value:
            yield Vector(self, 'faces', self['nfaces'].value, Face, 'face')
        if nb_vert:
            yield Vector(self, 'vertex normals', nb_vert, Vertex, 'normal')
        yield UInt32(self, 'has_shadow')
        yield Float32(self, 'unknown[]')
        yield Float32(self, 'radius')
        yield Vertex(self, 'unknown[]')
        yield Vertex(self, 'unknown[]')

    def createDescription(self):
        return 'Mesh "%s" (id %s)' % (self['name'].value, self['id'].value)


class Geoset(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield UInt32(self, 'count')
        for index in xrange(self['count'].value):
            yield Mesh(self, 'mesh[]')

    def createDescription(self):
        return 'Set of %s meshes' % self['count'].value


class Node(FieldSet):
    __module__ = __name__

    def __init__(self, *args):
        FieldSet.__init__(self, *args)
        size = (188 - 4) * 8
        if self['parent_offset'].value != 0:
            size += 32
        if self['first_child_offset'].value != 0:
            size += 32
        if self['next_sibling_offset'].value != 0:
            size += 32
        self._size = size

    def createFields(self):
        yield String(self, 'name', 32, strip='\x00')
        yield PaddingBytes(self, 'unknown[]', 32, pattern=b'\xcc')
        yield UInt32(self, 'flags')
        yield UInt32(self, 'id')
        yield UInt32(self, 'type')
        yield Int32(self, 'mesh_id')
        yield UInt32(self, 'depth')
        yield Int32(self, 'parent_offset')
        yield UInt32(self, 'nchildren')
        yield UInt32(self, 'first_child_offset')
        yield UInt32(self, 'next_sibling_offset')
        yield Vertex(self, 'pivot')
        yield Vertex(self, 'position')
        yield Float32(self, 'pitch')
        yield Float32(self, 'yaw')
        yield Float32(self, 'roll')
        for index in xrange(4):
            yield Vertex(self, 'unknown_vertex[]')

        if self['parent_offset'].value != 0:
            yield UInt32(self, 'parent_id')
        if self['first_child_offset'].value != 0:
            yield UInt32(self, 'first_child_id')
        if self['next_sibling_offset'].value != 0:
            yield UInt32(self, 'next_sibling_id')

    def createDescription(self):
        return 'Node "%s"' % self['name'].value


class Nodes(FieldSet):
    __module__ = __name__

    def createFields(self):
        yield UInt32(self, 'count')
        for index in xrange(self['count'].value):
            yield Node(self, 'node[]')

    def createDescription(self):
        return 'Nodes (%s)' % self['count'].value


class Materials(FieldSet):
    __module__ = __name__

    def __init__(self, *args):
        FieldSet.__init__(self, *args)
        count = self['count']
        self._size = count.size + count.value * (32 * 8)

    def createFields(self):
        yield UInt32(self, 'count')
        for index in xrange(self['count'].value):
            yield String(self, 'filename[]', 32, 'Material file name', strip='\x00')

    def createDescription(self):
        return 'Material file names (%s)' % self['count'].value


class File3do(Parser):
    __module__ = __name__
    PARSER_TAGS = {'id': '3do', 'category': 'misc', 'file_ext': ('3do', ), 'mime': ('image/x-3do', ), 'min_size': 8 * 4, 'description': 'renderdroid 3d model.'}
    endian = LITTLE_ENDIAN

    def validate(self):
        signature = self.stream.readBytes(0, 4)
        return signature in ('LDOM', 'MODL')

    def createFields(self):
        yield String(self, 'file_sig', 4, 'File signature', charset='ASCII')
        if self['file_sig'].value == 'MODL':
            self.endian = BIG_ENDIAN
        yield Materials(self, 'materials')
        yield String(self, 'model_name', 32, 'model file name', strip='\x00')
        yield RawBytes(self, 'unknown[]', 4)
        yield UInt32(self, 'ngeosets')
        for index in xrange(self['ngeosets'].value):
            yield Geoset(self, 'geoset[]')

        yield RawBytes(self, 'unknown[]', 4)
        yield Nodes(self, 'nodes')
        yield Float32(self, 'model_radius')
        yield Vertex(self, 'insertion_offset')
        if self.current_size < self._size:
            yield self.seekBit(self._size, 'end')