# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\cocos2020\cocos\text.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 9686 bytes
"""Text support

CocosNodes subclasses supporting text.
They use a suitable pyglet text object to do the work.
Functionality other that the one common to all cococsnodes, except 'opacity', is
provided by the member 'element' , which is the underlying pyglet object.
"""
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import cocos.director as director
from cocos.cocosnode import CocosNode
import pyglet
from pyglet.graphics import OrderedGroup
from pyglet import image
from pyglet import gl

class TextElement(CocosNode):
    __doc__ = "\n    Base class for all cocos text\n\n    Provides the CocosNode interfase and a pyglet Batch to store parts\n    Functionality other that the one common to all cococsnodes, except 'opacity', is\n    provided by the member 'element' , which is the underlying pyglet object.\n    "

    def __init__(self, text='', position=(0, 0), **kwargs):
        super(TextElement, self).__init__()
        self.position = position
        self.args = []
        self.kwargs = kwargs
        kwargs['text'] = text
        self.group = None
        self.batch = None
        self.batch = pyglet.graphics.Batch()
        self.create_element()

    def create_element(self):
        self.element = (self.klass)(group=self.group, batch=self.batch, **self.kwargs)

    def draw(self):
        gl.glPushMatrix()
        self.transform()
        self.batch.draw()
        gl.glPopMatrix()

    def _get_opacity(self):
        return self.element.color[3]

    def _set_opacity(self, value):
        self.element.color = tuple(self.element.color[:3]) + (int(value),)

    opacity = property(_get_opacity, _set_opacity)


class Label(TextElement):
    __doc__ = 'Plain text support\n\n    Functionality other that the one common to all cococsnodes, except \'opacity\', is\n    provided by the member \'element\' , which is the underlying pyglet object.\n    The undelying pyglet object is pyglet.text.Label\n\n    For pyglet 1.1.4 the available init keyword arguments are\n        - font_name: Font family name(s); the first matching name is used\n        - font_size: Font size, in points\n        - bold: bool\n        - italic: bool\n        - color: (int, int, int, int) Font colour, as RGBA\n        - width: Width of the label in pixels, or None\n        - height: Height of the label in pixels, or None\n        - anchor_x: one of "left", "center" or "right"\n        - anchor_y : one of "bottom", "baseline", "center" or "top"\n        - align : applies when width is supplied. One of "left", "center" or "right".\n        - multiline: bool\n        - dpi: Resolution of the fonts in this layout. Defaults to 96.\n\n    '
    klass = pyglet.text.Label


class HTMLLabel(TextElement):
    __doc__ = 'HTML formatted text label (supports a subset of HTML 4.01)\n\n    Functionality other that the one common to all cococsnodes, except \'opacity\', is\n    provided by the member \'element\' , which is the underlying pyglet object.\n    The undelying pyglet object is pyglet.text.HTMLLabel.\n\n    For pyglet 1.1.4 the available init keyword arguments are\n        - location: Location object for loading images referred to in the document. By default, the working directory is used.\n        - width: Width of the label in pixels, or None\n        - height: Height of the label in pixels, or None\n        - anchor_x: "left", "center" or "right".\n        - anchor_y: one of "bottom", "baseline", "center" or "top".\n        - multiline : bool\n        - dpi : float, defaults to 96\n\n    '
    klass = pyglet.text.HTMLLabel


class PygletRichLabel(pyglet.text.DocumentLabel):
    __doc__ = 'This is not a CocosNode - let instantiation be handled by RichLabel\n\n    Helper class for RichLabel\n    '

    def __init__(self, text='', font_name=None, font_size=None, bold=False, italic=False, color=None, x=0, y=0, width=None, height=None, anchor_x='left', anchor_y='baseline', align='left', multiline=False, dpi=None, batch=None, group=None):
        """Create a rich text label.

        :Parameters:
            `text` : str
                Pyglet attributed (rich) text to display.
            `font_name` : str or list
                Font family name(s).  If more than one name is given, the
                first matching name is used.
            `font_size` : float
                Font size, in points.
            `bold` : bool
                Bold font style.
            `italic` : bool
                Italic font style.
            `color` : (int, int, int, int) or None
                Font colour, as RGBA components in range [0, 255].
                None to use font colors defined by text attributes.
            `x` : int
                X coordinate of the label.
            `y` : int
                Y coordinate of the label.
            `width` : int
                Width of the label in pixels, or None
            `height` : int
                Height of the label in pixels, or None
            `anchor_x` : str
                Anchor point of the X coordinate: one of ``"left"``,
                ``"center"`` or ``"right"``.
            `anchor_y` : str
                Anchor point of the Y coordinate: one of ``"bottom"``,
                ``"baseline"``, ``"center"`` or ``"top"``.
            `align` : str
                Horizontal alignment of text on a line, only applies if
                a width is supplied. One of ``"left"``, ``"center"``
                or ``"right"``.
            `multiline` : bool
                If True, the label will be word-wrapped and accept newline
                characters.  You must also set the width of the label.
            `dpi` : float
                Resolution of the fonts in this layout.  Defaults to 96.
            `batch` : `Batch`
                Optional graphics batch to add the label to.
            `group` : `Group`
                Optional graphics group to use.

        """
        text = '{color (255, 255, 255, 255)}' + text
        document = pyglet.text.decode_attributed(text)
        super(PygletRichLabel, self).__init__(document, x, y, width, height, anchor_x, anchor_y, multiline, dpi, batch, group)
        style = dict(align=align)
        if font_name:
            style['font_name'] = font_name
        if font_size:
            style['font_size'] = font_size
        if bold:
            style['bold'] = bold
        if italic:
            style['italic'] = italic
        if color:
            style['color'] = color
        self.document.set_style(0, len(self.document.text), style)


class RichLabel(TextElement):
    __doc__ = 'displays pyglet attributed (rich) text\n\n    The undelying pyglet object is a custom, cocos provided PygletRichLabel\n    element, subclass of pyglet.text.DocumentLabel.\n\n    For pyglet 1.1.4 the available init keyword arguments are\n        - font_name: Font family name(s); first matching is used\n        - font_size: Font size, in points.\n        - bold: bool\n        - italic: bool\n        - color : (int, int, int, int) or None\n        - width: Width of the label in pixels, or None\n        - height: Height of the label in pixels, or None\n        - anchor_x: "left", "center" or "right"\n        - anchor_y: one of "bottom", "baseline", "center" or "top"\n        - align :  only when a width is supplied. One of "left", "center", "right".\n        - multiline : bool\n        - dpi : Resolution of the fonts in this layout.  Defaults to 96.\n\n    '
    klass = PygletRichLabel