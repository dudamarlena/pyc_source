# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/visuals/volume.py
# Compiled at: 2016-11-03 01:40:19
"""
About this technique
--------------------

In Python, we define the six faces of a cuboid to draw, as well as
texture cooridnates corresponding with the vertices of the cuboid. 
The back faces of the cuboid are drawn (and front faces are culled)
because only the back faces are visible when the camera is inside the 
volume.

In the vertex shader, we intersect the view ray with the near and far 
clipping planes. In the fragment shader, we use these two points to
compute the ray direction and then compute the position of the front
cuboid surface (or near clipping plane) along the view ray.

Next we calculate the number of steps to walk from the front surface
to the back surface and iterate over these positions in a for-loop.
At each iteration, the fragment color or other voxel information is 
updated depending on the selected rendering method.

It is important for the texture interpolation is 'linear', since with
nearest the result look very ugly. The wrapping should be clamp_to_edge
to avoid artifacts when the ray takes a small step outside the volume.

The ray direction is established by mapping the vertex to the document
coordinate frame, adjusting z to +/-1, and mapping the coordinate back.
The ray is expressed in coordinates local to the volume (i.e. texture
coordinates).

"""
from ..gloo import Texture3D, TextureEmulated3D, VertexBuffer, IndexBuffer
from . import Visual
from .shaders import Function
from ..color import get_colormap
import numpy as np
VERT_SHADER = '\nattribute vec3 a_position;\n// attribute vec3 a_texcoord;\nuniform vec3 u_shape;\n\n// varying vec3 v_texcoord;\nvarying vec3 v_position;\nvarying vec4 v_nearpos;\nvarying vec4 v_farpos;\n\nvoid main() {\n    // v_texcoord = a_texcoord;\n    v_position = a_position;\n    \n    // Project local vertex coordinate to camera position. Then do a step\n    // backward (in cam coords) and project back. Voila, we get our ray vector.\n    vec4 pos_in_cam = $viewtransformf(vec4(v_position, 1));\n\n    // intersection of ray and near clipping plane (z = -1 in clip coords)\n    pos_in_cam.z = -pos_in_cam.w;\n    v_nearpos = $viewtransformi(pos_in_cam);\n    \n    // intersection of ray and far clipping plane (z = +1 in clip coords)\n    pos_in_cam.z = pos_in_cam.w;\n    v_farpos = $viewtransformi(pos_in_cam);\n    \n    gl_Position = $transform(vec4(v_position, 1.0));\n}\n'
FRAG_SHADER = '\n// uniforms\nuniform $sampler_type u_volumetex;\nuniform vec3 u_shape;\nuniform float u_threshold;\nuniform float u_relative_step_size;\n\n//varyings\n// varying vec3 v_texcoord;\nvarying vec3 v_position;\nvarying vec4 v_nearpos;\nvarying vec4 v_farpos;\n\n// uniforms for lighting. Hard coded until we figure out how to do lights\nconst vec4 u_ambient = vec4(0.2, 0.4, 0.2, 1.0);\nconst vec4 u_diffuse = vec4(0.8, 0.2, 0.2, 1.0);\nconst vec4 u_specular = vec4(1.0, 1.0, 1.0, 1.0);\nconst float u_shininess = 40.0;\n\n//varying vec3 lightDirs[1];\n\n// global holding view direction in local coordinates\nvec3 view_ray;\n\nfloat rand(vec2 co)\n{{\n    // Create a pseudo-random number between 0 and 1.\n    // http://stackoverflow.com/questions/4200224\n    return fract(sin(dot(co.xy ,vec2(12.9898, 78.233))) * 43758.5453);\n}}\n\nfloat colorToVal(vec4 color1)\n{{\n    return color1.g; // todo: why did I have this abstraction in visvis?\n}}\n\nvec4 calculateColor(vec4 betterColor, vec3 loc, vec3 step)\n{{   \n    // Calculate color by incorporating lighting\n    vec4 color1;\n    vec4 color2;\n    \n    // View direction\n    vec3 V = normalize(view_ray);\n    \n    // calculate normal vector from gradient\n    vec3 N; // normal\n    color1 = $sample( u_volumetex, loc+vec3(-step[0],0.0,0.0) );\n    color2 = $sample( u_volumetex, loc+vec3(step[0],0.0,0.0) );\n    N[0] = colorToVal(color1) - colorToVal(color2);\n    betterColor = max(max(color1, color2),betterColor);\n    color1 = $sample( u_volumetex, loc+vec3(0.0,-step[1],0.0) );\n    color2 = $sample( u_volumetex, loc+vec3(0.0,step[1],0.0) );\n    N[1] = colorToVal(color1) - colorToVal(color2);\n    betterColor = max(max(color1, color2),betterColor);\n    color1 = $sample( u_volumetex, loc+vec3(0.0,0.0,-step[2]) );\n    color2 = $sample( u_volumetex, loc+vec3(0.0,0.0,step[2]) );\n    N[2] = colorToVal(color1) - colorToVal(color2);\n    betterColor = max(max(color1, color2),betterColor);\n    float gm = length(N); // gradient magnitude\n    N = normalize(N);\n    \n    // Flip normal so it points towards viewer\n    float Nselect = float(dot(N,V) > 0.0);\n    N = (2.0*Nselect - 1.0) * N;  // ==  Nselect * N - (1.0-Nselect)*N;\n    \n    // Get color of the texture (albeido)\n    color1 = betterColor;\n    color2 = color1;\n    // todo: parametrise color1_to_color2\n    \n    // Init colors\n    vec4 ambient_color = vec4(0.0, 0.0, 0.0, 0.0);\n    vec4 diffuse_color = vec4(0.0, 0.0, 0.0, 0.0);\n    vec4 specular_color = vec4(0.0, 0.0, 0.0, 0.0);\n    vec4 final_color;\n    \n    // todo: allow multiple light, define lights on viewvox or subscene\n    int nlights = 1; \n    for (int i=0; i<nlights; i++)\n    {{ \n        // Get light direction (make sure to prevent zero devision)\n        vec3 L = normalize(view_ray);  //lightDirs[i]; \n        float lightEnabled = float( length(L) > 0.0 );\n        L = normalize(L+(1.0-lightEnabled));\n        \n        // Calculate lighting properties\n        float lambertTerm = clamp( dot(N,L), 0.0, 1.0 );\n        vec3 H = normalize(L+V); // Halfway vector\n        float specularTerm = pow( max(dot(H,N),0.0), u_shininess);\n        \n        // Calculate mask\n        float mask1 = lightEnabled;\n        \n        // Calculate colors\n        ambient_color +=  mask1 * u_ambient;  // * gl_LightSource[i].ambient;\n        diffuse_color +=  mask1 * lambertTerm;\n        specular_color += mask1 * specularTerm * u_specular;\n    }}\n    \n    // Calculate final color by componing different components\n    final_color = color2 * ( ambient_color + diffuse_color) + specular_color;\n    final_color.a = color2.a;\n    \n    // Done\n    return final_color;\n}}\n\n// for some reason, this has to be the last function in order for the\n// filters to be inserted in the correct place...\n\nvoid main() {{\n    vec3 farpos = v_farpos.xyz / v_farpos.w;\n    vec3 nearpos = v_nearpos.xyz / v_nearpos.w;\n\n    // Calculate unit vector pointing in the view direction through this\n    // fragment.\n    view_ray = normalize(farpos.xyz - nearpos.xyz);\n\n    // Compute the distance to the front surface or near clipping plane\n    float distance = dot(nearpos-v_position, view_ray);\n    distance = max(distance, min((-0.5 - v_position.x) / view_ray.x,\n                            (u_shape.x - 0.5 - v_position.x) / view_ray.x));\n    distance = max(distance, min((-0.5 - v_position.y) / view_ray.y,\n                            (u_shape.y - 0.5 - v_position.y) / view_ray.y));\n    distance = max(distance, min((-0.5 - v_position.z) / view_ray.z,\n                            (u_shape.z - 0.5 - v_position.z) / view_ray.z));\n\n    // Now we have the starting position on the front surface\n    vec3 front = v_position + view_ray * distance;\n\n    // Decide how many steps to take\n    int nsteps = int(-distance / u_relative_step_size + 0.5);\n    if( nsteps < 1 )\n        discard;\n\n    // Get starting location and step vector in texture coordinates\n    vec3 step = ((v_position - front) / u_shape) / nsteps;\n    vec3 start_loc = front / u_shape;\n\n    // For testing: show the number of steps. This helps to establish\n    // whether the rays are correctly oriented\n    //gl_FragColor = vec4(0.0, nsteps / 3.0 / u_shape.x, 1.0, 1.0);\n    //return;\n\n    {before_loop}\n\n    // This outer loop seems necessary on some systems for large\n    // datasets. Ugly, but it works ...\n    vec3 loc = start_loc;\n    int iter = 0;\n    while (iter < nsteps) {{\n        for (iter=iter; iter<nsteps; iter++)\n        {{\n            // Get sample color\n            vec4 color = $sample(u_volumetex, loc);\n            float val = color.g;\n\n            {in_loop}\n\n            // Advance location deeper into the volume\n            loc += step;\n        }}\n    }}\n\n    {after_loop}\n\n    /* Set depth value - from visvis TODO\n    int iter_depth = int(maxi);\n    // Calculate end position in world coordinates\n    vec4 position2 = vertexPosition;\n    position2.xyz += ray*shape*float(iter_depth);\n    // Project to device coordinates and set fragment depth\n    vec4 iproj = gl_ModelViewProjectionMatrix * position2;\n    iproj.z /= iproj.w;\n    gl_FragDepth = (iproj.z+1.0)/2.0;\n    */\n}}\n\n\n'
MIP_SNIPPETS = dict(before_loop='\n        float maxval = -99999.0; // The maximum encountered value\n        int maxi = 0;  // Where the maximum value was encountered\n        ', in_loop='\n        if( val > maxval ) {\n            maxval = val;\n            maxi = iter;\n        }\n        ', after_loop='\n        // Refine search for max value\n        loc = start_loc + step * (float(maxi) - 0.5);\n        for (int i=0; i<10; i++) {\n            maxval = max(maxval, $sample(u_volumetex, loc).g);\n            loc += step * 0.1;\n        }\n        gl_FragColor = $cmap(maxval);\n        ')
MIP_FRAG_SHADER = FRAG_SHADER.format(**MIP_SNIPPETS)
TRANSLUCENT_SNIPPETS = dict(before_loop='\n        vec4 integrated_color = vec4(0., 0., 0., 0.);\n        ', in_loop="\n            color = $cmap(val);\n            float a1 = integrated_color.a;\n            float a2 = color.a * (1 - a1);\n            float alpha = max(a1 + a2, 0.001);\n            \n            // Doesn't work.. GLSL optimizer bug?\n            //integrated_color = (integrated_color * a1 / alpha) + \n            //                   (color * a2 / alpha); \n            // This should be identical but does work correctly:\n            integrated_color *= a1 / alpha;\n            integrated_color += color * a2 / alpha;\n            \n            integrated_color.a = alpha;\n            \n            if( alpha > 0.99 ){\n                // stop integrating if the fragment becomes opaque\n                iter = nsteps;\n            }\n        \n        ", after_loop='\n        gl_FragColor = integrated_color;\n        ')
TRANSLUCENT_FRAG_SHADER = FRAG_SHADER.format(**TRANSLUCENT_SNIPPETS)
ADDITIVE_SNIPPETS = dict(before_loop='\n        vec4 integrated_color = vec4(0., 0., 0., 0.);\n        ', in_loop='\n        color = $cmap(val);\n        \n        integrated_color = 1.0 - (1.0 - integrated_color) * (1.0 - color);\n        ', after_loop='\n        gl_FragColor = integrated_color;\n        ')
ADDITIVE_FRAG_SHADER = FRAG_SHADER.format(**ADDITIVE_SNIPPETS)
ISO_SNIPPETS = dict(before_loop='\n        vec4 color3 = vec4(0.0);  // final color\n        vec3 dstep = 1.5 / u_shape;  // step to sample derivative\n        gl_FragColor = vec4(0.0);\n    ', in_loop='\n        if (val > u_threshold-0.2) {\n            // Take the last interval in smaller steps\n            vec3 iloc = loc - step;\n            for (int i=0; i<10; i++) {\n                val = $sample(u_volumetex, iloc).g;\n                if (val > u_threshold) {\n                    color = $cmap(val);\n                    gl_FragColor = calculateColor(color, iloc, dstep);\n                    iter = nsteps;\n                    break;\n                }\n                iloc += step * 0.1;\n            }\n        }\n        ', after_loop='\n        ')
ISO_FRAG_SHADER = FRAG_SHADER.format(**ISO_SNIPPETS)
frag_dict = {'mip': MIP_FRAG_SHADER, 
   'iso': ISO_FRAG_SHADER, 
   'translucent': TRANSLUCENT_FRAG_SHADER, 
   'additive': ADDITIVE_FRAG_SHADER}

