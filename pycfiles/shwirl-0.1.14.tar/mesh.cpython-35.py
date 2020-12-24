# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/visuals/mesh.py
# Compiled at: 2017-04-05 22:13:00
# Size of source mod 2**32: 12965 bytes
""" A MeshVisual Visual that uses the new shader Function.
"""
from __future__ import division
import numpy as np
from .visual import Visual
from .shaders import Function, Varying
from ..gloo import VertexBuffer, IndexBuffer
from ..geometry import MeshData
from ..color import Color
shading_vertex_template = '\nvarying vec3 v_normal_vec;\nvarying vec3 v_light_vec;\nvarying vec3 v_eye_vec;\n\nvarying vec4 v_ambientk;\nvarying vec4 v_light_color;\nvarying vec4 v_base_color;\n\n\nvoid main() {\n\n    v_ambientk = $ambientk;\n    v_light_color = $light_color;\n    v_base_color = $base_color;\n\n\n    vec4 pos_scene = $visual2scene($to_vec4($position));\n    vec4 normal_scene = $visual2scene(vec4($normal, 1.0));\n    vec4 origin_scene = $visual2scene(vec4(0.0, 0.0, 0.0, 1.0));\n\n    normal_scene /= normal_scene.w;\n    origin_scene /= origin_scene.w;\n\n    vec3 normal = normalize(normal_scene.xyz - origin_scene.xyz);\n    v_normal_vec = normal; //VARYING COPY\n\n    vec4 pos_front = $scene2doc(pos_scene);\n    pos_front.z += 0.01;\n    pos_front = $doc2scene(pos_front);\n    pos_front /= pos_front.w;\n\n    vec4 pos_back = $scene2doc(pos_scene);\n    pos_back.z -= 0.01;\n    pos_back = $doc2scene(pos_back);\n    pos_back /= pos_back.w;\n\n    vec3 eye = normalize(pos_front.xyz - pos_back.xyz);\n    v_eye_vec = eye; //VARYING COPY\n\n    vec3 light = normalize($light_dir.xyz);\n    v_light_vec = light; //VARYING COPY\n\n    gl_Position = $transform($to_vec4($position));\n}\n'
shading_fragment_template = "\nvarying vec3 v_normal_vec;\nvarying vec3 v_light_vec;\nvarying vec3 v_eye_vec;\n\nvarying vec4 v_ambientk;\nvarying vec4 v_light_color;\nvarying vec4 v_base_color;\n\nvoid main() {\n\n\n    //DIFFUSE\n    float diffusek = dot(v_light_vec, v_normal_vec);\n    //clamp, because 0 < theta < pi/2\n    diffusek  = clamp(diffusek, 0.0, 1.0);\n    vec4 diffuse_color = v_light_color * diffusek;\n    //diffuse_color.a = 1.0;\n\n    //SPECULAR\n    //reflect light wrt normal for the reflected ray, then\n    //find the angle made with the eye\n    float speculark = dot(reflect(v_light_vec, v_normal_vec), v_eye_vec);\n    speculark = clamp(speculark, 0.0, 1.0);\n    //raise to the material's shininess, multiply with a\n    //small factor for spread\n    speculark = 20.0 * pow(speculark, 200.0);\n\n    vec4 specular_color = v_light_color * speculark;\n\n\n    gl_FragColor =\n       v_base_color * (v_ambientk + diffuse_color) + specular_color;\n\n    //gl_FragColor = vec4(speculark, 0, 1, 1.0);\n\n\n}\n"
vertex_template = '\nvoid main() {\n    gl_Position = $transform($to_vec4($position));\n}\n'
fragment_template = '\nvoid main() {\n    gl_FragColor = $color;\n}\n'
vec3to4 = Function('\nvec4 vec3to4(vec3 xyz) {\n    return vec4(xyz, 1.0);\n}\n')
vec2to4 = Function('\nvec4 vec2to4(vec2 xyz) {\n    return vec4(xyz, 0.0, 1.0);\n}\n')

