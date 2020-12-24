# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/mesh.py
# Compiled at: 2018-10-01 14:58:41
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
            (Visual.__init__)(self, vcode=shading_vertex_template, fcode=shading_fragment_template, **kwargs)
        else:
            (Visual.__init__)(self, vcode=vertex_template, fcode=fragment_template, **kwargs)
        self.set_gl_state('translucent', depth_test=True, cull_face=False)
        self._vertices = VertexBuffer(np.zeros((0, 3), dtype=(np.float32)))
        self._normals = None
        self._faces = IndexBuffer()
        self._colors = VertexBuffer(np.zeros((0, 4), dtype=(np.float32)))
        self._normals = VertexBuffer(np.zeros((0, 3), dtype=(np.float32)))
        self._color = Color(color)
        self._color_var = Varying('v_color', dtype='vec4')
        self._bounds = None
        MeshVisual.set_data(self, vertices=vertices, faces=faces, vertex_colors=vertex_colors,
          face_colors=face_colors,
          meshdata=meshdata,
          color=color)
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
            self._meshdata = MeshData(vertices=vertices, faces=faces, vertex_colors=vertex_colors,
              face_colors=face_colors)
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

    def _update_data--- This code section failed: ---

 L. 289         0  LOAD_FAST                'self'
                2  LOAD_ATTR                mesh_data
                4  STORE_FAST               'md'

 L. 291         6  LOAD_FAST                'self'
                8  LOAD_ATTR                shading
               10  LOAD_STR                 'smooth'
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_FALSE   246  'to 246'
               16  LOAD_FAST                'md'
               18  LOAD_METHOD              has_face_indexed_data
               20  CALL_METHOD_0         0  '0 positional arguments'
               22  POP_JUMP_IF_TRUE    246  'to 246'

 L. 292        24  LOAD_FAST                'md'
               26  LOAD_METHOD              get_vertices
               28  CALL_METHOD_0         0  '0 positional arguments'
               30  STORE_FAST               'v'

 L. 293        32  LOAD_FAST                'v'
               34  LOAD_CONST               None
               36  COMPARE_OP               is
               38  POP_JUMP_IF_FALSE    44  'to 44'

 L. 294        40  LOAD_CONST               False
               42  RETURN_VALUE     
             44_0  COME_FROM            38  '38'

 L. 295        44  LOAD_FAST                'v'
               46  LOAD_ATTR                shape
               48  LOAD_CONST               -1
               50  BINARY_SUBSCR    
               52  LOAD_CONST               2
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE    94  'to 94'

 L. 296        58  LOAD_GLOBAL              np
               60  LOAD_METHOD              concatenate
               62  LOAD_FAST                'v'
               64  LOAD_GLOBAL              np
               66  LOAD_METHOD              zeros
               68  LOAD_FAST                'v'
               70  LOAD_ATTR                shape
               72  LOAD_CONST               None
               74  LOAD_CONST               -1
               76  BUILD_SLICE_2         2 
               78  BINARY_SUBSCR    
               80  LOAD_CONST               (1,)
               82  BINARY_ADD       
               84  CALL_METHOD_1         1  '1 positional argument'
               86  BUILD_TUPLE_2         2 
               88  LOAD_CONST               -1
               90  CALL_METHOD_2         2  '2 positional arguments'
               92  STORE_FAST               'v'
             94_0  COME_FROM            56  '56'

 L. 297        94  LOAD_FAST                'self'
               96  LOAD_ATTR                _vertices
               98  LOAD_ATTR                set_data
              100  LOAD_FAST                'v'
              102  LOAD_CONST               True
              104  LOAD_CONST               ('convert',)
              106  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              108  POP_TOP          

 L. 298       110  LOAD_FAST                'self'
              112  LOAD_ATTR                _normals
              114  LOAD_ATTR                set_data
              116  LOAD_FAST                'md'
              118  LOAD_METHOD              get_vertex_normals
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  LOAD_CONST               True
              124  LOAD_CONST               ('convert',)
              126  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              128  POP_TOP          

 L. 299       130  LOAD_FAST                'self'
              132  LOAD_ATTR                _faces
              134  LOAD_ATTR                set_data
              136  LOAD_FAST                'md'
              138  LOAD_METHOD              get_faces
              140  CALL_METHOD_0         0  '0 positional arguments'
              142  LOAD_CONST               True
              144  LOAD_CONST               ('convert',)
              146  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              148  POP_TOP          

 L. 300       150  LOAD_FAST                'self'
              152  LOAD_ATTR                _faces
              154  LOAD_FAST                'self'
              156  STORE_ATTR               _index_buffer

 L. 301       158  LOAD_FAST                'md'
              160  LOAD_METHOD              has_vertex_color
              162  CALL_METHOD_0         0  '0 positional arguments'
              164  POP_JUMP_IF_FALSE   188  'to 188'

 L. 302       166  LOAD_FAST                'self'
              168  LOAD_ATTR                _colors
              170  LOAD_ATTR                set_data
              172  LOAD_FAST                'md'
              174  LOAD_METHOD              get_vertex_colors
              176  CALL_METHOD_0         0  '0 positional arguments'
              178  LOAD_CONST               True
              180  LOAD_CONST               ('convert',)
              182  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              184  POP_TOP          
              186  JUMP_FORWARD        550  'to 550'
            188_0  COME_FROM           164  '164'

 L. 303       188  LOAD_FAST                'md'
              190  LOAD_METHOD              has_face_color
              192  CALL_METHOD_0         0  '0 positional arguments'
              194  POP_JUMP_IF_FALSE   218  'to 218'

 L. 304       196  LOAD_FAST                'self'
              198  LOAD_ATTR                _colors
              200  LOAD_ATTR                set_data
              202  LOAD_FAST                'md'
              204  LOAD_METHOD              get_face_colors
              206  CALL_METHOD_0         0  '0 positional arguments'
              208  LOAD_CONST               True
              210  LOAD_CONST               ('convert',)
              212  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              214  POP_TOP          
              216  JUMP_FORWARD        550  'to 550'
            218_0  COME_FROM           194  '194'

 L. 306       218  LOAD_FAST                'self'
              220  LOAD_ATTR                _colors
              222  LOAD_METHOD              set_data
              224  LOAD_GLOBAL              np
              226  LOAD_ATTR                zeros
              228  LOAD_CONST               (0, 4)
              230  LOAD_GLOBAL              np
              232  LOAD_ATTR                float32
              234  LOAD_CONST               ('dtype',)
              236  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              238  CALL_METHOD_1         1  '1 positional argument'
              240  POP_TOP          
          242_244  JUMP_FORWARD        550  'to 550'
            246_0  COME_FROM            22  '22'
            246_1  COME_FROM            14  '14'

 L. 308       246  LOAD_FAST                'md'
              248  LOAD_ATTR                get_vertices
              250  LOAD_STR                 'faces'
              252  LOAD_CONST               ('indexed',)
              254  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              256  STORE_FAST               'v'

 L. 309       258  LOAD_FAST                'v'
              260  LOAD_CONST               None
              262  COMPARE_OP               is
          264_266  POP_JUMP_IF_FALSE   272  'to 272'

 L. 310       268  LOAD_CONST               False
              270  RETURN_VALUE     
            272_0  COME_FROM           264  '264'

 L. 311       272  LOAD_FAST                'v'
              274  LOAD_ATTR                shape
              276  LOAD_CONST               -1
              278  BINARY_SUBSCR    
              280  LOAD_CONST               2
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_FALSE   324  'to 324'

 L. 312       288  LOAD_GLOBAL              np
              290  LOAD_METHOD              concatenate
              292  LOAD_FAST                'v'
              294  LOAD_GLOBAL              np
              296  LOAD_METHOD              zeros
              298  LOAD_FAST                'v'
              300  LOAD_ATTR                shape
              302  LOAD_CONST               None
              304  LOAD_CONST               -1
              306  BUILD_SLICE_2         2 
              308  BINARY_SUBSCR    
              310  LOAD_CONST               (1,)
              312  BINARY_ADD       
              314  CALL_METHOD_1         1  '1 positional argument'
              316  BUILD_TUPLE_2         2 
              318  LOAD_CONST               -1
              320  CALL_METHOD_2         2  '2 positional arguments'
              322  STORE_FAST               'v'
            324_0  COME_FROM           284  '284'

 L. 313       324  LOAD_FAST                'self'
              326  LOAD_ATTR                _vertices
              328  LOAD_ATTR                set_data
              330  LOAD_FAST                'v'
              332  LOAD_CONST               True
              334  LOAD_CONST               ('convert',)
              336  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              338  POP_TOP          

 L. 314       340  LOAD_FAST                'self'
              342  LOAD_ATTR                shading
              344  LOAD_STR                 'smooth'
              346  COMPARE_OP               ==
          348_350  POP_JUMP_IF_FALSE   382  'to 382'

 L. 315       352  LOAD_FAST                'md'
              354  LOAD_ATTR                get_vertex_normals
              356  LOAD_STR                 'faces'
              358  LOAD_CONST               ('indexed',)
              360  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              362  STORE_FAST               'normals'

 L. 316       364  LOAD_FAST                'self'
              366  LOAD_ATTR                _normals
              368  LOAD_ATTR                set_data
              370  LOAD_FAST                'normals'
              372  LOAD_CONST               True
              374  LOAD_CONST               ('convert',)
              376  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              378  POP_TOP          
              380  JUMP_FORWARD        448  'to 448'
            382_0  COME_FROM           348  '348'

 L. 317       382  LOAD_FAST                'self'
              384  LOAD_ATTR                shading
              386  LOAD_STR                 'flat'
              388  COMPARE_OP               ==
          390_392  POP_JUMP_IF_FALSE   424  'to 424'

 L. 318       394  LOAD_FAST                'md'
              396  LOAD_ATTR                get_face_normals
              398  LOAD_STR                 'faces'
              400  LOAD_CONST               ('indexed',)
              402  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              404  STORE_FAST               'normals'

 L. 319       406  LOAD_FAST                'self'
              408  LOAD_ATTR                _normals
              410  LOAD_ATTR                set_data
              412  LOAD_FAST                'normals'
              414  LOAD_CONST               True
              416  LOAD_CONST               ('convert',)
              418  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              420  POP_TOP          
              422  JUMP_FORWARD        448  'to 448'
            424_0  COME_FROM           390  '390'

 L. 321       424  LOAD_FAST                'self'
              426  LOAD_ATTR                _normals
              428  LOAD_METHOD              set_data
              430  LOAD_GLOBAL              np
              432  LOAD_ATTR                zeros
              434  LOAD_CONST               (0, 3)
              436  LOAD_GLOBAL              np
              438  LOAD_ATTR                float32
              440  LOAD_CONST               ('dtype',)
              442  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              444  CALL_METHOD_1         1  '1 positional argument'
              446  POP_TOP          
            448_0  COME_FROM           422  '422'
            448_1  COME_FROM           380  '380'

 L. 322       448  LOAD_CONST               None
              450  LOAD_FAST                'self'
              452  STORE_ATTR               _index_buffer

 L. 323       454  LOAD_FAST                'md'
              456  LOAD_METHOD              has_vertex_color
              458  CALL_METHOD_0         0  '0 positional arguments'
          460_462  POP_JUMP_IF_FALSE   490  'to 490'

 L. 324       464  LOAD_FAST                'self'
              466  LOAD_ATTR                _colors
              468  LOAD_ATTR                set_data
              470  LOAD_FAST                'md'
              472  LOAD_ATTR                get_vertex_colors
              474  LOAD_STR                 'faces'
              476  LOAD_CONST               ('indexed',)
              478  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 325       480  LOAD_CONST               True
              482  LOAD_CONST               ('convert',)
              484  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              486  POP_TOP          
              488  JUMP_FORWARD        550  'to 550'
            490_0  COME_FROM           460  '460'

 L. 326       490  LOAD_FAST                'md'
            492_0  COME_FROM           186  '186'
              492  LOAD_METHOD              has_face_color
              494  CALL_METHOD_0         0  '0 positional arguments'
          496_498  POP_JUMP_IF_FALSE   526  'to 526'

 L. 327       500  LOAD_FAST                'self'
              502  LOAD_ATTR                _colors
              504  LOAD_ATTR                set_data
              506  LOAD_FAST                'md'
              508  LOAD_ATTR                get_face_colors
              510  LOAD_STR                 'faces'
              512  LOAD_CONST               ('indexed',)
              514  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'

 L. 328       516  LOAD_CONST               True
              518  LOAD_CONST               ('convert',)
              520  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
            522_0  COME_FROM           216  '216'
              522  POP_TOP          
              524  JUMP_FORWARD        550  'to 550'
            526_0  COME_FROM           496  '496'

 L. 330       526  LOAD_FAST                'self'
              528  LOAD_ATTR                _colors
              530  LOAD_METHOD              set_data
              532  LOAD_GLOBAL              np
              534  LOAD_ATTR                zeros
              536  LOAD_CONST               (0, 4)
              538  LOAD_GLOBAL              np
              540  LOAD_ATTR                float32
              542  LOAD_CONST               ('dtype',)
              544  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              546  CALL_METHOD_1         1  '1 positional argument'
              548  POP_TOP          
            550_0  COME_FROM           524  '524'
            550_1  COME_FROM           488  '488'
            550_2  COME_FROM           242  '242'

 L. 331       550  LOAD_FAST                'self'
              552  LOAD_ATTR                _vertices
              554  LOAD_FAST                'self'
              556  LOAD_ATTR                shared_program
              558  LOAD_ATTR                vert
              560  LOAD_STR                 'position'
              562  STORE_SUBSCR     

 L. 334       564  LOAD_FAST                'v'
              566  LOAD_ATTR                shape
              568  LOAD_CONST               -1
              570  BINARY_SUBSCR    
              572  LOAD_CONST               2
              574  COMPARE_OP               ==
          576_578  POP_JUMP_IF_FALSE   594  'to 594'

 L. 335       580  LOAD_GLOBAL              vec2to4
              582  LOAD_FAST                'self'
              584  LOAD_ATTR                shared_program
              586  LOAD_ATTR                vert
              588  LOAD_STR                 'to_vec4'
              590  STORE_SUBSCR     
              592  JUMP_FORWARD        632  'to 632'
            594_0  COME_FROM           576  '576'

 L. 336       594  LOAD_FAST                'v'
              596  LOAD_ATTR                shape
              598  LOAD_CONST               -1
              600  BINARY_SUBSCR    
              602  LOAD_CONST               3
              604  COMPARE_OP               ==
          606_608  POP_JUMP_IF_FALSE   624  'to 624'

 L. 337       610  LOAD_GLOBAL              vec3to4
              612  LOAD_FAST                'self'
              614  LOAD_ATTR                shared_program
              616  LOAD_ATTR                vert
              618  LOAD_STR                 'to_vec4'
              620  STORE_SUBSCR     
              622  JUMP_FORWARD        632  'to 632'
            624_0  COME_FROM           606  '606'

 L. 339       624  LOAD_GLOBAL              TypeError
              626  LOAD_STR                 'Vertex data must have shape (...,2) or (...,3).'
              628  CALL_FUNCTION_1       1  '1 positional argument'
              630  RAISE_VARARGS_1       1  'exception instance'
            632_0  COME_FROM           622  '622'
            632_1  COME_FROM           592  '592'

 L. 345       632  LOAD_FAST                'self'
              634  LOAD_ATTR                _colors
              636  LOAD_ATTR                size
              638  LOAD_CONST               0
              640  COMPARE_OP               >
          642_644  POP_JUMP_IF_FALSE   652  'to 652'
              646  LOAD_FAST                'self'
              648  LOAD_ATTR                _colors
              650  JUMP_FORWARD        658  'to 658'
            652_0  COME_FROM           642  '642'
              652  LOAD_FAST                'self'
              654  LOAD_ATTR                _color
              656  LOAD_ATTR                rgba
            658_0  COME_FROM           650  '650'
              658  STORE_FAST               'colors'

 L. 346       660  LOAD_FAST                'self'
              662  LOAD_ATTR                shading
              664  LOAD_CONST               None
              666  COMPARE_OP               is
          668_670  POP_JUMP_IF_FALSE   686  'to 686'

 L. 347       672  LOAD_FAST                'colors'
              674  LOAD_FAST                'self'
              676  LOAD_ATTR                shared_program
              678  LOAD_ATTR                vert
              680  LOAD_FAST                'self'
              682  LOAD_ATTR                _color_var
              684  STORE_SUBSCR     
            686_0  COME_FROM           668  '668'

 L. 350       686  LOAD_FAST                'self'
              688  LOAD_ATTR                shading
              690  LOAD_CONST               None
              692  COMPARE_OP               is
          694_696  POP_JUMP_IF_FALSE   714  'to 714'

 L. 351       698  LOAD_FAST                'self'
              700  LOAD_ATTR                _color_var
              702  LOAD_FAST                'self'
              704  LOAD_ATTR                shared_program
              706  LOAD_ATTR                frag
              708  LOAD_STR                 'color'
              710  STORE_SUBSCR     
              712  JUMP_FORWARD        800  'to 800'
            714_0  COME_FROM           694  '694'

 L. 354       714  LOAD_FAST                'self'
              716  LOAD_ATTR                _normals
              718  LOAD_ATTR                size
              720  LOAD_CONST               0
              722  COMPARE_OP               >
          724_726  POP_JUMP_IF_FALSE   736  'to 736'

 L. 355       728  LOAD_FAST                'self'
              730  LOAD_ATTR                _normals
              732  STORE_FAST               'normals'
              734  JUMP_FORWARD        740  'to 740'
            736_0  COME_FROM           724  '724'

 L. 357       736  LOAD_CONST               (1.0, 0.0, 0.0)
              738  STORE_FAST               'normals'
            740_0  COME_FROM           734  '734'

 L. 359       740  LOAD_FAST                'normals'
              742  LOAD_FAST                'self'
              744  LOAD_ATTR                shared_program
              746  LOAD_ATTR                vert
              748  LOAD_STR                 'normal'
              750  STORE_SUBSCR     

 L. 360       752  LOAD_FAST                'colors'
              754  LOAD_FAST                'self'
              756  LOAD_ATTR                shared_program
              758  LOAD_ATTR                vert
              760  LOAD_STR                 'base_color'
              762  STORE_SUBSCR     

 L. 363       764  LOAD_CONST               (10, 5, -5)
              766  LOAD_FAST                'self'
              768  LOAD_ATTR                shared_program
              770  LOAD_ATTR                vert
              772  LOAD_STR                 'light_dir'
              774  STORE_SUBSCR     

 L. 364       776  LOAD_CONST               (1.0, 1.0, 1.0, 1.0)
              778  LOAD_FAST                'self'
              780  LOAD_ATTR                shared_program
              782  LOAD_ATTR                vert
              784  LOAD_STR                 'light_color'
              786  STORE_SUBSCR     

 L. 365       788  LOAD_CONST               (0.3, 0.3, 0.3, 1.0)
              790  LOAD_FAST                'self'
              792  LOAD_ATTR                shared_program
              794  LOAD_ATTR                vert
              796  LOAD_STR                 'ambientk'
              798  STORE_SUBSCR     
            800_0  COME_FROM           712  '712'

 L. 367       800  LOAD_CONST               False
              802  LOAD_FAST                'self'
              804  STORE_ATTR               _data_changed

Parse error at or near `LOAD_METHOD' instruction at offset 492

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
        (Visual.draw)(self, *args, **kwds)

    @staticmethod
    def _prepare_transforms(view):
        tr = view.transforms.get_transform()
        view.view_program.vert['transform'] = tr
        if view.shading is not None:
            visual2scene = view.transforms.get_transform'visual''scene'
            scene2doc = view.transforms.get_transform'scene''document'
            doc2scene = view.transforms.get_transform'document''scene'
            view.shared_program.vert['visual2scene'] = visual2scene
            view.shared_program.vert['scene2doc'] = scene2doc
            view.shared_program.vert['doc2scene'] = doc2scene

    def _compute_bounds(self, axis, view):
        if self._bounds is None:
            return
        return self._bounds[axis]