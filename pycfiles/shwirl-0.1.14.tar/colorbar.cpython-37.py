# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vohl/Documents/code/shwirl/shwirl/extern/vispy/visuals/colorbar.py
# Compiled at: 2018-10-02 11:14:03
# Size of source mod 2**32: 24175 bytes
import numpy as np
from . import Visual, TextVisual, CompoundVisual, _BorderVisual
from .shaders import Function
from ..color import get_colormap
VERT_SHADER = '\nattribute vec2 a_position;\nattribute vec2 a_texcoord;\nvarying vec2 v_texcoord;\n\nvoid main() {\n    v_texcoord = a_texcoord;\n    gl_Position = $transform(vec4(a_position, 0, 1));\n}\n'
FRAG_SHADER_HORIZONTAL = '\nvarying vec2 v_texcoord;\n\nvoid main()\n{\n    vec4 mapped_color = $color_transform(v_texcoord.x);\n    gl_FragColor = mapped_color;\n}\n'
FRAG_SHADER_VERTICAL = "\nvarying vec2 v_texcoord;\n\nvoid main()\n{\n    // we get the texcoords inverted (with respect to the colormap)\n    // so let's invert it to make sure that the colorbar renders correctly\n    vec4 mapped_color = $color_transform(1.0 - v_texcoord.y);\n    gl_FragColor = mapped_color;\n}\n"

class _CoreColorBarVisual(Visual):
    __doc__ = "\n    Visual subclass that actually renders the ColorBar.\n\n    Parameters\n    ----------\n     pos : tuple (x, y)\n        Position where the colorbar is to be placed with\n        respect to the center of the colorbar\n    halfdim : tuple (half_width, half_height)\n        Half the dimensions of the colorbar measured\n        from the center. That way, the total dimensions\n        of the colorbar is (x - half_width) to (x + half_width)\n        and (y - half_height) to (y + half_height)\n    cmap : str | vispy.color.ColorMap\n        Either the name of the ColorMap to be used from the standard\n        set of names (refer to `vispy.color.get_colormap`),\n        or a custom ColorMap object.\n        The ColorMap is used to apply a gradient on the colorbar.\n     orientation : {'left', 'right', 'top', 'bottom'}\n        The orientation of the colorbar, used for rendering. The\n        orientation can be thought of as the position of the label\n        relative to the color bar.\n\n    Note\n    ----\n    This is purely internal.\n    Externally, the ColorBarVisual must be used.\n    This class was separated out to encapsulate rendering information\n    That way, ColorBar simply becomes a CompoundVisual\n\n    See Also\n    --------\n    vispy.visuals.ColorBarVisual\n    "

    def __init__(self, pos, halfdim, cmap, orientation, **kwargs):
        self._cmap = get_colormap(cmap)
        self._pos = pos
        self._halfdim = halfdim
        self._orientation = orientation
        if orientation == 'top' or orientation == 'bottom':
            (Visual.__init__)(self, vcode=VERT_SHADER, fcode=FRAG_SHADER_HORIZONTAL, **kwargs)
        else:
            if orientation == 'left' or orientation == 'right':
                (Visual.__init__)(self, vcode=VERT_SHADER, fcode=FRAG_SHADER_VERTICAL, **kwargs)
            else:
                raise _CoreColorBarVisual._get_orientation_error(self._orientation)
        tex_coords = np.array([[0, 0], [1, 0], [1, 1],
         [
          0, 0], [1, 1], [0, 1]],
          dtype=(np.float32))
        glsl_map_fn = Function(self._cmap.glsl_map)
        self.shared_program.frag['color_transform'] = glsl_map_fn
        self.shared_program['a_texcoord'] = tex_coords.astype(np.float32)
        self._update()

    def _update(self):
        """Rebuilds the shaders, and repositions the objects
           that are used internally by the ColorBarVisual
        """
        x, y = self._pos
        halfw, halfh = self._halfdim
        x += 2.5 * halfw
        if halfw <= 0:
            raise ValueError('half-width must be positive and non-zero, not %s' % halfw)
        elif halfh <= 0:
            raise ValueError('half-height must be positive and non-zero, not %s' % halfh)
        elif self._orientation == 'bottom' or self._orientation == 'top':
            if halfw < halfh:
                raise ValueError('half-width(%s) < half-height(%s) for%s orientation, expected half-width >= half-height' % (
                 halfw, halfh, self._orientation))
        elif halfw > halfh:
            raise ValueError('half-width(%s) > half-height(%s) for%s orientation, expected half-width <= half-height' % (
             halfw, halfh, self._orientation))
        vertices = np.array([[x - halfw, y - halfh],
         [
          x + halfw, y - halfh],
         [
          x + halfw, y + halfh],
         [
          x - halfw, y - halfh],
         [
          x + halfw, y + halfh],
         [
          x - halfw, y + halfh]],
          dtype=(np.float32))
        self.shared_program['a_position'] = vertices

    @staticmethod
    def _get_orientation_error(orientation):
        return ValueError("orientation must be one of 'top', 'bottom', 'left', or 'right', not '%s'" % (
         orientation,))

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos
        self._update()

    @property
    def halfdim(self):
        return self._halfdim

    @halfdim.setter
    def halfdim(self, halfdim):
        self._halfdim = halfdim

    @property
    def cmap(self):
        """ The colormap of the Colorbar
        """
        return self._cmap

    @cmap.setter
    def cmap(self, cmap):
        self._cmap = get_colormap(cmap)
        self._program.frag['color_transform'] = Function(self._cmap.glsl_map)

    @staticmethod
    def _prepare_transforms(view):
        program = view.view_program
        total_transform = view.transforms.get_transform()
        program.vert['transform'] = total_transform

    def _prepare_draw(self, view):
        self._draw_mode = 'triangles'
        return True


