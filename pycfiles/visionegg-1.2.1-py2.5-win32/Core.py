# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\Core.py
# Compiled at: 2009-07-07 11:29:42
"""
Core Vision Egg functionality.

This module contains the architectural foundations of the Vision Egg.

"""
import sys, types, math, time, os, StringIO, logging, VisionEgg, VisionEgg.PlatformDependent, VisionEgg.ParameterTypes as ve_types, VisionEgg.GLTrace, VisionEgg.ThreeDeeMath, pygame, pygame.locals, pygame.display, VisionEgg.GL as gl, numpy, numpy as np
try:
    sum
except NameError:
    import operator

    def sum(values):
        return reduce(operator.add, values)


def swap_buffers():
    global VisionEgg
    VisionEgg.config._FRAMECOUNT_ABSOLUTE += 1
    return pygame.display.flip()


class PygameKeeper(object):
    """global object that calls any cleanup functions when quitting pygame"""

    def __init__(self):
        self.to_call_on_quit = []

    def register_func_to_call_on_quit(self, func):
        if func not in self.to_call_on_quit:
            self.to_call_on_quit.append(func)

    def unregister_func_to_call_on_quit(self, func):
        idx = self.to_call_on_quit.index(func)
        del self.to_call_on_quit[idx]

    def quit(self):
        for func in self.to_call_on_quit:
            func()

        pygame.quit()


pygame_keeper = PygameKeeper()

