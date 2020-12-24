# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyhapi\hgeo.py
# Compiled at: 2020-03-18 10:18:32
# Size of source mod 2**32: 21804 bytes
__doc__ = 'Wrapper for houdini engine\'s geometry.\nAuthor  : Maajor\nEmail   : info@ma-yidong.com\n\nHGeo:\n    An base class for houdini engine\'s geometry, including shared operation        for setting and getting attributes. It could derived HGeoMesh        for handling mesh, HGeoCurve for handling curve, HGeoVolume for             handling volume data.\n\nHGeoMesh:\n    An object containing mesh data\n\nHGeoCurve:\n    An object containing curve data\n\nExample usage:\n\nimport pyhapi as ph\n\n#create houdini engine session\nsession = ph.HSessionManager.get_or_create_default_session()\n\n#create an inputnode where you can set geometry\ngeo_inputnode = ph.HInputNode(session, "Cube")\n\n#create a geomesh\ncube_geo = ph.HGeoMesh(\n    vertices=np.array(\n        [[0.0, 0.0, 0.0],\n            [0.0, 0.0, 1.0],\n            [0.0, 1.0, 0.0],\n            [0.0, 1.0, 1.0],\n            [1.0, 0.0, 0.0],\n            [1.0, 0.0, 1.0],\n            [1.0, 1.0, 0.0],\n            [1.0, 1.0, 1.0]], dtype=np.float32),\n    faces=np.array(\n        [[0, 2, 6, 4],\n            [2, 3, 7, 6],\n            [2, 0, 1, 3],\n            [1, 5, 7, 3],\n            [5, 4, 6, 7],\n            [0, 4, 5, 1]], dtype=np.int32))\n\n#set this geomesh as geometry of inputnode\ngeo_inputnode.set_geometry(cube_geo)\n\n'
import numpy as np
from . import hdata as HDATA
from . import hapi as HAPI

