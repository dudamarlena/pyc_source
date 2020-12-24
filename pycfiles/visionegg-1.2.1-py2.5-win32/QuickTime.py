# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\VisionEgg\QuickTime.py
# Compiled at: 2009-07-07 11:29:42
"""
QuickTime movies in the Vision Egg.

"""
import VisionEgg, VisionEgg.gl_qt, VisionEgg.qtmovie as qtmovie, VisionEgg.Textures, numpy.oldnumeric as Numeric, os, VisionEgg.GL as gl
__version__ = VisionEgg.release_name
__author__ = 'Andrew Straw <astraw@users.sourceforge.net>'
new_movie_from_filename = qtmovie.new_movie_from_filename

class MovieTexture(VisionEgg.Textures.Texture):
    __slots__ = ('movie', 'size', 'scale', 'gl_qt_renderer')

    def __init__(self, movie=None, texture_size=None):
        if not isinstance(movie, qtmovie.Movie):
            if isinstance(movie, str) or isinstance(movie, unicode):
                movie = new_movie_from_filename(filename=movie)
        self.movie = movie
        bounds = self.movie.GetMovieBox()
        height = bounds.bottom - bounds.top
        width = bounds.right - bounds.left
        self.movie.SetMovieBox(qtmovie.Rect(top=0, left=0, bottom=height, right=width))
        self.size = (width, height)
        self.scale = 1.0

    def make_half_size(self):
        self.size = (
         self.size[0] / 2, self.size[1] / 2)
        self.scale = self.scale / 2

    def unload(self):
        raise NotImplementedError('')

    def get_texels_as_image(self):
        raise NotImplementedError('')

    def load(self, texture_object, build_mipmaps=False, rescale_original_to_fill_texture_object=False, internal_format=gl.GL_RGB):
        if build_mipmaps:
            raise ValueError('cannot build mipmaps for QuickTime movies')
        if rescale_original_to_fill_texture_object:
            raise NotImplementedError('')
        (width, height) = self.size
        tex_shape = VisionEgg.Textures.next_power_of_2(max(width, height))
        self.buf_lf = 0.0
        self.buf_rf = float(width) / tex_shape
        self.buf_bf = 0.0
        self.buf_tf = float(height) / tex_shape
        self._buf_l = 0
        self._buf_r = width
        self._buf_b = 0
        self._buf_t = height
        buffer = Numeric.zeros((tex_shape, tex_shape), Numeric.UInt8)
        texture_object.put_new_image(buffer, internal_format=gl.GL_RGB, mipmap_level=0)
        self.texture_object = texture_object
        self.gl_qt_renderer = VisionEgg.gl_qt.gl_qt_renderer_create(self.movie, tex_shape, self.scale)

    def update(self):
        VisionEgg.gl_qt.gl_qt_renderer_update(self.gl_qt_renderer)

    def __del__(self):
        VisionEgg.gl_qt.gl_qt_renderer_delete(self.gl_qt_renderer)