class ColorBarVisual(CompoundVisual):
    __doc__ = "Visual subclass displaying a colorbar\n\n    Parameters\n    ----------\n    cmap : str | vispy.color.ColorMap\n        Either the name of the ColorMap to be used from the standard\n        set of names (refer to `vispy.color.get_colormap`),\n        or a custom ColorMap object.\n        The ColorMap is used to apply a gradient on the colorbar.\n    orientation : {'left', 'right', 'top', 'bottom'}\n        The orientation of the colorbar, used for rendering. The\n        orientation can be thought of as the position of the label\n        relative to the color bar.\n\n        When the orientation is 'left' or 'right', the colorbar is\n        vertically placed. When it is 'top' or 'bottom', the colorbar is\n        horizontally placed.\n\n            * 'top': the colorbar is horizontal.\n              Color is applied from left to right.\n              Minimum corresponds to left and maximum to right.\n              Label is to the top of the colorbar\n\n            * 'bottom': Same as top, except that\n              label is to the bottom of the colorbar\n\n            * 'left': the colorbar is vertical.\n              Color is applied from bottom to top.\n              Minimum corresponds to bottom and maximum to top.\n              Label is to the left of the colorbar\n\n            * 'right': Same as left, except that the\n              label is placed to the right of the colorbar\n\n    size : (major_axis_length, minor_axis_length)\n        lengths with respect to the major and minor axes.\n        The minor axis is the shorter axis, while the major axis is\n        the longer axis with respect to the orientation\n\n        For orientations 'top' and 'bottom', the major axis is\n        along the length.\n\n        For orientations 'left' and 'right', the major axis is\n        along the breadth\n    pos : tuple (x, y)\n        Position where the colorbar is to be placed with\n        respect to the center of the colorbar\n    label_str : str\n        The label that is to be drawn with the colorbar\n        that provides information about the colorbar.\n    label_color : str | vispy.color.Color\n        The color of the labels. This can either be a\n        str as the color's name or an actual instace of a vipy.color.Color\n    clim : tuple (min, max)\n        the minimum and maximum values of the data that\n        is given to the colorbar. This is used to draw the scale\n        on the side of the colorbar.\n    border_width : float (in px)\n        The width of the border the colormap should have. This measurement\n        is given in pixels\n    border_color : str | vispy.color.Color\n        The color of the border of the colormap. This can either be a\n        str as the color's name or an actual instace of a vipy.color.Color\n    "
    text_padding_factor = -0.95

    def __init__(self, cmap, orientation, size, pos=[
 0, 0], label_str='', label_color='black', clim=(0.0, 1.0), border_width=1.0, border_color='black', **kwargs):
        self._label_str = label_str
        self._label_color = label_color
        self._cmap = get_colormap(cmap)
        self._clim = clim
        self._pos = pos
        self._size = size
        self._orientation = orientation
        self._label = TextVisual((self._label_str), color=(self._label_color))
        self._ticks = []

        def isfloat(value):
            try:
                float(value)
                return True
            except:
                return False

        if isfloat(self._clim[0]):
            self._ticks.append(TextVisual(('{:.4f}'.format(self._clim[0])), color=(self._label_color)))
            self._ticks.append(TextVisual(('{:.4f}'.format(self._clim[1])), color=(self._label_color)))
        else:
            self._ticks.append(TextVisual((str(self._clim[0])), color=(self._label_color)))
            self._ticks.append(TextVisual((str(self._clim[1])), color=(self._label_color)))
        if orientation in ('top', 'bottom'):
            width, height = size
        else:
            if orientation in ('left', 'right'):
                height, width = size
            else:
                raise _CoreColorBarVisual._get_orientation_error(orientation)
        self._halfdim = (
         width * 0.5, height * 0.5)
        self._colorbar = _CoreColorBarVisual(pos, self._halfdim, cmap, orientation)
        self._border = _BorderVisual(pos, self._halfdim, border_width, border_color)
        CompoundVisual.__init__(self, [self._colorbar,
         self._border,
         self._ticks[0],
         self._ticks[1],
         self._label])
        self._update()

    def _update(self):
        """Rebuilds the shaders, and repositions the objects
           that are used internally by the ColorBarVisual
        """
        self._colorbar.halfdim = self._halfdim
        self._border.halfdim = self._halfdim
        self._label.text = self._label_str
        import numbers
        if isinstance(self._clim[0], int):
            self._ticks[0].text = str(self._clim[0])
            self._ticks[1].text = str(self._clim[1])
        else:
            self._ticks[0].text = '{:.4f}'.format(self._clim[0])
            self._ticks[1].text = '{:.4f}'.format(self._clim[1])
        self._update_positions()
        self._colorbar._update()
        self._border._update()

    def _update_positions(self):
        """
        updates the positions of the colorbars and labels

        """
        self._colorbar.pos = self._pos
        self._border.pos = self._pos
        if self._orientation == 'right' or self._orientation == 'left':
            self._label.rotation = -90
        x, y = self._pos
        halfw, halfh = self._halfdim
        label_anchors = ColorBarVisual._get_label_anchors(center=(self._pos), halfdim=(self._halfdim),
          orientation=(self._orientation),
          transforms=(self.label.transforms))
        self._label.anchors = label_anchors
        ticks_anchors = ColorBarVisual._get_ticks_anchors(center=(self._pos), halfdim=(self._halfdim),
          orientation=(self._orientation),
          transforms=(self.label.transforms))
        self._ticks[0].anchors = ticks_anchors
        self._ticks[1].anchors = ticks_anchors
        label_pos, ticks_pos = ColorBarVisual._calc_positions(center=(self._pos), halfdim=(self._halfdim),
          border_width=(self.border_width),
          orientation=(self._orientation),
          transforms=(self.transforms))
        self._label.pos = label_pos
        self._ticks[0].pos = ticks_pos[0]
        self._ticks[1].pos = ticks_pos[1]

    @staticmethod
    def _get_label_anchors(center, halfdim, orientation, transforms):
        visual_to_doc = transforms.get_transform('visual', 'document')
        doc_x = visual_to_doc.map(np.array([1, 0, 0, 0], dtype=(np.float32)))
        doc_y = visual_to_doc.map(np.array([0, 1, 0, 0], dtype=(np.float32)))
        if doc_x[0] < 0:
            doc_x *= -1
        if doc_y[1] < 0:
            doc_y *= -1
        if orientation == 'bottom':
            perp_direction = doc_y
        else:
            if orientation == 'top':
                perp_direction = -doc_y
            else:
                if orientation == 'left':
                    perp_direction = -doc_x
                else:
                    if orientation == 'right':
                        perp_direction = doc_x
                    else:
                        perp_direction = np.array(perp_direction, dtype=(np.float32))
                        perp_direction /= np.linalg.norm(perp_direction)
                        if orientation in ('left', 'right'):
                            x = perp_direction[0]
                            y = perp_direction[1]
                            perp_direction[0] = -y
                            perp_direction[1] = x
                        else:
                            anchors = []
                            if perp_direction[0] < 0:
                                anchors.append('right')
                            else:
                                if perp_direction[0] > 0:
                                    anchors.append('left')
                                else:
                                    anchors.append('center')
                            if perp_direction[1] < 0:
                                anchors.append('bottom')
                            else:
                                if perp_direction[1] > 0:
                                    anchors.append('top')
                                else:
                                    anchors.append('middle')
                    return anchors

    @staticmethod
    def _get_ticks_anchors(center, halfdim, orientation, transforms):
        visual_to_doc = transforms.get_transform('visual', 'document')
        doc_x = visual_to_doc.map(np.array([1, 0, 0, 0], dtype=(np.float32)))
        doc_y = visual_to_doc.map(np.array([0, 1, 0, 0], dtype=(np.float32)))
        if doc_x[0] < 0:
            doc_x *= -1
        if doc_y[1] < 0:
            doc_y *= -1
        if orientation == 'bottom':
            perp_direction = doc_y
        else:
            if orientation == 'top':
                perp_direction = -doc_y
            else:
                if orientation == 'left':
                    perp_direction = -doc_x
                else:
                    if orientation == 'right':
                        perp_direction = doc_x
                    else:
                        perp_direction = np.array(perp_direction, dtype=(np.float32))
                        perp_direction /= np.linalg.norm(perp_direction)
                        anchors = []
                        if perp_direction[0] < 0:
                            anchors.append('right')
                        else:
                            if perp_direction[0] > 0:
                                anchors.append('left')
                            else:
                                anchors.append('center')
                        if perp_direction[1] < 0:
                            anchors.append('bottom')
                        else:
                            if perp_direction[1] > 0:
                                anchors.append('top')
                            else:
                                anchors.append('middle')
                    return anchors

    @staticmethod
    def _calc_positions(center, halfdim, border_width, orientation, transforms):
        """
        Calculate the text centeritions given the ColorBar
        parameters.

        Note
        ----
        This is static because in principle, this
        function does not need access to the state of the ColorBar
        at all. It's a computation function that computes coordinate
        transforms

        Parameters
        ----------
        center: tuple (x, y)
            Center of the ColorBar
        halfdim: tuple (halfw, halfh)
            Half of the dimensions measured from the center
        border_width: float
            Width of the border of the ColorBar
        orientation: "top" | "bottom" | "left" | "right"
            Position of the label with respect to the ColorBar
        transforms: TransformSystem
            the transforms of the ColorBar
        """
        x, y = center
        halfw, halfh = halfdim
        visual_to_doc = transforms.get_transform('visual', 'document')
        doc_to_visual = transforms.get_transform('document', 'visual')
        doc_x = visual_to_doc.map(np.array([halfw, 0, 0, 0], dtype=(np.float32)))
        doc_y = visual_to_doc.map(np.array([0, halfh, 0, 0], dtype=(np.float32)))
        if doc_x[0] < 0:
            doc_x *= -1
        if doc_y[1] < 0:
            doc_y *= -1
        if orientation == 'top':
            doc_perp_vector = -doc_y
        else:
            if orientation == 'bottom':
                doc_perp_vector = doc_y
            else:
                if orientation == 'left':
                    doc_perp_vector = -doc_x
                else:
                    if orientation == 'right':
                        doc_perp_vector = doc_x
                    perp_len = np.linalg.norm(doc_perp_vector)
                    doc_perp_vector /= perp_len
                    perp_len += border_width
                    perp_len += 5
                    perp_len *= ColorBarVisual.text_padding_factor
                    doc_perp_vector *= perp_len
                    doc_center = visual_to_doc.map(np.array([x, y, 0, 0], dtype=(np.float32)))
                    doc_label_pos = doc_center + doc_perp_vector
                    visual_label_pos = doc_to_visual.map(doc_label_pos)[:3]
                    if orientation in ('top', 'bottom'):
                        doc_ticks_pos = [
                         doc_label_pos - doc_x,
                         doc_label_pos + doc_x]
                    else:
                        doc_ticks_pos = [
                         doc_label_pos + doc_y,
                         doc_label_pos - doc_y]
                visual_ticks_pos = []
                visual_ticks_pos.append(doc_to_visual.map(doc_ticks_pos[0])[:3])
                visual_ticks_pos.append(doc_to_visual.map(doc_ticks_pos[1])[:3])
                return (
                 visual_label_pos, visual_ticks_pos)

    @property
    def pos(self):
        """ The position of the text anchor in the local coordinate frame
        """
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos
        self._update_positions()

    @property
    def cmap(self):
        """ The colormap of the Colorbar
        """
        return self._colorbar._cmap

    @cmap.setter
    def cmap(self, cmap):
        self._colorbar.cmap = cmap

    @property
    def clim(self):
        """ The data limits of the Colorbar

        Returns
        -------
        clim: tuple(min, max)
        """
        return self._clim

    @clim.setter
    def clim(self, clim):
        self._clim = clim
        self._update()

    @property
    def label(self):
        """ The vispy.visuals.TextVisual associated with the label
        """
        return self._label

    @label.setter
    def label(self, label):
        self._label = label
        self._update()

    @property
    def label_str(self):
        return self._label_str

    @label_str.setter
    def label_str(self, label_str):
        self._label_str = label_str
        self._update()

    @property
    def ticks(self):
        """ The vispy.visuals.TextVisual associated with the ticks

        Returns
        -------
        ticks: [vispy.visual.TextVisual]
            The array is of length 2
        """
        return self._ticks

    @ticks.setter
    def ticks(self, ticks):
        self._ticks = ticks
        self._update()

    @property
    def border_width(self):
        """ The width of the border around the ColorBar in pixels
        """
        return self._border.border_width

    @border_width.setter
    def border_width(self, border_width):
        self._border.border_width = border_width
        self._update()

    @property
    def border_color(self):
        """ The color of the border around the ColorBar in pixels
        """
        return self._border.border_color

    @border_color.setter
    def border_color(self, border_color):
        self._border.border_color = border_color
        self._update()

    @property
    def orientation(self):
        """ The orientation of the ColorBar
        """
        return self._orientation

    @property
    def size(self):
        """ The size of the ColorBar

        Returns
        -------
        size: (major_axis_length, minor_axis_length)
            major and minor axis are defined by the
            orientation of the ColorBar
        """
        halfw, halfh = self._halfdim
        if self.orientation in ('top', 'bottom'):
            return (
             halfw * 2.0, halfh * 2.0)
        return (halfh * 2.0, halfw * 2.0)

    @size.setter
    def size(self, size):
        if size[0] < size[1]:
            raise ValueError('Major axis must be greater than or equal to Minor axis. Given Major axis: (%s) < Minor axis (%s)' % (
             size[0],
             size[1]))
        elif self.orientation in ('top', 'bottom'):
            width, height = size
        else:
            height, width = size
        if width < 0.0:
            raise ValueError('width must be non-negative, not %s ' % (width,))
        else:
            if width == 0.0:
                raise ValueError('width must be non-zero, not %s' % (width,))
            elif height < 0.0:
                raise ValueError('height must be non-negative, not %s ' % (
                 height,))
            else:
                if height == 0.0:
                    raise ValueError('height must be non-zero, not %s' % (height,))
            self._halfdim = (
             width / 2.0, height / 2.0)
            self._update()