class MeshVisual(Visual):
    __doc__ = 'Mesh visual\n\n    Parameters\n    ----------\n    vertices : array-like | None\n        The vertices.\n    faces : array-like | None\n        The faces.\n    vertex_colors : array-like | None\n        Colors to use for each vertex.\n    face_colors : array-like | None\n        Colors to use for each face.\n    color : instance of Color\n        The color to use.\n    meshdata : instance of MeshData | None\n        The meshdata.\n    shading : str | None\n        Shading to use.\n    mode : str\n        The drawing mode.\n    **kwargs : dict\n        Keyword arguments to pass to `Visual`.\n    '

    def __init__(self, vertices=None, faces=None, vertex_colors=None, face_colors=None, color=(0.5, 0.5, 1, 1), meshdata=None, shading=None, mode='triangles', **kwargs):
        self.shading = shading
        if shading is not None:
            Visual.__init__(self, vcode=shading_vertex_template, fcode=shading_fragment_template, **kwargs)
        else:
            Visual.__init__(self, vcode=vertex_template, fcode=fragment_template, **kwargs)
        self.set_gl_state('translucent', depth_test=True, cull_face=False)
        self._vertices = VertexBuffer(np.zeros((0, 3), dtype=np.float32))
        self._normals = None
        self._faces = IndexBuffer()
        self._colors = VertexBuffer(np.zeros((0, 4), dtype=np.float32))
        self._normals = VertexBuffer(np.zeros((0, 3), dtype=np.float32))
        self._color = Color(color)
        self._color_var = Varying('v_color', dtype='vec4')
        self._bounds = None
        MeshVisual.set_data(self, vertices=vertices, faces=faces, vertex_colors=vertex_colors, face_colors=face_colors, meshdata=meshdata, color=color)
        self._draw_mode = mode
        self.freeze()

    def set_data(self, vertices=None, faces=None, vertex_colors=None, face_colors=None, color=None, meshdata=None):
        """Set the mesh data

        Parameters
        ----------
        vertices : array-like | None
            The vertices.
        faces : array-like | None
            The faces.
        vertex_colors : array-like | None
            Colors to use for each vertex.
        face_colors : array-like | None
            Colors to use for each face.
        color : instance of Color
            The color to use.
        meshdata : instance of MeshData | None
            The meshdata.
        """
        if meshdata is not None:
            self._meshdata = meshdata
        else:
            self._meshdata = MeshData(vertices=vertices, faces=faces, vertex_colors=vertex_colors, face_colors=face_colors)
        self._bounds = self._meshdata.get_bounds()
        if color is not None:
            self._color = Color(color)
        self.mesh_data_changed()

    @property
    def mode(self):
        """The triangle mode used to draw this mesh.

        Options are:

            * 'triangles': Draw one triangle for every three vertices
              (eg, [1,2,3], [4,5,6], [7,8,9)
            * 'triangle_strip': Draw one strip for every vertex excluding the
              first two (eg, [1,2,3], [2,3,4], [3,4,5])
            * 'triangle_fan': Draw each triangle from the first vertex and the
              last two vertices (eg, [1,2,3], [1,3,4], [1,4,5])
        """
        return self._draw_mode

    @mode.setter
    def mode(self, m):
        modes = ['triangles', 'triangle_strip', 'triangle_fan']
        if m not in modes:
            raise ValueError('Mesh mode must be one of %s' % ', '.join(modes))
        self._draw_mode = m

    @property
    def mesh_data(self):
        """The mesh data"""
        return self._meshdata

    @property
    def color(self):
        """The uniform color for this mesh.

        This value is only used if per-vertex or per-face colors are not
        specified.
        """
        return self._color

    @color.setter
    def color(self, c):
        if c is not None:
            self._color = Color(c)
        self.mesh_data_changed()

    def mesh_data_changed(self):
        self._data_changed = True
        self.update()

    def _update_data(self):
        md = self.mesh_data
        if self.shading == 'smooth' and not md.has_face_indexed_data():
            v = md.get_vertices()
            if v is None:
                return False
            if v.shape[(-1)] == 2:
                v = np.concatenate((v, np.zeros(v.shape[:-1] + (1, ))), -1)
            self._vertices.set_data(v, convert=True)
            self._normals.set_data(md.get_vertex_normals(), convert=True)
            self._faces.set_data(md.get_faces(), convert=True)
            self._index_buffer = self._faces
            if md.has_vertex_color():
                self._colors.set_data(md.get_vertex_colors(), convert=True)
            else:
                if md.has_face_color():
                    self._colors.set_data(md.get_face_colors(), convert=True)
                else:
                    self._colors.set_data(np.zeros((0, 4), dtype=np.float32))
        else:
            v = md.get_vertices(indexed='faces')
            if v is None:
                return False
            if v.shape[(-1)] == 2:
                v = np.concatenate((v, np.zeros(v.shape[:-1] + (1, ))), -1)
            self._vertices.set_data(v, convert=True)
            if self.shading == 'smooth':
                normals = md.get_vertex_normals(indexed='faces')
                self._normals.set_data(normals, convert=True)
            else:
                if self.shading == 'flat':
                    normals = md.get_face_normals(indexed='faces')
                    self._normals.set_data(normals, convert=True)
                else:
                    self._normals.set_data(np.zeros((0, 3), dtype=np.float32))
                self._index_buffer = None
                if md.has_vertex_color():
                    self._colors.set_data(md.get_vertex_colors(indexed='faces'), convert=True)
                else:
                    if md.has_face_color():
                        self._colors.set_data(md.get_face_colors(indexed='faces'), convert=True)
                    else:
                        self._colors.set_data(np.zeros((0, 4), dtype=np.float32))
        self.shared_program.vert['position'] = self._vertices
        if v.shape[(-1)] == 2:
            self.shared_program.vert['to_vec4'] = vec2to4
        else:
            if v.shape[(-1)] == 3:
                self.shared_program.vert['to_vec4'] = vec3to4
            else:
                raise TypeError('Vertex data must have shape (...,2) or (...,3).')
            colors = self._colors if self._colors.size > 0 else self._color.rgba
            if self.shading is None:
                self.shared_program.vert[self._color_var] = colors
            if self.shading is None:
                self.shared_program.frag['color'] = self._color_var
            else:
                if self._normals.size > 0:
                    normals = self._normals
                else:
                    normals = (1.0, 0.0, 0.0)
                self.shared_program.vert['normal'] = normals
                self.shared_program.vert['base_color'] = colors
                self.shared_program.vert['light_dir'] = (10, 5, -5)
                self.shared_program.vert['light_color'] = (1.0, 1.0, 1.0, 1.0)
                self.shared_program.vert['ambientk'] = (0.3, 0.3, 0.3, 1.0)
        self._data_changed = False

    @property
    def shading(self):
        """ The shading method used.
        """
        return self._shading

    @shading.setter
    def shading(self, value):
        assert value in (None, 'flat', 'smooth')
        self._shading = value

    def _prepare_draw(self, view):
        if self._data_changed:
            if self._update_data() is False:
                return False
            self._data_changed = False

    def draw(self, *args, **kwds):
        Visual.draw(self, *args, **kwds)

    @staticmethod
    def _prepare_transforms(view):
        tr = view.transforms.get_transform()
        view.view_program.vert['transform'] = tr
        if view.shading is not None:
            visual2scene = view.transforms.get_transform('visual', 'scene')
            scene2doc = view.transforms.get_transform('scene', 'document')
            doc2scene = view.transforms.get_transform('document', 'scene')
            view.shared_program.vert['visual2scene'] = visual2scene
            view.shared_program.vert['scene2doc'] = scene2doc
            view.shared_program.vert['doc2scene'] = doc2scene

    def _compute_bounds(self, axis, view):
        if self._bounds is None:
            return
        return self._bounds[axis]