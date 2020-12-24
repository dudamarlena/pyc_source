# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/font/base.py
# Compiled at: 2009-02-18 19:37:25
"""Abstract classes used by pyglet.font implementations.

These classes should not be constructed directly.  Instead, use the functions
in `pyglet.font` to obtain platform-specific instances.  You can use these
classes as a documented interface to the concrete classes.
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: base.py 2278 2008-09-23 12:18:50Z Alex.Holkner $'
import unicodedata
from pyglet.gl import *
from pyglet import image
_other_grapheme_extend = map(unichr, [2494, 2519, 3043, 2903, 3006, 3031, 3266,
 3285, 3286, 3390, 3415, 3535, 3551, 8204,
 8205, 65438, 65439])
_logical_order_exception = map(unichr, range(3648, 3653) + range(3776, 3780))
_grapheme_extend = lambda c, cc: cc in ('Me', 'Mn') or c in _other_grapheme_extend
_CR = '\r'
_LF = '\n'
_control = lambda c, cc: cc in ('ZI', 'Zp', 'Cc', 'Cf') and c not in map(unichr, [13, 10, 8204, 8205])
_extend = lambda c, cc: _grapheme_extend(c, cc) or c in map(unichr, [3632, 3634, 3635, 3653, 3760, 3762, 3763])
_prepend = lambda c, cc: c in _logical_order_exception
_spacing_mark = lambda c, cc: cc == 'Mc' and c not in _other_grapheme_extend

def _grapheme_break(left, right):
    if left is None:
        return True
    if left == _CR and right == LF:
        return False
    left_cc = unicodedata.category(left)
    if _control(left, left_cc):
        return True
    right_cc = unicodedata.category(right)
    if _control(right, right_cc):
        return True
    if _extend(right, right_cc):
        return False
    if _spacing_mark(right, right_cc):
        return False
    if _prepend(left, left_cc):
        return False
    return True


def get_grapheme_clusters(text):
    """Implements Table 2 of UAX #29: Grapheme Cluster Boundaries.

    Does not currently implement Hangul syllable rules.
    
    :Parameters:
        `text` : unicode
            String to cluster.

    :since: pyglet 1.1.2

    :rtype: List of `unicode`
    :return: List of Unicode grapheme clusters
    """
    clusters = []
    cluster = ''
    left = None
    for right in text:
        if cluster and _grapheme_break(left, right):
            clusters.append(cluster)
            cluster = ''
        elif cluster:
            clusters.append('\u200b')
        cluster += right
        left = right

    if cluster:
        clusters.append(cluster)
    return clusters


class Glyph(image.TextureRegion):
    """A single glyph located within a larger texture.

    Glyphs are drawn most efficiently using the higher level APIs, for example
    `GlyphString`.

    :Ivariables:
        `advance` : int
            The horizontal advance of this glyph, in pixels.
        `vertices` : (int, int, int, int)
            The vertices of this glyph, with (0,0) originating at the
            left-side bearing at the baseline.

    """
    advance = 0
    vertices = (0, 0, 0, 0)

    def set_bearings(self, baseline, left_side_bearing, advance):
        """Set metrics for this glyph.

        :Parameters:
            `baseline` : int
                Distance from the bottom of the glyph to its baseline;
                typically negative.
            `left_side_bearing` : int
                Distance to add to the left edge of the glyph.
            `advance` : int
                Distance to move the horizontal advance to the next glyph.

        """
        self.advance = advance
        self.vertices = (
         left_side_bearing,
         -baseline,
         left_side_bearing + self.width,
         -baseline + self.height)

    def draw(self):
        """Debug method.
        
        Use the higher level APIs for performance and kerning.
        """
        glBindTexture(GL_TEXTURE_2D, self.owner.id)
        glBegin(GL_QUADS)
        self.draw_quad_vertices()
        glEnd()

    def draw_quad_vertices(self):
        """Debug method. 

        Use the higher level APIs for performance and kerning.
        """
        glTexCoord3f(*self.tex_coords[:3])
        glVertex2f(self.vertices[0], self.vertices[1])
        glTexCoord3f(*self.tex_coords[3:6])
        glVertex2f(self.vertices[2], self.vertices[1])
        glTexCoord3f(*self.tex_coords[6:9])
        glVertex2f(self.vertices[2], self.vertices[3])
        glTexCoord3f(*self.tex_coords[9:12])
        glVertex2f(self.vertices[0], self.vertices[3])

    def get_kerning_pair(self, right_glyph):
        """Not implemented.
        """
        return 0


class GlyphTextureAtlas(image.Texture):
    """A texture within which glyphs can be drawn.
    """
    region_class = Glyph
    x = 0
    y = 0
    line_height = 0

    def apply_blend_state(self):
        """Set the OpenGL blend state for the glyphs in this texture.
        """
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

    def fit(self, image):
        """Place `image` within this texture.

        :Parameters:
            `image` : `pyglet.image.AbstractImage`
                Image to place within the texture.

        :rtype: `Glyph`
        :return: The glyph representing the image from this texture, or None
            if the image doesn't fit.
        """
        if self.x + image.width > self.width:
            self.x = 0
            self.y += self.line_height
            self.line_height = 0
        if self.y + image.height > self.height:
            return
        self.line_height = max(self.line_height, image.height)
        region = self.get_region(self.x, self.y, image.width, image.height)
        if image.width > 0:
            region.blit_into(image, 0, 0, 0)
            self.x += image.width + 1
        return region


class GlyphRenderer(object):
    """Abstract class for creating glyph images.
    """

    def __init__(self, font):
        pass

    def render(self, text):
        raise NotImplementedError('Subclass must override')


class FontException(Exception):
    """Generic exception related to errors from the font module.  Typically
    these relate to invalid font data."""
    pass


class Font(object):
    """Abstract font class able to produce glyphs.

    To construct a font, use `pyglet.font.load`, which will instantiate the
    platform-specific font class.

    Internally, this class is used by the platform classes to manage the set
    of textures into which glyphs are written.

    :Ivariables:
        `ascent` : int
            Maximum ascent above the baseline, in pixels.
        `descent` : int
            Maximum descent below the baseline, in pixels. Usually negative.
    """
    texture_width = 256
    texture_height = 256
    texture_internalformat = GL_ALPHA
    ascent = 0
    descent = 0
    glyph_renderer_class = GlyphRenderer
    texture_class = GlyphTextureAtlas

    def __init__(self):
        self.textures = []
        self.glyphs = {}

    @classmethod
    def add_font_data(cls, data):
        """Add font data to the font loader.

        This is a class method and affects all fonts loaded.  Data must be
        some byte string of data, for example, the contents of a TrueType font
        file.  Subclasses can override this method to add the font data into
        the font registry.

        There is no way to instantiate a font given the data directly, you
        must use `pyglet.font.load` specifying the font name.
        """
        pass

    @classmethod
    def have_font(cls, name):
        """Determine if a font with the given name is installed.

        :Parameters:
            `name` : str
                Name of a font to search for

        :rtype: bool
        """
        return True

    def create_glyph(self, image):
        """Create a glyph using the given image.

        This is used internally by `Font` subclasses to add glyph data
        to the font.  Glyphs are packed within large textures maintained by
        `Font`.  This method inserts the image into a font texture and returns
        a glyph reference; it is up to the subclass to add metadata to the
        glyph.

        Applications should not use this method directly.

        :Parameters:
            `image` : `pyglet.image.AbstractImage`
                The image to write to the font texture.

        :rtype: `Glyph`
        """
        glyph = None
        for texture in self.textures:
            glyph = texture.fit(image)
            if glyph:
                break

        if not glyph:
            if image.width > self.texture_width or image.height > self.texture_height:
                texture = self.texture_class.create_for_size(GL_TEXTURE_2D, image.width * 2, image.height * 2, self.texture_internalformat)
                self.texture_width = texture.width
                self.texture_height = texture.height
            else:
                texture = self.texture_class.create_for_size(GL_TEXTURE_2D, self.texture_width, self.texture_height, self.texture_internalformat)
            self.textures.insert(0, texture)
            glyph = texture.fit(image)
        return glyph

    def get_glyphs(self, text):
        """Create and return a list of Glyphs for `text`.

        If any characters do not have a known glyph representation in this
        font, a substitution will be made.

        :Parameters:
            `text` : str or unicode
                Text to render.

        :rtype: list of `Glyph`
        """
        glyph_renderer = None
        glyphs = []
        for c in get_grapheme_clusters(unicode(text)):
            if c == '\t':
                c = ' '
            if c not in self.glyphs:
                if not glyph_renderer:
                    glyph_renderer = self.glyph_renderer_class(self)
                self.glyphs[c] = glyph_renderer.render(c)
            glyphs.append(self.glyphs[c])

        return glyphs

    def get_glyphs_for_width(self, text, width):
        """Return a list of glyphs for `text` that fit within the given width.
        
        If the entire text is larger than 'width', as much as possible will be
        used while breaking after a space or zero-width space character.  If a
        newline is enountered in text, only text up to that newline will be
        used.  If no break opportunities (newlines or spaces) occur within
        `width`, the text up to the first break opportunity will be used (this
        will exceed `width`).  If there are no break opportunities, the entire
        text will be used.

        You can assume that each character of the text is represented by
        exactly one glyph; so the amount of text "used up" can be determined
        by examining the length of the returned glyph list.

        :Parameters:
            `text` : str or unicode
                Text to render.
            `width` : int
                Maximum width of returned glyphs.
        
        :rtype: list of `Glyph`

        :see: `GlyphString`
        """
        glyph_renderer = None
        glyph_buffer = []
        glyphs = []
        for c in text:
            if c == '\n':
                glyphs += glyph_buffer
                break
            if c not in self.glyphs:
                if not glyph_renderer:
                    glyph_renderer = self.glyph_renderer_class(self)
                self.glyphs[c] = glyph_renderer.render(c)
            glyph = self.glyphs[c]
            glyph_buffer.append(glyph)
            width -= glyph.advance
            if width <= 0 and len(glyphs) > 0:
                break
            if c in ' \u200b':
                glyphs += glyph_buffer
                glyph_buffer = []

        if len(glyphs) == 0:
            glyphs = glyph_buffer
        return glyphs