class HGeo:
    """HGeo"""

    def __init__(self):
        self.part_info = HDATA.PartInfo()
        self.point_count = 0
        self.vertex_count = 0
        self.face_count = 0
        self.detail_count = 1
        self.attribs = {}
        self.type_to_add_attrib = {HDATA.AttributeOwner.VERTEX: self.add_vertex_attrib, 
         HDATA.AttributeOwner.POINT: self.add_point_attrib, 
         HDATA.AttributeOwner.PRIM: self.add_prim_attrib, 
         HDATA.AttributeOwner.DETAIL: self.add_detail_attrib}

    def add_attrib(self, attrib_type, name, data):
        """Add attribute data to geo, should provide attribute's            type, name and data

        Args:
            attrib_type (AttributeOwner): Type of the attribute
            name (str): name of the attribute
            data (ndarray(,)): Attribute data, should be 2D, 1st dims                corresponding to each item in that attribute, ptnum/vtnum                    primnum etc, 2nd dim should be tuple size of this attribute
        """
        self.type_to_add_attrib[attrib_type](name, data)

    def add_point_attrib(self, name, data):
        """Add point attribute data to geo

        Args:
            name (str): name of the attribute
            data (ndarray(,)): Attribute data, should be 2D, 1st dims                equals number of points, 2nd dim should be tuple size of this attribute
        """
        count, tuple_size = data.shape
        if count != self.point_count:
            print('AddPointAttrib Error, Data length {0} not compatible with point count {1}'.format(count, self.point_count))
            return
        attrib_info = HDATA.AttributeInfo()
        attrib_info.count = count
        attrib_info.tupleSize = tuple_size
        attrib_info.exists = True
        attrib_info.storage = HDATA.NP_TYPE_TO_HSTORAGE_TYPE[data.dtype]
        attrib_info.owner = HDATA.AttributeOwner.POINT
        self.part_info.point_attrib_count += 1
        self.attribs[(HDATA.AttributeOwner.POINT, name)] = (
         attrib_info, name, data)

    def add_vertex_attrib(self, name, data):
        """Add vertex attribute data to geo

        Args:
            name (str): name of the attribute
            data (ndarray(,)): Attribute data, should be 2D, 1st dims                equals number of vertices, 2nd dim should be tuple size of this attribute
        """
        count, tuple_size = data.shape
        if count != self.vertex_count:
            print('AddVertexAttrib Error, Data length {0} not compatible with vertex count {1}'.format(count, self.vertex_count))
            return
        attrib_info = HDATA.AttributeInfo()
        attrib_info.count = count
        attrib_info.tupleSize = tuple_size
        attrib_info.exists = True
        attrib_info.storage = HDATA.NP_TYPE_TO_HSTORAGE_TYPE[data.dtype]
        attrib_info.owner = HDATA.AttributeOwner.VERTEX
        self.part_info.vertex_attrib_count += 1
        self.attribs[(HDATA.AttributeOwner.VERTEX, name)] = (
         attrib_info, name, data)

    def add_prim_attrib(self, name, data):
        """Add prim attribute data to geo

        Args:
            name (str): name of the attribute
            data (ndarray(,)): Attribute data, should be 2D, 1st dims                equals number of faces, 2nd dim should be tuple size of this attribute
        """
        count, tuple_size = data.shape
        if count != self.face_count:
            print('AddPrimAttrib Error, Data length {0} not compatible with prim count {1}'.format(count, self.face_count))
            return
        attrib_info = HDATA.AttributeInfo()
        attrib_info.count = count
        attrib_info.tupleSize = tuple_size
        attrib_info.exists = True
        attrib_info.storage = HDATA.NP_TYPE_TO_HSTORAGE_TYPE[data.dtype]
        attrib_info.owner = HDATA.AttributeOwner.PRIM
        self.part_info.prim_attrib_count += 1
        self.attribs[(HDATA.AttributeOwner.PRIM, name)] = (
         attrib_info, name, data)

    def add_detail_attrib(self, name, data):
        """Add detail attribute data to geo

        Args:
            name (str): name of the attribute
            data (ndarray(,)): Attribute data, should be 2D, 1st dims                should be 1, 2nd dim should be tuple size of this attribute
        """
        count, tuple_size = data.shape
        if count != self.detail_count:
            print('add_detail_attrib Error, Data length {0} not compatible with detail count {1}'.format(count, self.detail_count))
            return
        attrib_info = HDATA.AttributeInfo()
        attrib_info.count = count
        attrib_info.tupleSize = tuple_size
        attrib_info.exists = True
        attrib_info.storage = HDATA.NP_TYPE_TO_HSTORAGE_TYPE[data.dtype]
        attrib_info.owner = HDATA.AttributeOwner.DETAIL
        self.part_info.detail_attrib_count += 1
        self.attribs[(HDATA.AttributeOwner.DETAIL, name)] = (
         attrib_info, name, data)

    def get_attrib_data(self, attrib_type, name):
        """Get attribute data of certain type and name

        Args:
            attrib_type (AttributeOwner): Type of querying attribute
            name (str): Name of querying attribute

        Returns:
            ndarray(,): Data of querying attribute
        """
        if (
         attrib_type, name) in self.attribs:
            _, _, data = self.attribs[(attrib_type, name)]
            return data

    def get_attrib_names(self):
        """Get all attribute name in this geo

        Returns:
            list((str,AttributeOwner)): All attributes containing in this geo
        """
        attrib_names = []
        for k, _ in self.attribs.items():
            attrib_type, name = k
            attrib_names.append([name, HDATA.AttributeOwner(attrib_type)])

        return attrib_names

    def commit_to_node(self, session, node_id):
        """Set this geo into hengine's node

        Args:
            session (int64): The session of Houdini you are interacting with.
            node_id (int): The node to add geo.
        """
        HAPI.set_part_info(session.hapi_session, node_id, self.part_info)
        for attrib_info, name, data in self.attribs.values():
            HAPI.add_attribute(session.hapi_session, node_id, name, attrib_info)
            HAPI.STORAGE_TYPE_TO_SET_ATTRIB[attrib_info.storage](session.hapi_session, node_id, name, attrib_info, data)

    def extract_from_sop(self, session, part_info, node_id, part_id=0):
        """Extract geometry from sop

        Args:
            session (int64): The session of Houdini you are interacting with.
            part_info (PartInfo): The info of part
            node_id (int): The node to add geo.
            part_id (int): Part id. Default to 0
        """
        self.part_info = part_info
        self.point_count = part_info.pointCount
        self.vertex_count = part_info.vertexCount
        self.face_count = part_info.faceCount
        for attrib_type in range(0, HDATA.AttributeOwner.MAX):
            attrib_names = HAPI.get_attribute_names(session.hapi_session, node_id, self.part_info, attrib_type)
            for attrib_name in attrib_names:
                if not attrib_name.startswith('__'):
                    attrib_info = HAPI.get_attribute_info(session.hapi_session, node_id, part_id, attrib_name, attrib_type)
                    data = HAPI.STORAGE_TYPE_TO_GET_ATTRIB[attrib_info.storage](session.hapi_session, node_id, part_id, attrib_name, attrib_info)
                    self.attribs[(attrib_type, attrib_name)] = (
                     attrib_info, attrib_name, data)


