# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\cocos\particle.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 26227 bytes
"""Particle system engine"""
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import random, math, numpy, ctypes, pyglet
from pyglet import gl
from cocos.cocosnode import CocosNode
from cocos.euclid import Point2
import cocos.director as director
from cocos.shader import ShaderProgram
forced_point_sprites = None

def point_sprites_available():
    """
    Returns:
        bool: tells if ``point sprites`` are available.

    For development and diagonostic :class:`cocos.particle.forced_point_sprites`
    could be set to force the desired return value.
    """
    if forced_point_sprites is not None:
        return forced_point_sprites
    have_point_sprites = True
    try:
        gl.glEnable(gl.GL_POINT_SPRITE)
        gl.glDisable(gl.GL_POINT_SPRITE)
    except:
        have_point_sprites = False
    else:
        return have_point_sprites


class ExceptionNoEmptyParticle(Exception):
    __doc__ = 'Particle system has no room for another particle.'


rand = lambda : random.random() * 2 - 1

def PointerToNumpy(a, ptype=ctypes.c_float):
    """PointerToNumpy(a, ptype=ctypes.c_float)

    Provides a ctype pointer to a Numpy array.

    Arguments:
        a (numpy.array): The Numpy array.
        ptype (ctypes): The ctypes type contained in the array.

    Returns:
        Pointer to the Numpy array.

    """
    a = numpy.ascontiguousarray(a)
    return a.ctypes.data_as(ctypes.POINTER(ptype))


class Color(object):
    __doc__ = 'Representation of a rgba color\n\n    Arguments:\n        r (float): red component\n        g (float): green component\n        b (float): blue component\n        a (float): alpha component\n    '

    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def to_array(self):
        """Convert :class:`Color` to a tuple.

        Returns:
            tuple: r, g, b and a components.
        """
        return (
         self.r, self.g, self.b, self.a)

    def __repr__(self):
        return 'Color({0:.2f}, {1:.2f}, {2:.2f}, {3:.2f})'.format(self.r, self.g, self.b, self.a)