class Screen(VisionEgg.ClassWithParameters):
    """An OpenGL window, possibly displayed across multiple displays.

    A Screen instance is an OpenGL window for the Vision Egg to draw
    in.  For an instance of Screen to do anything useful, it must
    contain one or more instances of the Viewport class and one or
    more instances of the Stimulus class.

    Currently, only one OpenGL window is supported by the library with
    which the Vision Egg initializes graphics (pygame/SDL).  However,
    this need not limit display to a single physical display device.
    Many video drivers, for example, allow applications to treat two
    separate monitors as one large array of contiguous pixels.  By
    sizing a window such that it occupies both monitors and creating
    separate viewports for the portion of the window on each monitor,
    a multiple screen effect can be created.

    Public read-only variables
    ==========================
    size -- Tuple of 2 integers specifying width and height

    Parameters
    ==========
    bgcolor -- background color (AnyOf(Sequence3 of Real or Sequence4 of Real))
               Default: (0.5, 0.5, 0.5, 0.0)

    Constant Parameters
    ===================
    alpha_bits          -- number of bits per pixel for alpha channel. Can be set with VISIONEGG_REQUEST_ALPHA_BITS (UnsignedInteger)
                           Default: (determined at runtime)
    blue_bits           -- number of bits per pixel for blue channel. Can be set with VISIONEGG_REQUEST_BLUE_BITS (UnsignedInteger)
                           Default: (determined at runtime)
    double_buffer       -- use double buffering? Can be set with VISIONEGG_DOUBLE_BUFFER (Boolean)
                           Default: (determined at runtime)
    frameless           -- remove standard window frame? Can be set with VISIONEGG_FRAMELESS_WINDOW (Boolean)
                           Default: (determined at runtime)
    fullscreen          -- use full screen? Can be set with VISIONEGG_FULLSCREEN (Boolean)
                           Default: (determined at runtime)
    green_bits          -- number of bits per pixel for green channel. Can be set with VISIONEGG_REQUEST_GREEN_BITS (UnsignedInteger)
                           Default: (determined at runtime)
    hide_mouse          -- hide the mouse cursor? Can be set with VISIONEGG_HIDE_MOUSE (Boolean)
                           Default: (determined at runtime)
    is_stereo           -- allocate stereo framebuffers? Can be set with VISIONEGG_REQUEST_STEREO (Boolean)
                           Default: (determined at runtime)
    maxpriority         -- raise priority? (platform dependent) Can be set with VISIONEGG_MAXPRIORITY (Boolean)
                           Default: (determined at runtime)
    multisample_samples -- preferred number of multisamples for FSAA (UnsignedInteger)
                           Default: (determined at runtime)
    preferred_bpp       -- preferred bits per pixel (bit depth) Can be set with VISIONEGG_PREFERRED_BPP (UnsignedInteger)
                           Default: (determined at runtime)
    red_bits            -- number of bits per pixel for red channel. Can be set with VISIONEGG_REQUEST_RED_BITS (UnsignedInteger)
                           Default: (determined at runtime)
    size                -- size (units: pixels) Can be set with VISIONEGG_SCREEN_W and VISIONEGG_SCREEN_H (Sequence2 of Real)
                           Default: (determined at runtime)
    sync_swap           -- synchronize buffer swaps to vertical sync? Can be set with VISIONEGG_SYNC_SWAP (Boolean)
                           Default: (determined at runtime)
    """
    parameters_and_defaults = VisionEgg.ParameterDefinition({'bgcolor': (
                 (0.5, 0.5, 0.5, 0.0),
                 ve_types.AnyOf(ve_types.Sequence3(ve_types.Real), ve_types.Sequence4(ve_types.Real)),
                 'background color')})
    constant_parameters_and_defaults = VisionEgg.ParameterDefinition({'size': (
              None,
              ve_types.Sequence2(ve_types.Real),
              'size (units: pixels) Can be set with VISIONEGG_SCREEN_W and VISIONEGG_SCREEN_H'), 
       'fullscreen': (
                    None,
                    ve_types.Boolean,
                    'use full screen? Can be set with VISIONEGG_FULLSCREEN'), 
       'double_buffer': (
                       None,
                       ve_types.Boolean,
                       'use double buffering? Can be set with VISIONEGG_DOUBLE_BUFFER'), 
       'preferred_bpp': (
                       None,
                       ve_types.UnsignedInteger,
                       'preferred bits per pixel (bit depth) Can be set with VISIONEGG_PREFERRED_BPP'), 
       'maxpriority': (
                     None,
                     ve_types.Boolean,
                     'raise priority? (platform dependent) Can be set with VISIONEGG_MAXPRIORITY'), 
       'hide_mouse': (
                    None,
                    ve_types.Boolean,
                    'hide the mouse cursor? Can be set with VISIONEGG_HIDE_MOUSE'), 
       'frameless': (
                   None,
                   ve_types.Boolean,
                   'remove standard window frame? Can be set with VISIONEGG_FRAMELESS_WINDOW'), 
       'sync_swap': (
                   None,
                   ve_types.Boolean,
                   'synchronize buffer swaps to vertical sync? Can be set with VISIONEGG_SYNC_SWAP'), 
       'red_bits': (
                  None,
                  ve_types.UnsignedInteger,
                  'number of bits per pixel for red channel. Can be set with VISIONEGG_REQUEST_RED_BITS'), 
       'green_bits': (
                    None,
                    ve_types.UnsignedInteger,
                    'number of bits per pixel for green channel. Can be set with VISIONEGG_REQUEST_GREEN_BITS'), 
       'blue_bits': (
                   None,
                   ve_types.UnsignedInteger,
                   'number of bits per pixel for blue channel. Can be set with VISIONEGG_REQUEST_BLUE_BITS'), 
       'alpha_bits': (
                    None,
                    ve_types.UnsignedInteger,
                    'number of bits per pixel for alpha channel. Can be set with VISIONEGG_REQUEST_ALPHA_BITS'), 
       'is_stereo': (
                   None,
                   ve_types.Boolean,
                   'allocate stereo framebuffers? Can be set with VISIONEGG_REQUEST_STEREO'), 
       'multisample_samples': (
                             None,
                             ve_types.UnsignedInteger,
                             'preferred number of multisamples for FSAA')})
    __slots__ = ('__cursor_visible_func__', '__pygame_quit__', '_put_pixels_texture_stimulus',
                 '_pixel_coord_projection')

    def __init__(self, **kw):
        global gl
        global gl_renderer
        global gl_vendor
        global gl_version
        global synclync
        logger = logging.getLogger('VisionEgg.Core')
        VisionEgg.ClassWithParameters.__init__(self, **kw)
        cp = self.constant_parameters
        if cp.size is None:
            cp.size = (
             VisionEgg.config.VISIONEGG_SCREEN_W,
             VisionEgg.config.VISIONEGG_SCREEN_H)
        if cp.double_buffer is None:
            cp.double_buffer = VisionEgg.config.VISIONEGG_DOUBLE_BUFFER
        if cp.fullscreen is None:
            cp.fullscreen = VisionEgg.config.VISIONEGG_FULLSCREEN
        if cp.preferred_bpp is None:
            cp.preferred_bpp = VisionEgg.config.VISIONEGG_PREFERRED_BPP
        if cp.maxpriority is None:
            cp.maxpriority = VisionEgg.config.VISIONEGG_MAXPRIORITY
        if cp.hide_mouse is None:
            cp.hide_mouse = VisionEgg.config.VISIONEGG_HIDE_MOUSE
        if cp.frameless is None:
            cp.frameless = VisionEgg.config.VISIONEGG_FRAMELESS_WINDOW
        if cp.sync_swap is None:
            cp.sync_swap = VisionEgg.config.VISIONEGG_SYNC_SWAP
        if cp.red_bits is None:
            cp.red_bits = VisionEgg.config.VISIONEGG_REQUEST_RED_BITS
        if cp.green_bits is None:
            cp.green_bits = VisionEgg.config.VISIONEGG_REQUEST_GREEN_BITS
        if cp.blue_bits is None:
            cp.blue_bits = VisionEgg.config.VISIONEGG_REQUEST_BLUE_BITS
        if cp.alpha_bits is None:
            cp.alpha_bits = VisionEgg.config.VISIONEGG_REQUEST_ALPHA_BITS
        if cp.is_stereo is None:
            cp.is_stereo = VisionEgg.config.VISIONEGG_REQUEST_STEREO
        if cp.multisample_samples is None:
            cp.multisample_samples = VisionEgg.config.VISIONEGG_MULTISAMPLE_SAMPLES
        if VisionEgg.config.SYNCLYNC_PRESENT:
            import synclync
            try:
                VisionEgg.config._SYNCLYNC_CONNECTION = synclync.SyncLyncConnection()
            except synclync.SyncLyncError, x:
                logger.warning('Could not connect to SyncLync device (SyncLyncError: %s).' % str(x))
                VisionEgg.config._SYNCLYNC_CONNECTION = None
            else:
                logger.info('Connected to SyncLync device')
        else:
            VisionEgg.config._SYNCLYNC_CONNECTION = None
        if cp.sync_swap:
            sync_success = VisionEgg.PlatformDependent.sync_swap_with_vbl_pre_gl_init()
        pygame.display.init()
        if hasattr(pygame.display, 'gl_set_attribute'):
            pygame.display.gl_set_attribute(pygame.locals.GL_RED_SIZE, cp.red_bits)
            pygame.display.gl_set_attribute(pygame.locals.GL_GREEN_SIZE, cp.green_bits)
            pygame.display.gl_set_attribute(pygame.locals.GL_BLUE_SIZE, cp.blue_bits)
            pygame.display.gl_set_attribute(pygame.locals.GL_ALPHA_SIZE, cp.alpha_bits)
            pygame.display.gl_set_attribute(pygame.locals.GL_STEREO, cp.is_stereo)
            if cp.multisample_samples > 0:
                pygame.display.gl_set_attribute(pygame.locals.GL_MULTISAMPLEBUFFERS, 1)
                pygame.display.gl_set_attribute(pygame.locals.GL_MULTISAMPLESAMPLES, cp.multisample_samples)
        else:
            logger.debug('Could not request or query exact bit depths, alpha or stereo because you need pygame release 1.4.9 or greater. This is only of concern if you use a stimulus that needs this. In that case, the stimulus should check for the desired feature(s).')
        if not hasattr(pygame.display, 'set_gamma_ramp'):
            logger.debug('set_gamma_ramp function not available because you need pygame release 1.5 or greater. This is only of concern if you need this feature.')
        pygame.display.set_caption('Vision Egg')
        flags = pygame.locals.OPENGL
        if cp.double_buffer:
            flags = flags | pygame.locals.DOUBLEBUF
        if cp.fullscreen:
            flags = flags | pygame.locals.FULLSCREEN
        if cp.frameless:
            flags = flags | pygame.locals.NOFRAME
        try_bpp = cp.preferred_bpp
        append_str = ''
        if cp.fullscreen:
            screen_mode = 'fullscreen'
        else:
            screen_mode = 'window'
        if hasattr(pygame.display, 'gl_set_attribute'):
            append_str = ' (%d %d %d %d RGBA).' % (cp.red_bits,
             cp.green_bits,
             cp.blue_bits,
             cp.alpha_bits)
        logger.info('Requesting %s %d x %d %d bpp%s' % (
         screen_mode, self.size[0], self.size[1],
         try_bpp, append_str))
        pygame.display.set_mode(self.size, flags, try_bpp)
        VisionEgg.config._pygame_started = 1
        try:
            if sys.platform != 'darwin':
                pygame.display.set_icon(pygame.transform.scale(pygame.image.load(os.path.join(VisionEgg.config.VISIONEGG_SYSTEM_DIR, 'data', 'visionegg.bmp')).convert(), (32,
                                                                                                                                                                           32)))
            else:
                import AppKit
                im = AppKit.NSImage.alloc()
                im.initWithContentsOfFile_(os.path.join(VisionEgg.config.VISIONEGG_SYSTEM_DIR, 'data', 'visionegg.tif'))
                AppKit.NSApplication.setApplicationIconImage_(AppKit.NSApp(), im)
        except Exception, x:
            logger.info('Error while trying to set_icon: %s: %s' % (
             str(x.__class__), str(x)))

        gl_vendor = gl.glGetString(gl.GL_VENDOR)
        gl_renderer = gl.glGetString(gl.GL_RENDERER)
        gl_version = gl.glGetString(gl.GL_VERSION)
        logger.info('OpenGL %s, %s, %s (PyOpenGL %s)' % (
         gl_version, gl_renderer, gl_vendor, gl.__version__))
        if gl_renderer == 'GDI Generic':
            if gl_vendor == 'Microsoft Corporation':
                logger.warning('Using default Microsoft Windows OpenGL drivers.  Please (re-)install the latest video drivers from your video card manufacturer to get hardware accelerated performance.')
            if gl_renderer == 'Mesa GLX Indirect' and gl_vendor == 'VA Linux Systems, Inc.':
                logger.warning('Using default Mesa GLX drivers. Please (re-)install the latest video drivers from your video card manufacturer or DRI project to get hardware accelarated performance.')
            cp.red_bits = None
            cp.green_bits = None
            cp.blue_bits = None
            cp.alpha_bits = None
            cp.is_stereo = None
            got_bpp = pygame.display.Info().bitsize
            append_str = ''
            if hasattr(pygame.display, 'gl_get_attribute'):
                cp.red_bits = pygame.display.gl_get_attribute(pygame.locals.GL_RED_SIZE)
                cp.green_bits = pygame.display.gl_get_attribute(pygame.locals.GL_GREEN_SIZE)
                cp.blue_bits = pygame.display.gl_get_attribute(pygame.locals.GL_BLUE_SIZE)
                cp.alpha_bits = pygame.display.gl_get_attribute(pygame.locals.GL_ALPHA_SIZE)
                cp.is_stereo = pygame.display.gl_get_attribute(pygame.locals.GL_STEREO)
                if cp.is_stereo:
                    stereo_string = ' stereo'
                else:
                    stereo_string = ''
                append_str = ' (%d %d %d %d RGBA%s)' % (
                 cp.red_bits, cp.green_bits, cp.blue_bits, cp.alpha_bits,
                 stereo_string)
            logger.info('Video system reports %d bpp%s.' % (got_bpp, append_str))
            if got_bpp < try_bpp:
                logger.warning('Video system reports %d bits per pixel, while your program requested %d. Can you adjust your video drivers?' % (
                 got_bpp,
                 try_bpp))
            self.__cursor_visible_func__ = pygame.mouse.set_visible
            self.__pygame_quit__ = pygame_keeper.quit
            if cp.multisample_samples > 0:
                if hasattr(pygame.display, 'gl_set_attribute'):
                    got_ms_buf = pygame.display.gl_get_attribute(pygame.locals.GL_MULTISAMPLEBUFFERS)
                    got_ms_samp = pygame.display.gl_get_attribute(pygame.locals.GL_MULTISAMPLESAMPLES)
                    if got_ms_samp < cp.multisample_samples:
                        logger.warning('Video system reports %d multisample samples, while you requested %d.  FSAA requires SDL > 1.2.6, check that it is installed.' % (
                         got_ms_samp, cp.multisample_samples))
            if cp.sync_swap:
                if not sync_success:
                    cp.sync_swap = VisionEgg.PlatformDependent.sync_swap_with_vbl_post_gl_init() or False
                    logger.warning("Unable to detect or automatically synchronize buffer swapping with vertical retrace. May be possible by manually adjusting video drivers. (Look for 'Enable Vertical Sync' or similar.) If buffer swapping is not synchronized, frame by frame control will not be possible. Because of this, you will probably get a warning about calculated frames per second different than specified.")
        post_gl_init()
        if cp.hide_mouse:
            self.__cursor_visible_func__(0)
        if cp.maxpriority:
            VisionEgg.PlatformDependent.set_priority()
        if hasattr(VisionEgg.config, '_open_screens'):
            VisionEgg.config._open_screens.append(self)
        else:
            VisionEgg.config._open_screens = [
             self]
        return

    def get_size(self):
        return self.constant_parameters.size

    def set_size(self, value):
        raise RuntimeError('Attempting to set read-only value')

    size = property(get_size, set_size)

    def get_framebuffer_as_image(self, buffer='back', format=gl.GL_RGB, position=(0, 0), anchor='lowerleft', size=None):
        """get pixel values from framebuffer to PIL image"""
        import Image
        fb_array = self.get_framebuffer_as_array(buffer=buffer, format=format, position=position, anchor=anchor, size=size)
        size = (
         fb_array.shape[1], fb_array.shape[0])
        if format == gl.GL_RGB:
            pil_mode = 'RGB'
        elif format == gl.GL_RGBA:
            pil_mode = 'RGBA'
        fb_image = Image.fromstring(pil_mode, size, fb_array.tostring())
        fb_image = fb_image.transpose(Image.FLIP_TOP_BOTTOM)
        return fb_image

    def get_framebuffer_as_array(self, buffer='back', format=gl.GL_RGB, position=(0, 0), anchor='lowerleft', size=None):
        """get pixel values from framebuffer to numpy array"""
        if size is None:
            size = self.size
        lowerleft = VisionEgg._get_lowerleft(position, anchor, size)
        if buffer == 'front':
            gl.glReadBuffer(gl.GL_FRONT)
        elif buffer == 'back':
            gl.glReadBuffer(gl.GL_BACK)
        else:
            raise ValueError('No support for "%s" framebuffer' % buffer)
        framebuffer_pixels = gl.glReadPixels(lowerleft[0], lowerleft[1], size[0], size[1], gl.GL_RGBA, gl.GL_UNSIGNED_BYTE)
        raw_format = 'RGBA'
        fb_array = np.fromstring(framebuffer_pixels, np.uint8)
        fb_array = np.reshape(fb_array, (size[1], size[0], 4))
        if format == gl.GL_RGB:
            if raw_format == 'BGRA':
                fb_array = fb_array[:, :, 1:]
            elif raw_format == 'RGBA':
                fb_array = fb_array[:, :, :3]
        elif format == gl.GL_RGBA:
            if raw_format == 'BGRA':
                B = fb_array[:, :, 0, np.newaxis]
                G = fb_array[:, :, 1, np.newaxis]
                R = fb_array[:, :, 2, np.newaxis]
                A = fb_array[:, :, 3, np.newaxis]
                fb_array = np.concatenate((R, G, B, A), axis=2)
            elif raw_format == 'RGBA':
                pass
        else:
            raise NotImplementedError('Only RGB and RGBA formats currently supported')
        return fb_array

    def put_pixels(self, pixels=None, position=(0, 0), anchor='lowerleft', scale_x=1.0, scale_y=1.0, texture_min_filter=gl.GL_NEAREST, texture_mag_filter=gl.GL_NEAREST, internal_format=gl.GL_RGB):
        """Put pixel values to screen.

        Pixel values become texture data using the VisionEgg.Textures
        module.  Any source of texture data accepted by that module is
        accepted here.

        This function could be sped up by allocating a fixed OpenGL texture object.

        """
        import VisionEgg.Textures
        make_new_texture_object = 0
        if not hasattr(self, '_put_pixels_texture_stimulus'):
            make_new_texture_object = 1
        elif internal_format != self._put_pixels_texture_stimulus.constant_parameters.internal_format:
            make_new_texture_object = 1
        if make_new_texture_object:
            texture = VisionEgg.Textures.Texture(pixels)
            on_screen_size = (texture.size[0] * scale_x, texture.size[1] * scale_y)
            t = VisionEgg.Textures.TextureStimulus(texture=texture, position=position, anchor=anchor, size=on_screen_size, mipmaps_enabled=0, texture_min_filter=texture_min_filter, texture_mag_filter=texture_mag_filter, internal_format=internal_format)
            self._put_pixels_texture_stimulus = t
            self._pixel_coord_projection = OrthographicProjection(left=0, right=self.size[0], bottom=0, top=self.size[1], z_clip_near=0.0, z_clip_far=1.0)
        else:
            self._put_pixels_texture_stimulus.parameters.texture = VisionEgg.Textures.Texture(pixels)
        self._pixel_coord_projection.push_and_set_gl_projection()
        self._put_pixels_texture_stimulus.draw()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()

    def query_refresh_rate(self):
        return VisionEgg.PlatformDependent.query_refresh_rate(self)

    def measure_refresh_rate(self, average_over_seconds=0.1):
        """Measure the refresh rate. Assumes swap buffers synced."""
        start_time = VisionEgg.time_func()
        duration_sec = 0.0
        num_frames = 0
        while duration_sec < average_over_seconds:
            swap_buffers()
            now = VisionEgg.time_func()
            num_frames += 1
            duration_sec = now - start_time

        if duration_sec > 0.0:
            fps = num_frames / duration_sec
        else:
            fps = 0.0
        return fps

    def clear(self):
        """Called by Presentation instance. Clear the screen."""
        c = self.parameters.bgcolor
        if len(c) == 4:
            gl.glClearColor(*c)
        else:
            gl.glClearColor(c[0], c[1], c[2], 0.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def make_current(self):
        """Called by Viewport instance. Makes screen active for drawing.

        Can not be implemented until multiple screens are possible."""
        pass

    def set_gamma_ramp(self, *args, **kw):
        """Set the gamma_ramp, if supported.

        Call pygame.display.set_gamma_ramp, if available.

        Returns True on success, False otherwise."""
        if not hasattr(pygame.display, 'set_gamma_ramp'):
            logger = logging.getLogger('VisionEgg.Core')
            logger.error('Need pygame 1.5 or greater for set_gamma_ramp function')
            return False
        if pygame.display.set_gamma_ramp(*args, **kw):
            return True
        else:
            return False

    def close(self):
        """Close the screen.

        You can call this to close the screen.  Not necessary during
        normal operation because it gets automatically deleted."""
        if hasattr(VisionEgg.config, '_open_screens'):
            if self in VisionEgg.config._open_screens:
                VisionEgg.config._open_screens.remove(self)
            if len(VisionEgg.config._open_screens) == 0:
                if hasattr(self, '__cursor_visible_func__'):
                    self.__cursor_visible_func__(1)
                pygame_keeper.quit()
        if hasattr(self, '__cursor_visible_func__'):
            del self.__cursor_visible_func__

    def __del__(self):
        if hasattr(self, '__cursor_visible_func__'):
            try:
                self.__cursor_visible_func__(1)
                self.__pygame_quit__()
            except pygame.error, x:
                if str(x) != 'video system not initialized':
                    raise

    def create_default():
        """Alternative constructor using configuration variables.

        Most of the time you can create and instance of Screen using
        this method.  If your script needs explicit control of the
        Screen parameters, initialize with the normal constructor.

        Uses VisionEgg.config.VISIONEGG_GUI_INIT to determine how the
        default screen parameters should are determined.  If this
        value is 0, the values from VisionEgg.cfg are used.  If this
        value is 1, a GUI panel is opened and allows manual settings
        of the screen parameters.  """
        global VisionEgg
        if VisionEgg.config.VISIONEGG_GUI_INIT:
            import VisionEgg.GUI
            window = VisionEgg.GUI.GraphicsConfigurationWindow()
            window.mainloop()
            if not window.clicked_ok:
                sys.exit()
        screen = None
        try:
            screen = Screen(size=(VisionEgg.config.VISIONEGG_SCREEN_W,
             VisionEgg.config.VISIONEGG_SCREEN_H), fullscreen=VisionEgg.config.VISIONEGG_FULLSCREEN, preferred_bpp=VisionEgg.config.VISIONEGG_PREFERRED_BPP, bgcolor=(0.5,
                                                                                                                                                                      0.5,
                                                                                                                                                                      0.5,
                                                                                                                                                                      0.0), maxpriority=VisionEgg.config.VISIONEGG_MAXPRIORITY, frameless=VisionEgg.config.VISIONEGG_FRAMELESS_WINDOW, hide_mouse=VisionEgg.config.VISIONEGG_HIDE_MOUSE)
        finally:
            if screen is None:
                try:
                    pygame.mouse.set_visible(1)
                    pygame_keeper.quit()
                except pygame.error, x:
                    if str(x) != 'video system not initialized':
                        raise

        if screen is None:
            raise RuntimeError('Screen open failed. Check your error log for a traceback.')
        gamma_source = VisionEgg.config.VISIONEGG_GAMMA_SOURCE.lower()
        if gamma_source != 'none':
            if gamma_source == 'invert':
                native_red = VisionEgg.config.VISIONEGG_GAMMA_INVERT_RED
                native_green = VisionEgg.config.VISIONEGG_GAMMA_INVERT_GREEN
                native_blue = VisionEgg.config.VISIONEGG_GAMMA_INVERT_BLUE
                red = screen._create_inverted_gamma_ramp(native_red)
                green = screen._create_inverted_gamma_ramp(native_green)
                blue = screen._create_inverted_gamma_ramp(native_blue)
                gamma_set_string = 'linearized gamma lookup tables to correct ' + 'monitor with native gammas (%f, %f, %f) RGB' % (
                 native_red,
                 native_green,
                 native_blue)
            elif gamma_source == 'file':
                filename = VisionEgg.config.VISIONEGG_GAMMA_FILE
                (red, green, blue) = screen._open_gamma_file(filename)
                gamma_set_string = 'set gamma lookup tables from data in file %s' % os.path.abspath(filename)
            else:
                raise ValueError("Unknown gamma source: '%s'" % gamma_source)
            logger = logging.getLogger('VisionEgg.Core')
            if not screen.set_gamma_ramp(red, green, blue):
                logger.warning('Setting gamma ramps failed.')
            else:
                logger.info('Gamma set sucessfully: %s' % gamma_set_string)
        return screen

    create_default = staticmethod(create_default)

    def _create_inverted_gamma_ramp(self, gamma):
        c = 1.0
        inc = 1.0 / 255
        target_luminances = np.arange(0.0, 1.0 + inc, inc)
        output_ramp = np.zeros(target_luminances.shape, dtype=np.int)
        for i in range(len(target_luminances)):
            L = target_luminances[i]
            if L == 0.0:
                v_88fp = 0
            else:
                v = math.exp((math.log(L) - math.log(c)) / gamma)
                v_88fp = int(round(v * 255 * 256))
            output_ramp[i] = v_88fp

        return list(output_ramp)

    def _open_gamma_file(self, filename):
        fd = open(filename, 'r')
        gamma_values = []
        for line in fd.readlines():
            line = line.strip()
            if line.startswith('#'):
                continue
            gamma_values.append(map(int, line.split()))
            if len(gamma_values[(-1)]) != 3:
                raise ValueError('expected 3 values per gamma entry')

        if len(gamma_values) != 256:
            raise ValueError('expected 256 gamma entries')
        (red, green, blue) = zip(*gamma_values)
        return (red, green, blue)


def get_default_screen():
    """Make an instance of Screen using a GUI window or from config file."""
    return Screen.create_default()


class ProjectionBaseClass(VisionEgg.ClassWithParameters):
    """Base class for 4x4 linear matrix transformation

    This is an abstract base class which should be subclassed for
    actual use.

    Parameters
    ==========
    matrix -- matrix specifying projection (Sequence4x4 of Real)
              Default: [[1 0 0 0]
                        [0 1 0 0]
                        [0 0 1 0]
                        [0 0 0 1]]
    """
    parameters_and_defaults = VisionEgg.ParameterDefinition({'matrix': (
                numpy.eye(4),
                ve_types.Sequence4x4(ve_types.Real),
                'matrix specifying projection')})
    __slots__ = ('projection_type', )

    def __init__(self, **kw):
        VisionEgg.ClassWithParameters.__init__(self, **kw)
        self.projection_type = None
        return

    def _get_matrix_type(self):
        if self.projection_type == gl.GL_PROJECTION:
            return gl.GL_PROJECTION_MATRIX
        elif self.projection_type == gl.GL_MODELVIEW:
            return gl.GL_MODELVIEW_MATRIX

    def apply_to_gl(self):
        """Set the OpenGL projection matrix."""
        gl.glMatrixMode(self.projection_type)
        gl.glLoadMatrixf(self.parameters.matrix)

    def set_gl_modelview(self):
        """Set the OpenGL modelview matrix."""
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadMatrixf(self.parameters.matrix)

    def set_gl_projection(self):
        """Set the OpenGL projection matrix."""
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadMatrixf(self.parameters.matrix)

    def push_and_set_gl_projection(self):
        """Set the OpenGL projection matrix, pushing current projection matrix to stack."""
        gl.glMatrixMode(self.projection_type)
        gl.glPushMatrix()
        gl.glLoadMatrixf(self.parameters.matrix)

    def translate(self, x, y, z):
        """Compose a translation and set the OpenGL projection matrix."""
        gl.glMatrixMode(self.projection_type)
        gl.glLoadMatrixf(self.parameters.matrix)
        gl.glTranslatef(x, y, z)
        self.parameters.matrix = gl.glGetFloatv(self._get_matrix_type())

    def stateless_translate(self, x, y, z):
        """Compose a translation without changing OpenGL state."""
        M = VisionEgg.ThreeDeeMath.TransformMatrix(self.parameters.matrix)
        M.translate(x, y, z)
        self.parameters.matrix = M.get_matrix()

    def rotate(self, angle_degrees, x, y, z):
        """Compose a rotation and set the OpenGL projection matrix."""
        gl.glMatrixMode(self.projection_type)
        gl.glLoadMatrixf(self.parameters.matrix)
        gl.glRotatef(angle_degrees, x, y, z)
        self.parameters.matrix = gl.glGetFloatv(self._get_matrix_type())

    def stateless_rotate(self, angle_degrees, x, y, z):
        """Compose a rotation without changing OpenGL state."""
        M = VisionEgg.ThreeDeeMath.TransformMatrix(self.parameters.matrix)
        M.rotate(angle_degrees, x, y, z)
        self.parameters.matrix = M.get_matrix()

    def scale(self, x, y, z):
        """Compose a rotation and set the OpenGL projection matrix."""
        gl.glMatrixMode(self.projection_type)
        gl.glLoadMatrixf(self.parameters.matrix)
        gl.glScalef(x, y, z)
        self.parameters.matrix = gl.glGetFloatv(self._get_matrix_type())

    def stateless_scale(self, x, y, z):
        """Compose a rotation without changing OpenGL state."""
        M = VisionEgg.ThreeDeeMath.TransformMatrix(self.parameters.matrix)
        M.scale(x, y, z)
        self.parameters.matrix = M.get_matrix()

    def get_matrix(self):
        return self.parameters.matrix

    def look_at(self, eye, center, up):

        def normalize(vec):
            numpy_vec = numpy.asarray(vec)
            mag = math.sqrt(numpy.sum(numpy_vec ** 2))
            return numpy_vec / mag

        def cross(vec1, vec2):
            return (vec1[1] * vec2[2] - vec1[2] * vec2[1],
             vec1[2] * vec2[0] - vec1[0] * vec2[2],
             vec1[0] * vec2[1] - vec1[1] * vec2[0])

        forward = numpy.array((center[0] - eye[0],
         center[1] - eye[1],
         center[2] - eye[2]), 'f')
        forward = normalize(forward)
        side = cross(forward, up)
        side = normalize(side)
        new_up = cross(side, forward)
        m = np.array([[side[0], new_up[0], -forward[0], 0.0],
         [
          side[1], new_up[1], -forward[1], 0.0],
         [
          side[2], new_up[2], -forward[2], 0.0],
         [
          0.0, 0.0, 0.0, 1.0]])
        gl.glMatrixMode(self.projection_type)
        gl.glPushMatrix()
        try:
            gl.glLoadMatrixf(self.parameters.matrix)
            gl.glMultMatrixf(m)
            gl.glTranslatef(-eye[0], -eye[1], -eye[2])
            self.parameters.matrix = gl.glGetFloatv(self._get_matrix_type())
        finally:
            gl.glPopMatrix()

    def eye_2_clip(self, eye_coords_vertex):
        """Transform eye coordinates to clip coordinates"""
        m = np.array(self.parameters.matrix)
        v = np.array(eye_coords_vertex)
        homog = VisionEgg.ThreeDeeMath.make_homogeneous_coord_rows(v)
        r = numpy.dot(homog, m)
        if len(homog.shape) > len(v.shape):
            r = np.reshape(r, (4, ))
        return r

    def clip_2_norm_device(self, clip_coords_vertex):
        """Transform clip coordinates to normalized device coordinates"""
        v = numpy.array(clip_coords_vertex)
        homog = VisionEgg.ThreeDeeMath.make_homogeneous_coord_rows(v)
        err = numpy.seterr(all='ignore')
        r = (homog / homog[:, 3, numpy.newaxis])[:, :3]
        numpy.seterr(**err)
        if len(homog.shape) > len(v.shape):
            r = np.reshape(r, (3, ))
        return r

    def eye_2_norm_device(self, eye_coords_vertex):
        """Transform eye coordinates to normalized device coordinates"""
        return self.clip_2_norm_device(self.eye_2_clip(eye_coords_vertex))

    def apply_to_vertex(self, vertex):
        """Perform multiplication on vertex to get transformed result"""
        M = VisionEgg.ThreeDeeMath.TransformMatrix(matrix=self.parameters.matrix)
        r = M.transform_vertices([vertex])
        return r[0]

    def apply_to_vertices(self, vertices):
        """Perform multiplication on vertex to get transformed result"""
        M = VisionEgg.ThreeDeeMath.TransformMatrix(matrix=self.parameters.matrix)
        r = M.transform_vertices(vertices)
        return r


class Projection(ProjectionBaseClass):
    """for use of OpenGL PROJECTION_MATRIX

    Converts eye coordinates to clip coordinates.

    Parameters
    ==========
    matrix -- matrix specifying projection (Sequence4x4 of Real)
              Default: [[1 0 0 0]
                        [0 1 0 0]
                        [0 0 1 0]
                        [0 0 0 1]]
    """

    def __init__(self, *args, **kw):
        ProjectionBaseClass.__init__(self, *args, **kw)
        self.projection_type = gl.GL_PROJECTION


class ModelView(ProjectionBaseClass):
    """for use of OpenGL MODELVIEW_MATRIX

    Converts object coordinates to eye coordinates.

    Parameters
    ==========
    matrix -- matrix specifying projection (Sequence4x4 of Real)
              Default: [[1 0 0 0]
                        [0 1 0 0]
                        [0 0 1 0]
                        [0 0 0 1]]
    """

    def __init__(self, *args, **kw):
        ProjectionBaseClass.__init__(self, *args, **kw)
        self.projection_type = gl.GL_MODELVIEW


class OrthographicProjection(Projection):
    """An orthographic projection.

    Parameters
    ==========
    matrix -- matrix specifying projection (Sequence4x4 of Real)
              Default: [[1 0 0 0]
                        [0 1 0 0]
                        [0 0 1 0]
                        [0 0 0 1]]
    """

    def __init__(self, left=0.0, right=640.0, bottom=0.0, top=480.0, z_clip_near=0.0, z_clip_far=1.0):
        """Create an orthographic projection.

        Defaults to map x eye coordinates in the range [0,640], y eye
        coordinates [0,480] and clip coordinates [0,1] to [0,1].
        Therefore, if the viewport is 640 x 480, eye coordinates
        correspond 1:1 with window (pixel) coordinates.  Only points
        between these clipping planes will be displayed.
        """
        matrix = np.array([[2.0 / (right - left), 0.0, 0.0, -(right + left) / (right - left)],
         [
          0.0, 2.0 / (top - bottom), 0.0, -(top + bottom) / (top - bottom)],
         [
          0.0, 0.0, -2.0 / (z_clip_far - z_clip_near), -(z_clip_far + z_clip_near) / (z_clip_far - z_clip_near)],
         [
          0.0, 0.0, 0.0, 1.0]])
        matrix = np.transpose(matrix)
        Projection.__init__(self, **{'matrix': matrix})


class OrthographicProjectionNoZClip(Projection):
    """An orthographic projection without Z clipping.

    Parameters
    ==========
    matrix -- matrix specifying projection (Sequence4x4 of Real)
              Default: [[1 0 0 0]
                        [0 1 0 0]
                        [0 0 1 0]
                        [0 0 0 1]]
    """

    def __init__(self, left=0.0, right=640.0, bottom=0.0, top=480.0):
        """Create an orthographic projection without Z clipping.

        Defaults to map x eye coordinates in the range [0,640] and y
        eye coordinates [0,480] -> [0,1].  Therefore, if the viewport
        is 640 x 480, eye coordinates correspond 1:1 with window
        (pixel) coordinates.
        """
        matrix = np.array([[2.0 / (right - left), 0, 0, -(right + left) / (right - left)],
         [
          0, 2.0 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
         [
          0, 0, -1, -1.0],
         [
          0, 0, 0, 1]])
        matrix = np.transpose(matrix)
        Projection.__init__(self, **{'matrix': matrix})


class SimplePerspectiveProjection(Projection):
    """A simplified perspective projection.

    Parameters
    ==========
    matrix -- matrix specifying projection (Sequence4x4 of Real)
              Default: [[1 0 0 0]
                        [0 1 0 0]
                        [0 0 1 0]
                        [0 0 0 1]]
    """

    def __init__(self, fov_x=45.0, z_clip_near=0.1, z_clip_far=10000.0, aspect_ratio=4.0 / 3.0):
        matrix = self._compute_matrix(fov_x, z_clip_near, z_clip_far, aspect_ratio)
        Projection.__init__(self, **{'matrix': matrix})

    def _compute_matrix(self, fov_x=45.0, z_clip_near=0.1, z_clip_far=10000.0, aspect_ratio=4.0 / 3.0):
        """Compute a 4x4 projection matrix that performs a perspective distortion."""
        fov_y = fov_x / aspect_ratio
        radians = fov_y / 2.0 * math.pi / 180.0
        delta_z = z_clip_far - z_clip_near
        sine = math.sin(radians)
        if delta_z == 0.0 or sine == 0.0 or aspect_ratio == 0.0:
            raise ValueError('Invalid parameters passed to SimpleProjection.__init__()')
        cotangent = math.cos(radians) / sine
        matrix = np.zeros((4, 4))
        matrix[0][0] = cotangent / aspect_ratio
        matrix[1][1] = cotangent
        matrix[2][2] = -(z_clip_far + z_clip_near) / delta_z
        matrix[2][3] = -1.0
        matrix[3][2] = -2.0 * z_clip_near * z_clip_far / delta_z
        matrix[3][3] = 0.0
        return matrix


class PerspectiveProjection(Projection):
    """A perspective projection.

    Parameters
    ==========
    matrix -- matrix specifying projection (Sequence4x4 of Real)
              Default: [[1 0 0 0]
                        [0 1 0 0]
                        [0 0 1 0]
                        [0 0 0 1]]
    """

    def __init__(self, left, right, bottom, top, near, far):
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glFrustum(left, right, bottom, top, near, far)
        matrix = gl.glGetFloatv(gl.GL_PROJECTION_MATRIX)
        gl.glPopMatrix()
        if matrix is None:
            raise RuntimeError('OpenGL matrix operations can only take place once OpenGL context started.')
        matrix = np.asarray(matrix)
        Projection.__init__(self, **{'matrix': matrix})
        return


class Stimulus(VisionEgg.ClassWithParameters):
    """Base class for a stimulus.

    Any stimulus element should be a subclass of this Stimulus class.
    The draw() method contains the code executed before every buffer
    swap in order to render the stimulus to the frame buffer.  It
    should execute as quickly as possible.  The init_gl() method must
    be called before the first call to draw() so that any internal
    data, OpenGL display lists, and OpenGL:texture objects can be
    established.

    To illustrate the concept of the Stimulus class, here is a
    description of several methods of drawing two spots.  If your
    experiment displays two spots simultaneously, you could create two
    instances of (a single subclass of) Stimulus, varying parameters
    so each draws at a different location.  Another possibility is to
    create one instance of a subclass that draws two spots.  Another,
    somewhat obscure, possibility is to create a single instance and
    add it to two different viewports.  (Something that will not work
    would be adding the same instance two times to the same viewport.
    It would also get drawn twice, although at exactly the same
    location.)

    OpenGL is a 'state machine', meaning that it has internal
    parameters whose values vary and affect how it operates.  Because
    of this inherent uncertainty, there are only limited assumptions
    about the state of OpenGL that an instance of Stimulus should
    expect when its draw() method is called.  Because the Vision Egg
    loops through stimuli this also imposes some important behaviors:

    First, the framebuffer will contain the results of any drawing
    operations performed since the last buffer swap by other instances
    of (subclasses of) Stimulus. Therefore, the order in which stimuli
    are present in the stimuli list of an instance of Viewport may be
    important.  Additionally, if there are overlapping viewports, the
    order in which viewports are added to an instance of Screen is
    important.

    Second, previously established OpenGL display lists and OpenGL
    texture objects will be available.  The __init__() method should
    establish these things.

    Third, there are several OpenGL state variables which are
    commonly set by subclasses of Stimulus, and which cannot be
    assumed to have any particular value at the time draw() is called.
    These state variables are: blending mode and function, texture
    state and environment, the matrix mode (modelview or projection),
    the modelview matrix, depth mode and settings. Therefore, if the
    draw() method depends on specific values for any of these states,
    it must specify its own values to OpenGL.

    Finally, a well-behaved Stimulus subclass resets any OpenGL state
    values other than those listed above to their initial state before
    draw() and init_gl() were called.  In other words, before your
    stimulus changes the state of an OpenGL variable, use
    glGetBoolean, glGetInteger, glGetFloat, or a similar function to
    query its value and restore it later.  For example, upon calling
    the draw() method, the projection matrix will be that which was
    set by the viewport. If the draw() method alters the projection
    matrix, it must be restored. The glPushMatrix() and glPopMatrix()
    commands provide an easy way to do this.

    The default projection of Viewport maps eye coordinates in a 1:1
    fashion to window coordinates (in other words, it sets eye
    coordinates to use pixel units from the lower left corner of the
    viewport). Therefore the default parameters for a stimulus should
    specify pixel coordinates if possible (such as for a 2D
    stimulus). Assuming a window size of 640 by 480 for the default
    parameters is a pretty safe way to do things.

    Also, be sure to check for any assumptions made about the system
    in the __init__ method.  For example, if your stimulus needs alpha
    in the framebuffer, check the value of
    glGetIntegerv(GL_ALPHA_BITS) and raise an exception if it is not
    available.
    """

    def __init__(self, **kw):
        """Instantiate and get ready to draw.

        Set parameter values and create anything needed to draw the
        stimulus including OpenGL state variables such display lists
        and texture objects.

        """
        VisionEgg.ClassWithParameters.__init__(self, **kw)

    def draw(self):
        """Draw the stimulus. (Called by Viewport instance.)

        This method is called every frame.  This method actually
        performs the OpenGL calls to draw the stimulus.

        """
        pass


class Viewport(VisionEgg.ClassWithParameters):
    """Connects stimuli to a screen.

    A viewport defines a (possibly clipped region) of the screen on
    which stimuli are drawn.

    A screen may have multiple viewports.  The viewports may be
    overlapping.

    A viewport may have multiple stimuli.

    A single stimulus may be drawn simultaneously by several
    viewports, although this is typically useful only for 3D stimuli
    to represent different views of the same object.

    The coordinates of the stimulus are converted to screen
    coordinates via several steps, the most important of which is the
    projection, which is defined by an instance of the Projection
    class.

    By default, a viewport has a projection and viewport
    transformation which maps eye coordinates to window coordinates in
    1:1 manner.  In other words, eye coordinates specify pixel
    location in the viewport window. For example, if the viewport was
    640 pixels wide and 480 pixels high, the default projection would
    take eye coordinate (320,240,0,1) and map it to normalized device
    coordinates of (0.5,0.5,0.0). The default viewport transformation
    would transform this to window coordinates of (320,240,0.5).

    For cases where pixel units are not natural to describe
    coordinates of a stimulus, the application should specify the a
    projection other than the default.  This is usually the case for
    3D stimuli.

    For details of the projection and clipping process, see the
    section 'Coordinate Transformations' in the book/online document
    'The OpenGL Graphics System: A Specification'

    Parameters
    ==========
    anchor        -- How position parameter is interpreted (String)
                     Default: lowerleft
    camera_matrix -- extrinsic camera parameter matrix (position and orientation) (Instance of <class 'VisionEgg.Core.ModelView'>)
                     Default: (determined at runtime)
    depth_range   -- depth range (in object units) for rendering (Sequence2 of Real)
                     Default: (0, 1)
    position      -- Position (in pixel units) within the screen (Sequence2 of Real)
                     Default: (0, 0)
    projection    -- intrinsic camera parameter matrix (field of view, focal length, aspect ratio) (Instance of <class 'VisionEgg.Core.Projection'>)
                     Default: (determined at runtime)
    screen        -- The screen in which this viewport is drawn (Instance of <class 'VisionEgg.Core.Screen'>)
                     Default: (determined at runtime)
    size          -- Size (in pixel units) (Sequence2 of Real)
                     Default: (determined at runtime)
    stimuli       -- sequence of stimuli to draw in screen (Sequence of Instance of <class 'VisionEgg.Core.Stimulus'>)
                     Default: (determined at runtime)
    """
    parameters_and_defaults = VisionEgg.ParameterDefinition({'screen': (
                None,
                ve_types.Instance(Screen),
                'The screen in which this viewport is drawn'), 
       'position': (
                  (0, 0),
                  ve_types.Sequence2(ve_types.Real),
                  'Position (in pixel units) within the screen'), 
       'anchor': (
                'lowerleft',
                ve_types.String,
                'How position parameter is interpreted'), 
       'depth_range': (
                     (0, 1),
                     ve_types.Sequence2(ve_types.Real),
                     'depth range (in object units) for rendering'), 
       'size': (
              None,
              ve_types.Sequence2(ve_types.Real),
              'Size (in pixel units)'), 
       'projection': (
                    None,
                    ve_types.Instance(Projection),
                    'intrinsic camera parameter matrix (field of view, focal length, aspect ratio)'), 
       'auto_pixel_projection': (
                               None,
                               ve_types.Boolean,
                               'reset the projection when the size changes to maintain pixel coordinates'), 
       'camera_matrix': (
                       None,
                       ve_types.Instance(ModelView),
                       'extrinsic camera parameter matrix (position and orientation)'), 
       'stimuli': (
                 None,
                 ve_types.Sequence(ve_types.Instance(Stimulus)),
                 'sequence of stimuli to draw in screen'), 
       'lowerleft': (
                   None,
                   ve_types.Sequence2(ve_types.Real),
                   'position (in pixel units) of lower-left viewport corner',
                   VisionEgg.ParameterDefinition.DEPRECATED)})
    __slots__ = ('_is_drawing', '_cached_size')

    def __init__(self, **kw):
        """Create a new instance.

        Required arguments:

        screen

        Optional arguments (specify parameter value other than default):

        position -- defaults to (0,0), position relative to screen by anchor (see below)
        anchor -- defaults to 'lowerleft'
        size -- defaults to screen.size
        projection -- defaults to self.make_new_pixel_coord_projection()
        stimuli -- defaults to empty list

        """
        VisionEgg.ClassWithParameters.__init__(self, **kw)
        if self.parameters.screen is None:
            raise ValueError('Must specify screen when creating an instance of Viewport.')
        p = self.parameters
        if p.size is None:
            p.size = p.screen.constant_parameters.size
        self._cached_size = None
        if p.projection is None:
            p.projection = self.make_new_pixel_coord_projection()
            if p.auto_pixel_projection is None:
                p.auto_pixel_projection = True
                self._cached_size = p.size
        elif p.auto_pixel_projection is None:
            p.auto_pixel_projection = False
        if p.camera_matrix is None:
            p.camera_matrix = ModelView()
        if p.stimuli is None:
            p.stimuli = []
        self._is_drawing = False
        return

    def make_new_pixel_coord_projection(self):
        """Create instance of Projection mapping eye coordinates 1:1 with pixel coordinates."""
        return OrthographicProjectionNoZClip(left=0, right=self.parameters.size[0], bottom=0, top=self.parameters.size[1])

    def make_current(self):
        p = self.parameters
        p.screen.make_current()
        if p.auto_pixel_projection and self._cached_size != p.size:
            p.projection = self.make_new_pixel_coord_projection()
            self._cached_size = p.size
        if p.lowerleft != None:
            if not hasattr(Viewport, '_gave_lowerleft_warning'):
                logger = logging.getLogger('VisionEgg.Core')
                logger.warning("lowerleft parameter of Viewport class will stop being supported. Use 'position' instead with anchor set to 'lowerleft'.")
                Viewport._gave_lowerleft_warning = True
            p.anchor = 'lowerleft'
            p.position = (p.lowerleft[0], p.lowerleft[1])
        lowerleft = VisionEgg._get_lowerleft(p.position, p.anchor, p.size)
        gl.glViewport(int(lowerleft[0]), int(lowerleft[1]), int(p.size[0]), int(p.size[1]))
        gl.glDepthRange(p.depth_range[0], p.depth_range[1])
        p.projection.apply_to_gl()
        p.camera_matrix.apply_to_gl()
        return

    def draw(self):
        """Set the viewport and draw stimuli."""
        self.make_current()
        self._is_drawing = True
        for stimulus in self.parameters.stimuli:
            stimulus.draw()

        self._is_drawing = False

    def norm_device_2_window(self, norm_device_vertex):
        """Transform normalized device coordinates to window coordinates"""
        v = np.asarray(norm_device_vertex)
        homog = VisionEgg.ThreeDeeMath.make_homogeneous_coord_rows(v)
        xd = homog[:, 0, np.newaxis]
        yd = homog[:, 1, np.newaxis]
        zd = homog[:, 2, np.newaxis]
        p = self.parameters
        lowerleft = VisionEgg._get_lowerleft(p.position, p.anchor, p.size)
        (x, y) = lowerleft
        (w, h) = p.size
        (n, f) = p.depth_range
        n = min(1.0, max(0.0, n))
        f = min(1.0, max(0.0, f))
        ox = x + w / 2.0
        oy = y + h / 2.0
        px = w
        py = h
        xw = px / 2.0 * xd + ox
        yw = py / 2.0 * yd + oy
        zw = (f - n) / 2.0 * zd + (n + f) / 2.0
        r = np.concatenate((xw, yw, zw), axis=1)
        if len(homog.shape) > len(v.shape):
            r = np.reshape(r, (3, ))
        return r

    def clip_2_window(self, eye_coords_vertex):
        """Transform clip coordinates to window coordinates"""
        my_proj = self.parameters.projection
        return self.norm_device_2_window(my_proj.clip_2_norm_device(eye_coords_vertex))

    def eye_2_window(self, eye_coords_vertex):
        """Transform eye coordinates to window coordinates"""
        my_proj = self.parameters.projection
        return self.norm_device_2_window(my_proj.eye_2_norm_device(eye_coords_vertex))


class FixationSpot(Stimulus):
    """A rectangle stimulus, typically used as a fixation spot.

    Parameters
    ==========
    anchor   -- how position parameter is used (String)
                Default: center
    color    -- color (AnyOf(Sequence3 of Real or Sequence4 of Real))
                Default: (1.0, 1.0, 1.0)
    on       -- draw? (Boolean)
                Default: True
    position -- position in eye coordinates (AnyOf(Sequence2 of Real or Sequence3 of Real or Sequence4 of Real))
                Default: (320.0, 240.0)
    size     -- size in eye coordinates (Sequence2 of Real)
                Default: (4.0, 4.0)
    """
    parameters_and_defaults = VisionEgg.ParameterDefinition({'on': (
            True,
            ve_types.Boolean,
            'draw?'), 
       'color': (
               (1.0, 1.0, 1.0),
               ve_types.AnyOf(ve_types.Sequence3(ve_types.Real), ve_types.Sequence4(ve_types.Real)),
               'color'), 
       'position': (
                  (320.0, 240.0),
                  ve_types.AnyOf(ve_types.Sequence2(ve_types.Real), ve_types.Sequence3(ve_types.Real), ve_types.Sequence4(ve_types.Real)),
                  'position in eye coordinates'), 
       'anchor': (
                'center',
                ve_types.String,
                'how position parameter is used'), 
       'size': (
              (4.0, 4.0),
              ve_types.Sequence2(ve_types.Real),
              'size in eye coordinates'), 
       'center': (
                None,
                ve_types.Sequence2(ve_types.Real),
                'position in eye coordinates',
                VisionEgg.ParameterDefinition.DEPRECATED)})

    def __init__(self, **kw):
        Stimulus.__init__(self, **kw)

    def draw(self):
        p = self.parameters
        if p.center is not None:
            if not hasattr(VisionEgg.config, '_GAVE_CENTER_DEPRECATION'):
                logger = logging.getLogger('VisionEgg.Core')
                logger.warning("Specifying FixationSpot by deprecated 'center' parameter deprecated.  Use 'position' parameter instead.  (Allows use of 'anchor' parameter to set to other values.)")
                VisionEgg.config._GAVE_CENTER_DEPRECATION = 1
            p.anchor = 'center'
            p.position = (p.center[0], p.center[1])
        if p.on:
            center = VisionEgg._get_center(p.position, p.anchor, p.size)
            gl.glDisable(gl.GL_DEPTH_TEST)
            gl.glDisable(gl.GL_TEXTURE_2D)
            gl.glDisable(gl.GL_BLEND)
            if len(p.color) == 3:
                gl.glColor3f(*p.color)
            elif len(p.color) == 4:
                gl.glColor4f(*p.color)
            x_size = self.parameters.size[0] / 2.0
            y_size = self.parameters.size[1] / 2.0
            x, y = center[0], center[1]
            x1 = x - x_size
            x2 = x + x_size
            y1 = y - y_size
            y2 = y + y_size
            gl.glBegin(gl.GL_QUADS)
            gl.glVertex2f(x1, y1)
            gl.glVertex2f(x2, y1)
            gl.glVertex2f(x2, y2)
            gl.glVertex2f(x1, y2)
            gl.glEnd()
        return


class FrameTimer():
    """Time inter frame intervals and compute frames per second."""

    def __init__(self, bin_start_msec=2, bin_stop_msec=28, bin_width_msec=2, running_average_num_frames=0, save_all_frametimes=False):
        """Create instance of FrameTimer."""
        self.bins = np.arange(bin_start_msec, bin_stop_msec, bin_width_msec)
        self.bin_width_msec = float(bin_width_msec)
        self.timing_histogram = np.zeros(self.bins.shape)
        self._true_time_last_frame = None
        self.longest_frame_draw_time_sec = None
        self.first_tick_sec = None
        self.total_frames = 0
        self.running_average_num_frames = running_average_num_frames
        if self.running_average_num_frames:
            self.last_n_frame_times_sec = [
             None] * self.running_average_num_frames
        self.save_all_frametimes = save_all_frametimes
        if self.save_all_frametimes:
            self.all_frametimes = []
        return

    def tick(self):
        """Declare a frame has just been drawn."""
        true_time_now = VisionEgg.true_time_func()
        if self._true_time_last_frame != None:
            this_frame_draw_time_sec = true_time_now - self._true_time_last_frame
            index = int(math.ceil(this_frame_draw_time_sec * 1000.0 / self.bin_width_msec)) - 1
            if index > len(self.timing_histogram) - 1:
                index = -1
            self.timing_histogram[index] += 1
            self.longest_frame_draw_time_sec = max(self.longest_frame_draw_time_sec, this_frame_draw_time_sec)
            if self.running_average_num_frames:
                self.last_n_frame_times_sec.append(true_time_now)
                self.last_n_frame_times_sec.pop(0)
        else:
            self.first_tick_sec = true_time_now
        self._true_time_last_frame = true_time_now
        if self.save_all_frametimes:
            self.all_frametimes.append(true_time_now)
        return

    def get_all_frametimes(self):
        if self.save_all_frametimes:
            return self.all_frametimes
        else:
            raise ValueError('must set save_all_frametimes')

    def get_longest_frame_duration_sec(self):
        return self.longest_frame_draw_time_sec

    def get_running_average_ifi_sec(self):
        if self.running_average_num_frames:
            frame_times = []
            for frame_time in self.last_n_frame_times_sec:
                if frame_time is not None:
                    frame_times.append(frame_time)

            if len(frame_times) >= 2:
                return (frame_times[(-1)] - frame_times[0]) / len(frame_times)
        else:
            raise RuntimeError('running_average_num_frames not set when creating FrameTimer instance')
        return

    def get_average_ifi_sec(self):
        if self._true_time_last_frame is None:
            raise RuntimeError("No frames were drawn, can't calculate average IFI")
        return (self._true_time_last_frame - self.first_tick_sec) / sum(self.timing_histogram)

    def print_histogram(self):
        logger = logging.getLogger('VisionEgg.Core')
        logger.warning('print_histogram() method of FrameTimer is deprecated will stop being supported. Use log_histogram() instead.')
        self.log_histogram()

    def log_histogram(self):
        """Send histogram to logger."""
        buffer = StringIO.StringIO()
        n_frames = sum(self.timing_histogram) + 1
        if n_frames < 2:
            print >> buffer, '%d frames were drawn.' % n_frames
            return
        average_ifi_sec = self.get_average_ifi_sec()
        print >> buffer, '%d frames were drawn.' % int(n_frames)
        print >> buffer, 'Mean IFI was %.2f msec (%.2f fps), longest IFI was %.2f msec.' % (
         average_ifi_sec * 1000.0, 1.0 / average_ifi_sec, self.longest_frame_draw_time_sec * 1000.0)
        h = hist = self.timing_histogram
        maxhist = float(max(h))
        if maxhist == 0:
            print >> buffer, 'No frames were drawn.'
            return
        lines = min(10, int(math.ceil(maxhist)))
        hist = hist / maxhist * float(lines)
        print >> buffer, 'histogram:'
        for line in range(lines):
            val = float(lines) - 1.0 - float(line)
            timing_string = '%6d   ' % (round(maxhist * val / lines),)
            q = np.greater(hist, val)
            for qi in q:
                s = ' '
                if qi:
                    s = '*'
                timing_string += '%4s ' % (s,)

            print >> buffer, timing_string

        timing_string = ' Time: '
        timing_string += '%4d ' % (0, )
        for bin in self.bins[:-1]:
            timing_string += '%4d ' % (bin,)

        timing_string += '+(msec)\n'
        timing_string += 'Total:    '
        for hi in h:
            if hi <= 999:
                num_str = str(int(hi)).center(5)
            else:
                num_str = ' +++ '
            timing_string += num_str

        print >> buffer, timing_string
        buffer.seek(0)
        logger = logging.getLogger('VisionEgg.Core')
        logger.info(buffer.read())


import VisionEgg.Deprecated
Message = VisionEgg.Deprecated.Message
message = VisionEgg.Deprecated.Message()
gl_assumptions = []

def add_gl_assumption(gl_variable, required_value, failure_callback):
    """Save assumptions for later checking once OpenGL context created."""
    if type(failure_callback) != types.FunctionType:
        raise ValueError('failure_callback must be a function!')
    gl_assumptions.append((gl_variable, required_value, failure_callback))


def init_gl_extension(prefix, name):
    global gl
    logger = logging.getLogger('VisionEgg.Core')
    if gl is VisionEgg.GLTrace:
        watched = True
        gl = VisionEgg.GLTrace.gl
    else:
        watched = False
    module_name = 'OpenGL.GL.%(prefix)s.%(name)s' % locals()
    try:
        exec 'import ' + module_name
    except ImportError:
        logger.warning('Could not import %s -- some features will be missing.' % (
         module_name,))
        return False

    module = eval(module_name)
    init_function_name = 'glInit' + name.title().replace('_', '') + prefix
    init_function = getattr(module, init_function_name)
    if not init_function():
        logger.warning('Could not initialize %s -- some features will be missing.' % (
         module_name,))
        return False
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if attr_name.startswith('__'):
            continue
        elif attr_name == init_function_name:
            continue
        elif attr_name == 'gl':
            continue
        elif type(attr) == type(VisionEgg):
            continue
        gl_attr_name = attr_name
        setattr(gl, gl_attr_name, attr)

    if watched:
        VisionEgg.GLTrace.gl_trace_attach()
        gl = VisionEgg.GLTrace
    return True


def post_gl_init():
    """Called by Screen instance. Requires OpenGL context to be created."""
    logger = logging.getLogger('VisionEgg.Core')
    if gl_version < '1.3':
        if not init_gl_extension('ARB', 'multitexture'):
            logger.warning('multitexturing not available.  Some features will not be available')
    else:
        if not hasattr(gl, 'glActiveTexture'):
            logger.debug('PyOpenGL bug: OpenGL multitexturing not available even though OpenGL is 1.3 or greater. Attempting ctypes-based workaround.')
            VisionEgg.PlatformDependent.attempt_to_load_multitexturing()
        if hasattr(gl, 'glActiveTexture'):
            gl.glActiveTextureARB = gl.glActiveTexture
            gl.glMultiTexCoord2fARB = gl.glMultiTexCoord2f
            gl.GL_TEXTURE0_ARB = gl.GL_TEXTURE0
            gl.GL_TEXTURE1_ARB = gl.GL_TEXTURE1
    if gl_version < '1.2':
        if init_gl_extension('EXT', 'bgra'):
            gl.GL_BGRA = gl.GL_BGRA_EXT
    for (gl_variable, required_value, failure_callback) in gl_assumptions:
        if gl_variable == '__SPECIAL__':
            if required_value == 'linux_nvidia_or_new_ATI':
                ok = 0
                if 'nvidia' == gl_vendor.split()[0].lower():
                    ok = 1
                if gl_renderer.startswith('Mesa DRI Radeon'):
                    date = gl_renderer.split()[3]
                    if date > '20021216':
                        ok = 1
                if not ok:
                    failure_callback()
            else:
                raise RuntimeError, 'Unknown gl_assumption: %s == %s' % (gl_variable, required_value)
        elif gl_variable.upper() == 'GL_VERSION':
            value_str = gl_version.split()[0]
            value_ints = map(int, value_str.split('.'))
            value = float(str(value_ints[0]) + '.' + ('').join(map(str, value_ints[1:])))
            if value < required_value:
                failure_callback()
        else:
            raise RuntimeError, 'Unknown gl_assumption'

    try:
        gl.GL_CLAMP_TO_EDGE
    except AttributeError:
        if gl_version >= '1.2':
            logger.debug('GL_CLAMP_TO_EDGE is not defined. Because you have OpenGL version 1.2 or greater, this is probably a bug in PyOpenGL.  Assigning GL_CLAMP_TO_EDGE to the value that is usually used.')
            gl.GL_CLAMP_TO_EDGE = 33071
        else:
            try:
                init_gl_extension('SGIS', 'texture_edge_clamp')
                gl.GL_CLAMP_TO_EDGE = gl.GL_CLAMP_TO_EDGE_SGIS
            except:
                logger.warning('GL_CLAMP_TO_EDGE is not available.  OpenGL version is less than 1.2, and the texture_edge_clamp_SGIS extension failed to load. It may be impossible to get exact 1:1 reproduction of textures.  Using GL_CLAMP instead of GL_CLAMP_TO_EDGE.')
                gl.GL_CLAMP_TO_EDGE = gl.GL_CLAMP


import VisionEgg.FlowControl
Presentation = VisionEgg.FlowControl.Presentation
Controller = VisionEgg.FlowControl.Controller
ConstantController = VisionEgg.FlowControl.ConstantController
EvalStringController = VisionEgg.FlowControl.EvalStringController
ExecStringController = VisionEgg.FlowControl.ExecStringController
FunctionController = VisionEgg.FlowControl.FunctionController
EncapsulatedController = VisionEgg.FlowControl.EncapsulatedController