class HGeoMesh(HGeo):
    """HGeoMesh"""

    def __init__(self, vertices=None, faces=None):
        """Initialize

        Args:
            vertices (np.ndarray, optional): Verticed data, should be 2D:                (pount_count, 3). Defaults to None.
            faces (np.ndarray, optional): Faces data, should be in 2D such as                (face_count, vertex_each_face). Defaults to None.
        """
        super(HGeoMesh, self).__init__()
        if isinstance(vertices, np.ndarray):
            if isinstance(faces, np.ndarray):
                self.point_count = vertices.shape[0]
                self.vertex_count = faces.flatten().shape[0]
                self.face_count = faces.shape[0]
                self.faces = faces
                self.part_info.type = HDATA.PartType.MESH
                self.part_info.faceCount = self.face_count
                self.part_info.vertexCount = self.vertex_count
                self.part_info.pointCount = self.point_count
                self.add_attrib(HDATA.AttributeOwner.POINT, 'P', vertices)

    def extract_from_sop(self, session, part_info, node_id, part_id=0):
        """Extract mesh from sop

        Args:
            session (int64): The session of Houdini you are interacting with.
            part_info (PartInfo): The info of part
            node_id (int): The node to add geo.
            part_id (int): Part id. Default to 0
        """
        super().extract_from_sop(session, part_info, node_id, part_id)
        self.faces = HAPI.get_faces(session.hapi_session, node_id, part_info)

    def commit_to_node(self, session, node_id):
        super().commit_to_node(session, node_id)
        HAPI.set_vertex_list(session.hapi_session, node_id, self.faces)
        HAPI.set_face_counts(session.hapi_session, node_id, np.array([len(face) for face in self.faces]))
        HAPI.commit_geo(session.hapi_session, node_id)


class HGeoCurve(HGeo):
    """HGeoCurve"""

    def __init__(self, vertices=None, curve_knots=None, is_periodic=False, order=4, curve_type=HDATA.CurveType.LINEAR):
        """Initialize

        Args:
            vertices (ndarray): Position of curve cvs, should be in 2D (vertices_count, 3)
            curve_knots (ndarray, optional): Knots of cvs. Defaults to None.
            order (int, optional): Order of curve. Defaults to 4.
            curve_type (CurveType, optional): Type of curve.                 Defaults to HDATA.CurveType.LINEAR.
        """
        super(HGeoCurve, self).__init__()
        if isinstance(vertices, np.ndarray):
            self.point_count = vertices.shape[0]
            self.vertex_count = vertices.shape[0]
            self.face_count = 1
            self.curve_knots = curve_knots
            self.curve_count = np.repeat(vertices.shape[0], 1)
            self.part_info.type = HDATA.PartType.CURVE
            self.part_info.faceCount = self.face_count
            self.part_info.vertexCount = self.vertex_count
            self.part_info.pointCount = self.point_count
            self.curve_info = HDATA.CurveInfo()
            self.curve_info.curveType = curve_type
            self.curve_info.curveCount = 1
            self.curve_info.vertexCount = vertices.shape[0]
            self.curve_info.knotCount = curve_knots.shape[0] if isinstance(curve_knots, np.ndarray) else 0
            self.curve_info.isPeriodic = is_periodic
            self.curve_info.order = order
            self.curve_info.hasKnots = isinstance(curve_knots, np.ndarray)
            self.add_attrib(HDATA.AttributeOwner.POINT, 'P', vertices)

    def commit_to_node(self, session, node_id):
        super().commit_to_node(session, node_id)
        HAPI.set_curve_info(session.hapi_session, node_id, self.curve_info)
        HAPI.set_curve_counts(session.hapi_session, node_id, self.part_info.id, self.curve_count)
        HAPI.set_curve_knots(session.hapi_session, node_id, self.part_info.id, self.curve_knots)
        HAPI.commit_geo(session.hapi_session, node_id)

    def extract_from_sop(self, session, part_info, node_id, part_id=0):
        """Extract curve from sop

        Args:
            session (int64): The session of Houdini you are interacting with.
            part_info (PartInfo): The info of part
            node_id (int): The node to add geo.
            part_id (int): Part id. Default to 0
        """
        super().extract_from_sop(session, part_info, node_id, part_id)
        self.curve_info = HAPI.get_curve_info(session.hapi_session, node_id, part_info.id)
        self.point_count = self.curve_info.vertexCount
        self.vertex_count = self.curve_info.vertexCount
        self.face_count = self.curve_info.curveCount
        self.curve_count = HAPI.get_curve_counts(session.hapi_session, node_id, part_info.id, self.face_count)
        if self.curve_info.hasKnots:
            self.curve_knots = HAPI.get_curve_knots(session.hapi_session, node_id, part_info.id, self.curve_info.knotCount)