class ParticleSystem(CocosNode):
    __doc__ = '\n    Base class for many flavors of cocos particle systems.\n\n    The easiest way to customize is to subclass and redefine some class attributes;\n    see :mod:`cocos.particle_systems` for examples.\n\n    To define a per-class custom texture, override :meth:`load_texture`.\n    To use a per-instance custom texture, pass it in the __init__ texture kw-param\n\n    Arguments:\n        fallback (Optional[None, True, False]): Defaults to None.\n            \n            - False: use point sprites, faster, not always available\n            - True: use quads, slower but always available\n            - None: autodetect, use the fastest available\n        texture (Optional[pyglet.image.Texture]): The texture image to be used for\n            the particles.\n    '
    POSITION_FREE, POSITION_GROUPED = range(2)
    active = True
    duration = 0
    elapsed = 0
    gravity = Point2(0.0, 0.0)
    pos_var = Point2(0.0, 0.0)
    angle = 0.0
    angle_var = 0.0
    speed = 0.0
    speed_var = 0.0
    tangential_accel = 0.0
    tangential_accel_var = 0.0
    radial_accel = 0.0
    radial_accel_var = 0.0
    size = 0.0
    size_var = 0.0
    life = 0
    life_var = 0
    start_color = Color(0.0, 0.0, 0.0, 0.0)
    start_color_var = Color(0.0, 0.0, 0.0, 0.0)
    end_color = Color(0.0, 0.0, 0.0, 0.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)
    total_particles = 0
    texture = None
    blend_additive = False
    color_modulate = True
    position_type = POSITION_GROUPED

    def __init__(self, fallback=None, texture=None):
        """
        fallback can be None, True, False; default is None
            False: use point sprites, faster, not always available
            True: use quads, slower but always available)
            None: autodetect, use the faster available
        texture: The texture image to be used for the particles.
        """
        super(ParticleSystem, self).__init__()
        self.particle_pos = numpy.zeros((self.total_particles, 2), numpy.float32)
        self.particle_dir = numpy.zeros((self.total_particles, 2), numpy.float32)
        self.particle_rad = numpy.zeros((self.total_particles, 1), numpy.float32)
        self.particle_tan = numpy.zeros((self.total_particles, 1), numpy.float32)
        self.particle_grav = numpy.zeros((self.total_particles, 2), numpy.float32)
        self.particle_color = numpy.zeros((self.total_particles, 4), numpy.float32)
        self.particle_delta_color = numpy.zeros((self.total_particles, 4), numpy.float32)
        self.particle_life = numpy.zeros((self.total_particles, 1), numpy.float32)
        self.particle_life.fill(-1.0)
        self.particle_size = numpy.zeros((self.total_particles, 1), numpy.float32)
        self.particle_size_scaled = self.particle_size
        self.start_pos = numpy.zeros((self.total_particles, 2), numpy.float32)
        self.emit_counter = 0
        self.particle_count = 0
        self.auto_remove_on_finish = False
        if texture is None:
            if self.texture is None:
                self.load_texture()
        else:
            self.texture = texture
        if fallback is None:
            fallback = not point_sprites_available()
        else:
            self.fallback = fallback
            if fallback:
                self._fallback_init()
                self.draw = self.draw_fallback
            else:
                self._init_shader()
        self.schedule(self.step)

    def _init_shader(self):
        vertex_code = '\n        #version 120\n        attribute float particle_size;\n\n        void main()\n        {\n            gl_PointSize = particle_size;\n            gl_Position = ftransform();\n            gl_FrontColor = gl_Color;\n        }\n        '
        frag_code = '\n        #version 120\n        uniform sampler2D sprite_texture;\n\n        void main()\n        {\n            gl_FragColor = gl_Color * texture2D(sprite_texture, gl_PointCoord);\n        }\n        '
        self.sprite_shader = ShaderProgram.simple_program('sprite', vertex_code, frag_code)
        self.particle_size_idx = gl.glGetAttribLocation(self.sprite_shader.program, b'particle_size')

    def load_texture(self):
        """Sets the default texture used by all instances of this particles system.

        Override this method to change the default texture.

        Note:
            By `issue #168 <https://github.com/los-cocos/cocos/issues/168>`_ 
            the texture should hold only one image, so don't use::

                texture = pyglet.resource.image('z.png').texture # (produces an atlas, ie multiple images in a texture)

            You can use instead::

                texture = pyglet.image.load(...).get_texture()
                # Or using pyglet resource mechanism
                texture = pyglet.image.load('filename.png', file=pyglet.resource.file('filename.png')).get_texture()
        """
        pic = pyglet.image.load('fire.png', file=(pyglet.resource.file('fire.png')))
        self.__class__.texture = pic.get_texture()

    def on_enter(self):
        super(ParticleSystem, self).on_enter()
        director.push_handlers(self)

    def on_exit(self):
        super(ParticleSystem, self).on_exit()
        director.remove_handlers(self)

    def on_cocos_resize(self, usable_width, usable_height):
        """Handler for windows resize.

        Arguments:
            usable_width (int): New window width.
            usable_height (int): New window height.
        """
        self._scale_particle_size()

    @CocosNode.scale.setter
    def scale(self, s):
        super(ParticleSystem, ParticleSystem).scale.__set__(self, s)
        self._scale_particle_size()

    def _scale_particle_size(self):
        """Resize the particles in respect to node scaling and window resize;
        only used when rendering with shaders.
        """
        node = self
        scale = 1.0
        while node.parent:
            scale *= node.scale
            node = node.parent

        if director.autoscale:
            scale *= 1.0 * director._usable_width / director._window_virtual_width
        self.particle_size_scaled = self.particle_size * scale

    def draw(self):
        """Draw the particles system"""
        gl.glPushMatrix()
        self.transform()
        gl.glPushAttrib(gl.GL_CURRENT_BIT)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glEnable(gl.GL_PROGRAM_POINT_SIZE)
        gl.glEnable(gl.GL_POINT_SPRITE)
        gl.glTexEnvi(gl.GL_POINT_SPRITE, gl.GL_COORD_REPLACE, gl.GL_TRUE)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        vertex_ptr = PointerToNumpy(self.particle_pos)
        gl.glVertexPointer(2, gl.GL_FLOAT, 0, vertex_ptr)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        color_ptr = PointerToNumpy(self.particle_color)
        gl.glColorPointer(4, gl.GL_FLOAT, 0, color_ptr)
        gl.glEnableVertexAttribArray(self.particle_size_idx)
        size_ptr = PointerToNumpy(self.particle_size_scaled)
        gl.glVertexAttribPointer(self.particle_size_idx, 1, gl.GL_FLOAT, False, 0, size_ptr)
        gl.glPushAttrib(gl.GL_COLOR_BUFFER_BIT)
        gl.glEnable(gl.GL_BLEND)
        if self.blend_additive:
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
        else:
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        self.sprite_shader.install()
        self.sprite_shader.usetTex('sprite_texture', 0, gl.GL_TEXTURE_2D, self.texture.id)
        gl.glDrawArrays(gl.GL_POINTS, 0, self.total_particles)
        self.sprite_shader.uninstall()
        gl.glPopAttrib()
        gl.glPopAttrib()
        gl.glDisableVertexAttribArray(self.particle_size_idx)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisable(gl.GL_POINT_SPRITE)
        gl.glDisable(gl.GL_PROGRAM_POINT_SIZE)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glPopMatrix()

    def step(self, delta):
        """Called every frame to create new particles if needed and
        update the particles position.

        If a duration was given to this particle system, the method will check
        if it needs to remove itself from its parent node when its time has 
        arrived.

        Arguments:
            delta (float): time in seconds since last frame.
        """
        self.particle_count = numpy.sum(self.particle_life >= 0)
        if self.active:
            rate = 1.0 / self.emission_rate
            self.emit_counter += delta
            while self.particle_count < self.total_particles:
                if self.emit_counter > rate:
                    self.add_particle()
                    self.emit_counter -= rate

            self.elapsed += delta
            if self.duration != -1:
                if self.duration < self.elapsed:
                    self.stop_system()
        self.update_particles(delta)
        if not self.active:
            if self.particle_count == 0:
                if self.auto_remove_on_finish is True:
                    self.unschedule(self.step)
                    self.parent.remove(self)

    def add_particle(self):
        """
        Code calling add_particle must either:
            - be sure there is room for the particle
            - be prepared to catch the exception :class:`ExceptionNoEmptyParticle`
          
        It is acceptable to ``try: ... except...: pass``
        """
        self.init_particle()
        self.particle_count += 1

    def stop_system(self):
        """Stop the particle system."""
        self.active = False
        self.elapsed = self.duration
        self.emit_counter = 0

    def reset_system(self):
        """Resets the particle system."""
        self.elapsed = self.duration
        self.emit_counter = 0

    def update_particles(self, delta):
        """Updates particles position.

        Arguments:
            delta (float): time in seconds since last frame.
        """
        norm = numpy.sqrt(self.particle_pos[:, 0] ** 2 + self.particle_pos[:, 1] ** 2)
        norm = numpy.select([norm == 0], [1e-07], default=norm)
        posx = self.particle_pos[:, 0] / norm
        posy = self.particle_pos[:, 1] / norm
        radial = numpy.array([posx, posy])
        tangential = numpy.array([-posy, posx])
        radial = numpy.swapaxes(radial, 0, 1)
        radial *= self.particle_rad
        tangential = numpy.swapaxes(tangential, 0, 1)
        tangential *= self.particle_tan
        self.particle_dir += (tangential + radial + self.particle_grav) * delta
        self.particle_pos += self.particle_dir * delta
        self.particle_life -= delta
        if self.position_type == self.POSITION_FREE:
            tuple = numpy.array([self.x, self.y])
            tmp = tuple - self.start_pos
            self.particle_pos -= tmp
        self.particle_color += self.particle_delta_color * delta
        self.particle_color[:, 3] = numpy.select([self.particle_life[:, 0] < 0], [0], default=(self.particle_color[:, 3]))

    def init_particle(self):
        """Set initial particles state."""
        a = self.particle_life < 0
        idxs = a.nonzero()
        idx = -1
        if len(idxs[0]) > 0:
            idx = idxs[0][0]
        else:
            raise ExceptionNoEmptyParticle()
        self.particle_pos[idx][0] = self.pos_var.x * rand()
        self.particle_pos[idx][1] = self.pos_var.y * rand()
        self.start_pos[idx][0] = self.x
        self.start_pos[idx][1] = self.y
        a = math.radians(self.angle + self.angle_var * rand())
        v = Point2(math.cos(a), math.sin(a))
        s = self.speed + self.speed_var * rand()
        dir = v * s
        self.particle_dir[idx][0] = dir.x
        self.particle_dir[idx][1] = dir.y
        self.particle_rad[idx] = self.radial_accel + self.radial_accel_var * rand()
        self.particle_tan[idx] = self.tangential_accel + self.tangential_accel_var * rand()
        life = self.particle_life[idx] = self.life + self.life_var * rand()
        sr = self.start_color.r + self.start_color_var.r * rand()
        sg = self.start_color.g + self.start_color_var.g * rand()
        sb = self.start_color.b + self.start_color_var.b * rand()
        sa = self.start_color.a + self.start_color_var.a * rand()
        self.particle_color[idx][0] = sr
        self.particle_color[idx][1] = sg
        self.particle_color[idx][2] = sb
        self.particle_color[idx][3] = sa
        er = self.end_color.r + self.end_color_var.r * rand()
        eg = self.end_color.g + self.end_color_var.g * rand()
        eb = self.end_color.b + self.end_color_var.b * rand()
        ea = self.end_color.a + self.end_color_var.a * rand()
        delta_color_r = (er - sr) / life
        delta_color_g = (eg - sg) / life
        delta_color_b = (eb - sb) / life
        delta_color_a = (ea - sa) / life
        self.particle_delta_color[idx][0] = delta_color_r
        self.particle_delta_color[idx][1] = delta_color_g
        self.particle_delta_color[idx][2] = delta_color_b
        self.particle_delta_color[idx][3] = delta_color_a
        self.particle_size[idx] = self.size + self.size_var * rand()
        self._scale_particle_size()
        self.particle_grav[idx][0] = self.gravity.x
        self.particle_grav[idx][1] = self.gravity.y

    def _fallback_init(self):
        self.vertexs = numpy.zeros((self.total_particles, 4, 2), numpy.float32)
        tex_coords_for_quad = numpy.array([[0.0, 1.0], [0.0, 0.0], [1.0, 0.0], [1.0, 1.0]], numpy.float32)
        self.tex_coords = numpy.zeros((self.total_particles, 4, 2), numpy.float32)
        self.tex_coords[:] = tex_coords_for_quad[numpy.newaxis, :, :]
        self.per_vertex_colors = numpy.zeros((self.total_particles, 4, 4), numpy.float32)
        self.delta_pos_to_vertex = numpy.zeros((self.total_particles, 4, 2), numpy.float32)

    def draw_fallback(self):
        """Called instead of :meth:`draw` when quads are used instead of
        Point Sprite.
        """
        self.make_delta_pos_to_vertex()
        self.update_vertexs_from_pos()
        self.update_per_vertex_colors()
        gl.glPushMatrix()
        self.transform()
        gl.glPushAttrib(gl.GL_CURRENT_BIT)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture.id)
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        vertexs_ptr = PointerToNumpy(self.vertexs)
        gl.glVertexPointer(2, gl.GL_FLOAT, 0, vertexs_ptr)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        color_ptr = PointerToNumpy(self.per_vertex_colors)
        gl.glColorPointer(4, gl.GL_FLOAT, 0, color_ptr)
        gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        tex_coord_ptr = PointerToNumpy(self.tex_coords)
        gl.glTexCoordPointer(2, gl.GL_FLOAT, 0, tex_coord_ptr)
        gl.glPushAttrib(gl.GL_COLOR_BUFFER_BIT)
        gl.glEnable(gl.GL_BLEND)
        if self.blend_additive:
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE)
        else:
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glDrawArrays(gl.GL_QUADS, 0, len(self.vertexs) * 4)
        gl.glPopAttrib()
        gl.glPopAttrib()
        gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glPopMatrix()

    def update_vertexs_from_pos(self):
        """Helper function to update particle quad vertices based
        on particle position.
        """
        vertexs = self.vertexs
        delta = self.delta_pos_to_vertex
        pos = self.particle_pos
        vertexs[:] = delta + pos[:, numpy.newaxis, :]

    def update_per_vertex_colors(self):
        """Helper function to update particle quad colors based
        on particle color.
        """
        colors = self.particle_color
        per_vertex_colors = self.per_vertex_colors
        per_vertex_colors[:] = colors[:, numpy.newaxis, :]

    def make_delta_pos_to_vertex(self):
        """Helper function creating quad vertices based on particles
        position.
        """
        size2 = self.particle_size / 2.0
        self.delta_pos_to_vertex[:, 0] = numpy.array([-size2, +size2]).T
        self.delta_pos_to_vertex[:, 1] = numpy.array([-size2, -size2]).T
        self.delta_pos_to_vertex[:, 2] = numpy.array([+size2, -size2]).T
        self.delta_pos_to_vertex[:, 3] = numpy.array([+size2, +size2]).T