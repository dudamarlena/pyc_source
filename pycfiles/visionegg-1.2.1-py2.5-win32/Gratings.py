# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\Gratings.py
# Compiled at: 2009-07-07 11:29:42
"""
Grating stimuli.

"""
import logging, VisionEgg, VisionEgg.Core, VisionEgg.Textures, VisionEgg.ParameterTypes as ve_types, numpy, math, types, string, VisionEgg.GL as gl, _vegl

def _get_type_info(bitdepth):
    """Private helper function to calculate type info based on bit depth"""
    if bitdepth == 8:
        gl_type = gl.GL_UNSIGNED_BYTE
        numpy_dtype = numpy.uint8
        max_int_val = float(255)
    elif bitdepth == 12:
        gl_type = gl.GL_SHORT
        numpy_dtype = numpy.int16
        max_int_val = float(32767)
    elif bitdepth == 16:
        gl_type = gl.GL_INT
        numpy_dtype = numpy.int32
        max_int_val = float(2147483647.0)
    else:
        raise ValueError('supported bitdepths are 8, 12, and 16.')
    return (
     gl_type, numpy_dtype, max_int_val)


class LuminanceGratingCommon(VisionEgg.Core.Stimulus):
    """Base class with common code to all ways of drawing luminance gratings.

    Parameters
    ==========
    bit_depth -- precision with which grating is calculated and sent to OpenGL (UnsignedInteger)
                 Default: 8
    """
    parameters_and_defaults = VisionEgg.ParameterDefinition({'bit_depth': (
                   8,
                   ve_types.UnsignedInteger,
                   'precision with which grating is calculated and sent to OpenGL')})
    __slots__ = ('gl_internal_format', 'format', 'gl_type', 'numpy_dtype', 'max_int_val',
                 'cached_bit_depth')

    def calculate_bit_depth_dependencies(self):
        """Calculate a number of parameters dependent on bit depth."""
        bit_depth_warning = False
        p = self.parameters
        red_bits = gl.glGetIntegerv(gl.GL_RED_BITS)
        green_bits = gl.glGetIntegerv(gl.GL_GREEN_BITS)
        blue_bits = gl.glGetIntegerv(gl.GL_BLUE_BITS)
        min_bits = min((red_bits, green_bits, blue_bits))
        if min_bits < p.bit_depth:
            logger = logging.getLogger('VisionEgg.Gratings')
            logger.warning('Requested bit depth of %d in LuminanceGratingCommon, which is greater than your current OpenGL context supports (%d).' % (
             p.bit_depth, min_bits))
        self.gl_internal_format = gl.GL_LUMINANCE
        self.format = gl.GL_LUMINANCE
        (self.gl_type, self.numpy_dtype, self.max_int_val) = _get_type_info(p.bit_depth)
        self.cached_bit_depth = p.bit_depth


class AlphaGratingCommon(VisionEgg.Core.Stimulus):
    """Base class with common code to all ways of drawing gratings in alpha.

    This class is currently not used by any other classes.

    Parameters
    ==========
    bit_depth -- precision with which grating is calculated and sent to OpenGL (UnsignedInteger)
                 Default: 8
    """
    parameters_and_defaults = VisionEgg.ParameterDefinition({'bit_depth': (
                   8,
                   ve_types.UnsignedInteger,
                   'precision with which grating is calculated and sent to OpenGL')})
    __slots__ = ('gl_internal_format', 'format', 'gl_type', 'numpy_dtype', 'max_int_val',
                 'cached_bit_depth')

    def calculate_bit_depth_dependencies(self):
        """Calculate a number of parameters dependent on bit depth."""
        p = self.parameters
        alpha_bit_depth = gl.glGetIntegerv(gl.GL_ALPHA_BITS)
        if alpha_bit_depth < p.bit_depth:
            logger = logging.getLogger('VisionEgg.Gratings')
            logger.warning('Requested bit depth of %d, which is greater than your current OpenGL context supports (%d).' % (
             p.bit_depth, min_bits))
        self.gl_internal_format = gl.GL_ALPHA
        self.format = gl.GL_ALPHA
        (self.gl_type, self.numpy_dtype, self.max_int_val) = _get_type_info(p.bit_depth)
        self.cached_bit_depth = p.bit_depth