class VolumeVisual(Visual):
    """ Displays a 3D Volume
    
    Parameters
    ----------
    vol : ndarray
        The volume to display. Must be ndim==3.
    clim : tuple of two floats | None
        The contrast limits. The values in the volume are mapped to
        black and white corresponding to these values. Default maps
        between min and max.
    method : {'mip', 'translucent', 'additive', 'iso'}
        The render method to use. See corresponding docs for details.
        Default 'mip'.
    threshold : float
        The threshold to use for the isosurface render method. By default
        the mean of the given volume is used.
    relative_step_size : float
        The relative step size to step through the volume. Default 0.8.
        Increase to e.g. 1.5 to increase performance, at the cost of
        quality.
    cmap : str
        Colormap to use.
    emulate_texture : bool
        Use 2D textures to emulate a 3D texture. OpenGL ES 2.0 compatible,
        but has lower performance on desktop platforms.
    """

    def __init__(self, vol, clim=None, method='mip', threshold=None, relative_step_size=0.8, cmap='grays', emulate_texture=False):
        tex_cls = TextureEmulated3D if emulate_texture else Texture3D
        self._vol_shape = ()
        self._clim = None
        self._need_vertex_update = True
        self._cmap = get_colormap(cmap)
        self._vertices = VertexBuffer()
        self._texcoord = VertexBuffer(np.array([
         [
          0, 0, 0],
         [
          1, 0, 0],
         [
          0, 1, 0],
         [
          1, 1, 0],
         [
          0, 0, 1],
         [
          1, 0, 1],
         [
          0, 1, 1],
         [
          1, 1, 1]], dtype=np.float32))
        self._tex = tex_cls((10, 10, 10), interpolation='linear', wrapping='clamp_to_edge')
        Visual.__init__(self, vcode=VERT_SHADER, fcode='')
        self.shared_program['u_volumetex'] = self._tex
        self.shared_program['a_position'] = self._vertices
        self.shared_program['a_texcoord'] = self._texcoord
        self._draw_mode = 'triangle_strip'
        self._index_buffer = IndexBuffer()
        self.set_gl_state('translucent', cull_face=False)
        self.set_data(vol, clim)
        self.method = method
        self.relative_step_size = relative_step_size
        self.threshold = threshold if threshold is not None else vol.mean()
        self.freeze()
        return

    def set_data(self, vol, clim=None):
        """ Set the volume data. 

        Parameters
        ----------
        vol : ndarray
            The 3D volume.
        clim : tuple | None
            Colormap limits to use. None will use the min and max values.
        """
        if not isinstance(vol, np.ndarray):
            raise ValueError('Volume visual needs a numpy array.')
        if not (vol.ndim == 3 or vol.ndim == 4 and vol.shape[(-1)] <= 4):
            raise ValueError('Volume visual needs a 3D image.')
        if clim is not None:
            clim = np.array(clim, float)
            if not (clim.ndim == 1 and clim.size == 2):
                raise ValueError('clim must be a 2-element array-like')
            self._clim = tuple(clim)
        if self._clim is None:
            self._clim = (
             vol.min(), vol.max())
        vol = np.array(vol, dtype='float32', copy=False)
        if self._clim[1] == self._clim[0]:
            if self._clim[0] != 0.0:
                vol *= 1.0 / self._clim[0]
        else:
            vol -= self._clim[0]
            vol /= self._clim[1] - self._clim[0]
        self._tex.set_data(vol)
        self.shared_program['u_shape'] = (vol.shape[2], vol.shape[1],
         vol.shape[0])
        shape = vol.shape[:3]
        if self._vol_shape != shape:
            self._vol_shape = shape
            self._need_vertex_update = True
        self._vol_shape = shape
        self._kb_for_texture = np.prod(self._vol_shape) / 1024
        return

    @property
    def clim(self):
        """ The contrast limits that were applied to the volume data.
        Settable via set_data().
        """
        return self._clim

    @property
    def cmap(self):
        return self._cmap

    @cmap.setter
    def cmap(self, cmap):
        self._cmap = get_colormap(cmap)
        self.shared_program.frag['cmap'] = Function(self._cmap.glsl_map)
        self.update()

    @property
    def method(self):
        """The render method to use

        Current options are:
        
            * translucent: voxel colors are blended along the view ray until
              the result is opaque.
            * mip: maxiumum intensity projection. Cast a ray and display the
              maximum value that was encountered.
            * additive: voxel colors are added along the view ray until
              the result is saturated.
            * iso: isosurface. Cast a ray until a certain threshold is
              encountered. At that location, lighning calculations are
              performed to give the visual appearance of a surface.  
        """
        return self._method

    @method.setter
    def method(self, method):
        known_methods = list(frag_dict.keys())
        if method not in known_methods:
            raise ValueError('Volume render method should be in %r, not %r' % (
             known_methods, method))
        self._method = method
        if 'u_threshold' in self.shared_program:
            self.shared_program['u_threshold'] = None
        self.shared_program.frag = frag_dict[method]
        self.shared_program.frag['sampler_type'] = self._tex.glsl_sampler_type
        self.shared_program.frag['sample'] = self._tex.glsl_sample
        self.shared_program.frag['cmap'] = Function(self._cmap.glsl_map)
        self.update()
        return

    @property
    def threshold(self):
        """ The threshold value to apply for the isosurface render method.
        """
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = float(value)
        if 'u_threshold' in self.shared_program:
            self.shared_program['u_threshold'] = self._threshold
        self.update()

    @property
    def relative_step_size(self):
        """ The relative step size used during raycasting.
        
        Larger values yield higher performance at reduced quality. If
        set > 2.0 the ray skips entire voxels. Recommended values are
        between 0.5 and 1.5. The amount of quality degredation depends
        on the render method.
        """
        return self._relative_step_size

    @relative_step_size.setter
    def relative_step_size(self, value):
        value = float(value)
        if value < 0.1:
            raise ValueError('relative_step_size cannot be smaller than 0.1')
        self._relative_step_size = value
        self.shared_program['u_relative_step_size'] = value

    def _create_vertex_data(self):
        """ Create and set positions and texture coords from the given shape
        
        We have six faces with 1 quad (2 triangles) each, resulting in
        6*2*3 = 36 vertices in total.
        """
        shape = self._vol_shape
        x0, x1 = -0.5, shape[2] - 0.5
        y0, y1 = -0.5, shape[1] - 0.5
        z0, z1 = -0.5, shape[0] - 0.5
        pos = np.array([
         [
          x0, y0, z0],
         [
          x1, y0, z0],
         [
          x0, y1, z0],
         [
          x1, y1, z0],
         [
          x0, y0, z1],
         [
          x1, y0, z1],
         [
          x0, y1, z1],
         [
          x1, y1, z1]], dtype=np.float32)
        indices = np.array([2, 6, 0, 4, 5, 6, 7, 2, 3, 0, 1, 5, 3, 7], dtype=np.uint32)
        self._vertices.set_data(pos)
        self._index_buffer.set_data(indices)

    def _compute_bounds(self, axis, view):
        return (
         0, self._vol_shape[axis])

    def _prepare_transforms(self, view):
        trs = view.transforms
        view.view_program.vert['transform'] = trs.get_transform()
        view_tr_f = trs.get_transform('visual', 'document')
        view_tr_i = view_tr_f.inverse
        view.view_program.vert['viewtransformf'] = view_tr_f
        view.view_program.vert['viewtransformi'] = view_tr_i

    def _prepare_draw(self, view):
        if self._need_vertex_update:
            self._create_vertex_data()