class HGeoVolume(HGeo):
    """HGeoVolume"""

    def __init__(self):
        super(HGeoVolume, self).__init__()

    def extract_from_sop(self, session, part_info, node_id, part_id=0):
        """Extract mesh from sop

        Args:
            session (int64): The session of Houdini you are interacting with.
            part_info (PartInfo): The info of part
            node_id (int): The node to add geo.
            part_id (int): Part id. Default to 0
        """
        super().extract_from_sop(session, part_info, node_id, part_id)

    def commit_to_node(self, session, node_id):
        super().commit_to_node(session, node_id)


class HGeoHeightfield(HGeo):
    """HGeoHeightfield"""

    def __init__(self, volume=None, volume_name='height', transform=None):
        """Initialize

        Args:
            vertices (np.ndarray, optional): Verticed data, should be 2D:                (pount_count, 3). Defaults to None.
            faces (np.ndarray, optional): Faces data, should be in 2D such as                (face_count, vertex_each_face). Defaults to None.
        """
        super(HGeoHeightfield, self).__init__()
        if isinstance(volume, np.ndarray):
            self.volume = volume
            self.volume_name = volume_name
            self.transform = transform
            self.xsize, self.ysize, self.tuple_size = volume.shape
            self.zsize = 1
            self.part_info.type = HDATA.PartType.VOLUME
            self.part_info.faceCount = 1
            self.part_info.vertexCount = 1
            self.part_info.pointCount = 1
            self.volume_info = HDATA.VolumeInfo()
            self.volume_info.xLength = self.xsize
            self.volume_info.yLength = self.ysize
            self.volume_info.zLength = self.zsize
            self.volume_info.tupleSize = self.tuple_size
            self.volume_info.tileSize = 8
            self.volume_info.type = HDATA.VolumeType.HOUDINI
            self.volume_info.storage = HDATA.StorageType.FLOAT if volume.dtype is np.dtype('float32') else HDATA.StorageType.INT
            if isinstance(transform, HDATA.Transform):
                self.volume_info.transform = transform
            else:
                tr = HDATA.Transform()
                tr.scale[0] = self.xsize
                tr.scale[1] = self.ysize
                tr.scale[2] = self.zsize / 2.0
                self.volume_info.transform = tr
                self.transform = tr

    def extract_from_sop(self, session, part_info, node_id, part_id=0):
        """Extract mesh from sop

        Args:
            session (int64): The session of Houdini you are interacting with.
            part_info (PartInfo): The info of part
            node_id (int): The node to add geo.
            part_id (int): Part id. Default to 0
        """
        super().extract_from_sop(session, part_info, node_id, part_id)
        self.volume_info = HAPI.get_volume_info(session.hapi_session, node_id, part_id)
        self.xsize = self.volume_info.xLength
        self.ysize = self.volume_info.yLength
        self.zsize = self.volume_info.zLength
        self.tuple_size = self.volume_info.tupleSize
        self.volume = HAPI.get_heightfield_data(session.hapi_session, node_id, part_id, self.volume_info)
        self.volume_name = HAPI.get_string(session.hapi_session, self.volume_info.nameSH)

    def commit_to_node--- This code section failed: ---

 L. 533         0  LOAD_GLOBAL              HAPI
                2  LOAD_METHOD              get_geo_info
                4  LOAD_FAST                'session'
                6  LOAD_ATTR                hapi_session
                8  LOAD_FAST                'node_id'
               10  CALL_METHOD_2         2  ''
               12  STORE_FAST               'geo_info'

 L. 534        14  LOAD_GLOBAL              HAPI
               16  LOAD_METHOD              get_volume_info
               18  LOAD_FAST                'session'
               20  LOAD_ATTR                hapi_session
               22  LOAD_FAST                'geo_info'
               24  LOAD_ATTR                nodeId
               26  LOAD_CONST               0
               28  CALL_METHOD_3         3  ''
               30  STORE_FAST               'volume_info'

 L. 536        32  LOAD_FAST                'volume_info'
               34  LOAD_ATTR                xLength
               36  LOAD_FAST                'self'
               38  LOAD_ATTR                xsize
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_FALSE    78  'to 78'
               44  LOAD_FAST                'volume_info'
               46  LOAD_ATTR                yLength
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                ysize
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    78  'to 78'

 L. 537        56  LOAD_FAST                'volume_info'
               58  LOAD_ATTR                zLength
               60  LOAD_CONST               1
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    78  'to 78'
               66  LOAD_FAST                'volume_info'
               68  LOAD_ATTR                tupleSize
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                tuple_size
               74  COMPARE_OP               ==
               76  POP_JUMP_IF_TRUE     82  'to 82'
             78_0  COME_FROM            64  '64'
             78_1  COME_FROM            54  '54'
             78_2  COME_FROM            42  '42'
               78  LOAD_ASSERT              AssertionError
               80  RAISE_VARARGS_1       1  ''
             82_0  COME_FROM            76  '76'

 L. 538        82  LOAD_CONST               1
               84  LOAD_FAST                'volume_info'
               86  STORE_ATTR               tileSize

 L. 539        88  LOAD_GLOBAL              HDATA
               90  LOAD_ATTR                VolumeType
               92  LOAD_ATTR                HOUDINI
               94  LOAD_FAST                'volume_info'
               96  STORE_ATTR               type

 L. 540        98  LOAD_FAST                'self'
              100  LOAD_ATTR                transform
              102  LOAD_FAST                'volume_info'
              104  STORE_ATTR               transform

 L. 541       106  LOAD_FAST                'volume_info'
              108  LOAD_FAST                'self'
              110  STORE_ATTR               volume_info

 L. 545       112  LOAD_GLOBAL              HAPI
              114  LOAD_METHOD              set_volume_info
              116  LOAD_FAST                'session'
              118  LOAD_ATTR                hapi_session
              120  LOAD_FAST                'geo_info'
              122  LOAD_ATTR                nodeId
              124  LOAD_CONST               0
              126  LOAD_FAST                'volume_info'
              128  CALL_METHOD_4         4  ''
              130  POP_TOP          

 L. 546       132  LOAD_GLOBAL              HAPI
              134  LOAD_METHOD              set_heightfield_data
              136  LOAD_FAST                'session'
              138  LOAD_ATTR                hapi_session
              140  LOAD_FAST                'node_id'
              142  LOAD_CONST               0
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                volume_name
              148  LOAD_FAST                'self'
              150  LOAD_ATTR                volume
              152  CALL_METHOD_5         5  ''
              154  POP_TOP          

 L. 547       156  LOAD_GLOBAL              HAPI
              158  LOAD_METHOD              commit_geo
              160  LOAD_FAST                'session'
              162  LOAD_ATTR                hapi_session
              164  LOAD_FAST                'node_id'
              166  CALL_METHOD_2         2  ''
              168  POP_TOP          

Parse error at or near `CALL_METHOD_2' instruction at offset 166