class SinGrating2D(LuminanceGratingCommon):
    """Sine wave grating stimulus

    This is a general-purpose, realtime sine-wave luminace grating
    generator. To acheive an arbitrary orientation, this class rotates
    a textured quad.  To draw a grating with sides that always remain
    horizontal and vertical, draw a large grating in a small viewport.
    (The viewport will clip anything beyond its edges.)

    Parameters
    ==========
    anchor                      -- specifies how position parameter is interpreted (String)
                                   Default: center
    bit_depth                   -- precision with which grating is calculated and sent to OpenGL (UnsignedInteger)
                                   Inherited from LuminanceGratingCommon
                                   Default: 8
    color1                      -- (AnyOf(Sequence3 of Real or Sequence4 of Real))
                                   Default: (1.0, 1.0, 1.0)
    color2                      -- optional color with which to perform interpolation with color1 in RGB space (AnyOf(Sequence3 of Real or Sequence4 of Real))
                                   Default: (determined at runtime)
    contrast                    -- (Real)
                                   Default: 1.0
    depth                       -- (Real)
                                   Default: (determined at runtime)
    ignore_time                 -- (Boolean)
                                   Default: False
    mask                        -- optional masking function (Instance of <class 'VisionEgg.Textures.Mask2D'>)
                                   Default: (determined at runtime)
    max_alpha                   -- (Real)
                                   Default: 1.0
    num_samples                 -- (UnsignedInteger)
                                   Default: 512
    on                          -- draw stimulus? (Boolean)
                                   Default: True
    orientation                 -- (Real)
                                   Default: 0.0
    pedestal                    -- (Real)
                                   Default: 0.5
    phase_at_t0                 -- (Real)
                                   Default: 0.0
    position                    -- (units: eye coordinates) (Sequence2 of Real)
                                   Default: (320.0, 240.0)
    recalculate_phase_tolerance -- (Real)
                                   Default: (determined at runtime)
    size                        -- defines coordinate size of grating (in eye coordinates) (Sequence2 of Real)
                                   Default: (640.0, 480.0)
    spatial_freq                -- frequency defined relative to coordinates defined in size parameter (units: cycles/eye_coord_unit) (Real)
                                   Default: 0.0078125
    t0_time_sec_absolute        -- (Real)
                                   Default: (determined at runtime)
    temporal_freq_hz            -- (Real)
                                   Default: 5.0
    """
    parameters_and_defaults = VisionEgg.ParameterDefinition({'on': (
            True,
            ve_types.Boolean,
            'draw stimulus?'), 
       'mask': (
              None,
              ve_types.Instance(VisionEgg.Textures.Mask2D),
              'optional masking function'), 
       'contrast': (
                  1.0,
                  ve_types.Real), 
       'pedestal': (
                  0.5,
                  ve_types.Real), 
       'position': (
                  (320.0, 240.0),
                  ve_types.Sequence2(ve_types.Real),
                  '(units: eye coordinates)'), 
       'anchor': (
                'center',
                ve_types.String,
                'specifies how position parameter is interpreted'), 
       'depth': (
               None,
               ve_types.Real), 
       'size': (
              (640.0, 480.0),
              ve_types.Sequence2(ve_types.Real),
              'defines coordinate size of grating (in eye coordinates)'), 
       'spatial_freq': (
                      1.0 / 128.0,
                      ve_types.Real,
                      'frequency defined relative to coordinates defined in size parameter (units: cycles/eye_coord_unit)'), 
       'temporal_freq_hz': (
                          5.0,
                          ve_types.Real), 
       't0_time_sec_absolute': (
                              None,
                              ve_types.Real), 
       'ignore_time': (
                     False,
                     ve_types.Boolean), 
       'phase_at_t0': (
                     0.0,
                     ve_types.Real), 
       'orientation': (
                     0.0,
                     ve_types.Real), 
       'num_samples': (
                     512,
                     ve_types.UnsignedInteger), 
       'max_alpha': (
                   1.0,
                   ve_types.Real), 
       'color1': (
                (1.0, 1.0, 1.0),
                ve_types.AnyOf(ve_types.Sequence3(ve_types.Real), ve_types.Sequence4(ve_types.Real))), 
       'color2': (
                None,
                ve_types.AnyOf(ve_types.Sequence3(ve_types.Real), ve_types.Sequence4(ve_types.Real)),
                'optional color with which to perform interpolation with color1 in RGB space'), 
       'recalculate_phase_tolerance': (
                                     None,
                                     ve_types.Real)})
    __slots__ = ('_texture_object_id', '_last_phase')

    def __init__(self, **kw):
        LuminanceGratingCommon.__init__(self, **kw)
        p = self.parameters
        self._texture_object_id = gl.glGenTextures(1)
        if p.mask:
            gl.glActiveTextureARB(gl.GL_TEXTURE0_ARB)
        gl.glBindTexture(gl.GL_TEXTURE_1D, self._texture_object_id)
        max_dim = gl.glGetIntegerv(gl.GL_MAX_TEXTURE_SIZE)
        if p.num_samples > max_dim:
            raise NumSamplesTooLargeError('Grating num_samples too large for video system.\nOpenGL reports maximum size of %d' % (max_dim,))
        self.calculate_bit_depth_dependencies()
        w = p.size[0]
        inc = w / float(p.num_samples)
        phase = 0.0
        self._last_phase = phase
        floating_point_sin = numpy.sin(2.0 * math.pi * p.spatial_freq * numpy.arange(0.0, w, inc, dtype=numpy.float) + phase / 180.0 * math.pi) * 0.5 * p.contrast + p.pedestal
        floating_point_sin = numpy.clip(floating_point_sin, 0.0, 1.0)
        texel_data = (floating_point_sin * self.max_int_val).astype(self.numpy_dtype).tostring()
        gl.glTexImage1D(gl.GL_PROXY_TEXTURE_1D, 0, self.gl_internal_format, p.num_samples, 0, self.format, self.gl_type, texel_data)
        if gl.glGetTexLevelParameteriv(gl.GL_PROXY_TEXTURE_1D, 0, gl.GL_TEXTURE_WIDTH) == 0:
            raise NumSamplesTooLargeError('Grating num_samples is too wide for your video system!')
        gl.glTexImage1D(gl.GL_TEXTURE_1D, 0, self.gl_internal_format, p.num_samples, 0, self.format, self.gl_type, texel_data)
        gl.glTexParameteri(gl.GL_TEXTURE_1D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_1D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_1D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_1D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        if p.color2 is not None:
            if VisionEgg.Core.gl_renderer == 'ATi Rage 128 Pro OpenGL Engine' and VisionEgg.Core.gl_version == '1.1 ATI-1.2.22':
                logger = logging.getLogger('VisionEgg.Gratings')
                logger.warning('Your video card and driver have known bugs which prevent them from rendering color gratings properly.')
        return

    def __del__(self):
        gl.glDeleteTextures([self._texture_object_id])

    def draw(self):
        p = self.parameters
        if p.on:
            center = VisionEgg._get_center(p.position, p.anchor, p.size)
            if p.mask:
                gl.glActiveTextureARB(gl.GL_TEXTURE0_ARB)
            gl.glBindTexture(gl.GL_TEXTURE_1D, self._texture_object_id)
            gl.glEnable(gl.GL_TEXTURE_1D)
            gl.glDisable(gl.GL_TEXTURE_2D)
            if p.bit_depth != self.cached_bit_depth:
                self.calculate_bit_depth_dependencies()
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glPushMatrix()
            gl.glTranslate(center[0], center[1], 0)
            gl.glRotate(p.orientation, 0, 0, 1)
            if p.depth is None:
                gl.glDisable(gl.GL_DEPTH_TEST)
                depth = 0.0
            else:
                gl.glEnable(gl.GL_DEPTH_TEST)
                depth = p.depth
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            if p.color2:
                gl.glTexEnvi(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_BLEND)
                gl.glTexEnvfv(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_COLOR, p.color2)
            else:
                gl.glTexEnvi(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE)
            if p.t0_time_sec_absolute is None and not p.ignore_time:
                p.t0_time_sec_absolute = VisionEgg.time_func()
            w = p.size[0]
            inc = w / float(p.num_samples)
            if p.ignore_time:
                phase = p.phase_at_t0
            else:
                t_var = VisionEgg.time_func() - p.t0_time_sec_absolute
                phase = t_var * p.temporal_freq_hz * -360.0 + p.phase_at_t0
            if p.recalculate_phase_tolerance is None or abs(self._last_phase - phase) > p.recalculate_phase_tolerance:
                self._last_phase = phase
                floating_point_sin = numpy.sin(2.0 * math.pi * p.spatial_freq * numpy.arange(0.0, w, inc, dtype=numpy.float) + phase / 180.0 * math.pi) * 0.5 * p.contrast + p.pedestal
                floating_point_sin = numpy.clip(floating_point_sin, 0.0, 1.0)
                texel_data = (floating_point_sin * self.max_int_val).astype(self.numpy_dtype)
                _vegl.veglTexSubImage1D(gl.GL_TEXTURE_1D, 0, 0, p.num_samples, self.format, self.gl_type, texel_data)
            h_w = p.size[0] / 2.0
            h_h = p.size[1] / 2.0
            l = -h_w
            r = h_w
            b = -h_h
            t = h_h
            gl.glColor4f(p.color1[0], p.color1[1], p.color1[2], p.max_alpha)
            if p.mask:
                p.mask.draw_masked_quad(0.0, 1.0, 0.0, 1.0, l, r, b, t, depth)
            else:
                gl.glBegin(gl.GL_QUADS)
                gl.glTexCoord2f(0.0, 0.0)
                gl.glVertex3f(l, b, depth)
                gl.glTexCoord2f(1.0, 0.0)
                gl.glVertex3f(r, b, depth)
                gl.glTexCoord2f(1.0, 1.0)
                gl.glVertex3f(r, t, depth)
                gl.glTexCoord2f(0.0, 1.0)
                gl.glVertex3f(l, t, depth)
                gl.glEnd()
            gl.glDisable(gl.GL_TEXTURE_1D)
            gl.glPopMatrix()
        return


class SinGrating3D(LuminanceGratingCommon):
    """Sine wave grating stimulus texture mapped onto quad in 3D

    This is a general-purpose, realtime sine-wave luminace grating
    generator. This 3D version doesn't support an orientation
    parameter.  This could be implemented, but for now should be done
    by orienting the quad in 3D.

    Parameters
    ==========
    bit_depth                   -- precision with which grating is calculated and sent to OpenGL (UnsignedInteger)
                                   Inherited from LuminanceGratingCommon
                                   Default: 8
    color1                      -- (AnyOf(Sequence3 of Real or Sequence4 of Real))
                                   Default: (1.0, 1.0, 1.0)
    color2                      -- optional color with which to perform interpolation with color1 in RGB space (AnyOf(Sequence3 of Real or Sequence4 of Real))
                                   Default: (determined at runtime)
    contrast                    -- (Real)
                                   Default: 1.0
    depth                       -- (Real)
                                   Default: (determined at runtime)
    depth_test                  -- perform depth test? (Boolean)
                                   Default: True
    ignore_time                 -- (Boolean)
                                   Default: False
    lowerleft                   -- vertex position (units: eye coordinates) (AnyOf(Sequence3 of Real or Sequence4 of Real))
                                   Default: (0.0, 0.0, -1.0)
    lowerright                  -- vertex position (units: eye coordinates) (AnyOf(Sequence3 of Real or Sequence4 of Real))
                                   Default: (1.0, 0.0, -1.0)
    mask                        -- optional masking function (Instance of <class 'VisionEgg.Textures.Mask2D'>)
                                   Default: (determined at runtime)
    max_alpha                   -- (Real)
                                   Default: 1.0
    num_samples                 -- (UnsignedInteger)
                                   Default: 512
    on                          -- draw stimulus? (Boolean)
                                   Default: True
    pedestal                    -- (Real)
                                   Default: 0.5
    phase_at_t0                 -- (Real)
                                   Default: 0.0
    recalculate_phase_tolerance -- (Real)
                                   Default: (determined at runtime)
    size                        -- defines coordinate size of grating (in eye coordinates) (Sequence2 of Real)
                                   Default: (1.0, 1.0)
    spatial_freq                -- frequency defined relative to coordinates defined in size parameter (units; cycles/eye_coord_unit) (Real)
                                   Default: 4.0
    t0_time_sec_absolute        -- (Real)
                                   Default: (determined at runtime)
    temporal_freq_hz            -- (Real)
                                   Default: 5.0
    upperleft                   -- vertex position (units: eye coordinates) (AnyOf(Sequence3 of Real or Sequence4 of Real))
                                   Default: (0.0, 1.0, -1.0)
    upperright                  -- vertex position (units: eye coordinates) (AnyOf(Sequence3 of Real or Sequence4 of Real))
                                   Default: (1.0, 1.0, -1.0)
    """
    parameters_and_defaults = VisionEgg.ParameterDefinition({'on': (
            True,
            ve_types.Boolean,
            'draw stimulus?'), 
       'mask': (
              None,
              ve_types.Instance(VisionEgg.Textures.Mask2D),
              'optional masking function'), 
       'contrast': (
                  1.0,
                  ve_types.Real), 
       'pedestal': (
                  0.5,
                  ve_types.Real), 
       'depth': (
               None,
               ve_types.Real), 
       'size': (
              (1.0, 1.0),
              ve_types.Sequence2(ve_types.Real),
              'defines coordinate size of grating (in eye coordinates)'), 
       'spatial_freq': (
                      4.0,
                      ve_types.Real,
                      'frequency defined relative to coordinates defined in size parameter (units; cycles/eye_coord_unit)'), 
       'temporal_freq_hz': (
                          5.0,
                          ve_types.Real), 
       't0_time_sec_absolute': (
                              None,
                              ve_types.Real), 
       'ignore_time': (
                     False,
                     ve_types.Boolean), 
       'phase_at_t0': (
                     0.0,
                     ve_types.Real), 
       'num_samples': (
                     512,
                     ve_types.UnsignedInteger), 
       'max_alpha': (
                   1.0,
                   ve_types.Real), 
       'color1': (
                (1.0, 1.0, 1.0),
                ve_types.AnyOf(ve_types.Sequence3(ve_types.Real), ve_types.Sequence4(ve_types.Real))), 
       'color2': (
                None,
                ve_types.AnyOf(ve_types.Sequence3(ve_types.Real), ve_types.Sequence4(ve_types.Real)),
                'optional color with which to perform interpolation with color1 in RGB space'), 
       'recalculate_phase_tolerance': (
                                     None,
                                     ve_types.Real), 
       'depth_test': (
                    True,
                    ve_types.Boolean,
                    'perform depth test?'), 
       'lowerleft': (
                   (0.0, 0.0, -1.0),
                   ve_types.AnyOf(ve_types.Sequence3(ve_types.Real), ve_types.Sequence4(ve_types.Real)),
                   'vertex position (units: eye coordinates)'), 
       'lowerright': (
                    (1.0, 0.0, -1.0),
                    ve_types.AnyOf(ve_types.Sequence3(ve_types.Real), ve_types.Sequence4(ve_types.Real)),
                    'vertex position (units: eye coordinates)'), 
       'upperleft': (
                   (0.0, 1.0, -1.0),
                   ve_types.AnyOf(ve_types.Sequence3(ve_types.Real), ve_types.Sequence4(ve_types.Real)),
                   'vertex position (units: eye coordinates)'), 
       'upperright': (
                    (1.0, 1.0, -1.0),
                    ve_types.AnyOf(ve_types.Sequence3(ve_types.Real), ve_types.Sequence4(ve_types.Real)),
                    'vertex position (units: eye coordinates)'), 
       'polygon_offset_enabled': (
                                False,
                                ve_types.Boolean,
                                'perform polygon offset?'), 
       'polygon_offset_factor': (
                               1.0,
                               ve_types.Real,
                               'polygon factor'), 
       'polygon_offset_units': (
                              1.0,
                              ve_types.Real,
                              'polygon units')})
    __slots__ = ('_texture_object_id', '_last_phase')

    def __init__(self, **kw):
        LuminanceGratingCommon.__init__(self, **kw)
        p = self.parameters
        self._texture_object_id = gl.glGenTextures(1)
        if p.mask:
            gl.glActiveTextureARB(gl.GL_TEXTURE0_ARB)
        gl.glBindTexture(gl.GL_TEXTURE_1D, self._texture_object_id)
        max_dim = gl.glGetIntegerv(gl.GL_MAX_TEXTURE_SIZE)
        if p.num_samples > max_dim:
            raise NumSamplesTooLargeError('Grating num_samples too large for video system.\nOpenGL reports maximum size of %d' % (max_dim,))
        self.calculate_bit_depth_dependencies()
        w = p.size[0]
        inc = w / float(p.num_samples)
        phase = 0.0
        self._last_phase = phase
        floating_point_sin = numpy.sin(2.0 * math.pi * p.spatial_freq * numpy.arange(0.0, w, inc, dtype=numpy.float) + phase / 180.0 * math.pi) * 0.5 * p.contrast + p.pedestal
        floating_point_sin = numpy.clip(floating_point_sin, 0.0, 1.0)
        texel_data = (floating_point_sin * self.max_int_val).astype(self.numpy_dtype).tostring()
        gl.glTexImage1D(gl.GL_PROXY_TEXTURE_1D, 0, self.gl_internal_format, p.num_samples, 0, self.format, self.gl_type, texel_data)
        if gl.glGetTexLevelParameteriv(gl.GL_PROXY_TEXTURE_1D, 0, gl.GL_TEXTURE_WIDTH) == 0:
            raise NumSamplesTooLargeError('Grating num_samples is too wide for your video system!')
        gl.glTexImage1D(gl.GL_TEXTURE_1D, 0, self.gl_internal_format, p.num_samples, 0, self.format, self.gl_type, texel_data)
        gl.glTexParameteri(gl.GL_TEXTURE_1D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_1D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameteri(gl.GL_TEXTURE_1D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_1D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        if p.color2 is not None:
            if VisionEgg.Core.gl_renderer == 'ATi Rage 128 Pro OpenGL Engine' and VisionEgg.Core.gl_version == '1.1 ATI-1.2.22':
                logger = logging.getLogger('VisionEgg.Gratings')
                logger.warning('Your video card and driver have known bugs which prevent them from rendering color gratings properly.')
        return

    def __del__(self):
        gl.glDeleteTextures([self._texture_object_id])

    def draw(self):
        p = self.parameters
        if p.on:
            if p.mask:
                gl.glActiveTextureARB(gl.GL_TEXTURE0_ARB)
            if p.depth_test:
                gl.glEnable(gl.GL_DEPTH_TEST)
            else:
                gl.glDisable(gl.GL_DEPTH_TEST)
            if p.polygon_offset_enabled:
                gl.glEnable(gl.GL_POLYGON_OFFSET_EXT)
                gl.glPolygonOffset(p.polygon_offset_factor, p.polygon_offset_units)
            gl.glBindTexture(gl.GL_TEXTURE_1D, self._texture_object_id)
            gl.glEnable(gl.GL_TEXTURE_1D)
            gl.glDisable(gl.GL_TEXTURE_2D)
            if p.bit_depth != self.cached_bit_depth:
                self.calculate_bit_depth_dependencies()
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            if p.color2:
                gl.glTexEnvi(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_BLEND)
                gl.glTexEnvfv(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_COLOR, p.color2)
            else:
                gl.glTexEnvi(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE)
            if p.t0_time_sec_absolute is None and not p.ignore_time:
                p.t0_time_sec_absolute = VisionEgg.time_func()
            w = p.size[0]
            inc = w / float(p.num_samples)
            if p.ignore_time:
                phase = p.phase_at_t0
            else:
                t_var = VisionEgg.time_func() - p.t0_time_sec_absolute
                phase = t_var * p.temporal_freq_hz * -360.0 + p.phase_at_t0
            if p.recalculate_phase_tolerance is None or abs(self._last_phase - phase) > p.recalculate_phase_tolerance:
                self._last_phase = phase
                floating_point_sin = numpy.sin(2.0 * math.pi * p.spatial_freq * numpy.arange(0.0, w, inc, dtype=numpy.float) + phase / 180.0 * math.pi) * 0.5 * p.contrast + p.pedestal
                floating_point_sin = numpy.clip(floating_point_sin, 0.0, 1.0)
                texel_data = (floating_point_sin * self.max_int_val).astype(self.numpy_dtype).tostring()
                gl.glTexSubImage1D(gl.GL_TEXTURE_1D, 0, 0, p.num_samples, self.format, self.gl_type, texel_data)
            gl.glColor4f(p.color1[0], p.color1[1], p.color1[2], p.max_alpha)
            if p.mask:
                p.mask.draw_masked_quad_3d(0.0, 1.0, 0.0, 1.0, p.lowerleft, p.lowerright, p.upperright, p.upperleft)
            else:
                gl.glBegin(gl.GL_QUADS)
                gl.glTexCoord2f(0.0, 0.0)
                gl.glVertex(*p.lowerleft)
                gl.glTexCoord2f(1.0, 0.0)
                gl.glVertex(*p.lowerright)
                gl.glTexCoord2f(1.0, 1.0)
                gl.glVertex(*p.upperright)
                gl.glTexCoord2f(0.0, 1.0)
                gl.glVertex(*p.upperleft)
                gl.glEnd()
            gl.glDisable(gl.GL_TEXTURE_1D)
            if p.polygon_offset_enabled:
                gl.glDisable(gl.GL_POLYGON_OFFSET_EXT)
        return


class NumSamplesTooLargeError(RuntimeError):
    pass