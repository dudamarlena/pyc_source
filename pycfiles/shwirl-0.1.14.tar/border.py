# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/visuals/border.py
# Compiled at: 2016-11-03 01:40:19
import numpy as np
from . import Visual
from ..color import Color
VERT_SHADER_BORDER = '\nattribute vec2 a_position;\nattribute vec2 a_adjust_dir;\n\nvoid main() {\n    // First map the vertex to document coordinates\n    vec4 doc_pos = $visual_to_doc(vec4(a_position, 0, 1));\n\n    // Also need to map the adjustment direction vector, but this is tricky!\n    // We need to adjust separately for each component of the vector:\n    vec4 adjusted;\n    if ( a_adjust_dir.x == 0 ) {\n        // If this is an outer vertex, no adjustment for line weight is needed.\n        // (In fact, trying to make the adjustment would result in no\n        // triangles being drawn, hence the if/else block)\n        adjusted = doc_pos;\n    }\n    else {\n        // Inner vertexes must be adjusted for line width, but this is\n        // surprisingly tricky given that the rectangle may have been scaled\n        // and rotated!\n        vec4 doc_x = $visual_to_doc(vec4(a_adjust_dir.x, 0, 0, 0)) -\n                    $visual_to_doc(vec4(0, 0, 0, 0));\n        vec4 doc_y = $visual_to_doc(vec4(0, a_adjust_dir.y, 0, 0)) -\n                    $visual_to_doc(vec4(0, 0, 0, 0));\n        doc_x = normalize(doc_x);\n        doc_y = normalize(doc_y);\n\n        // Now doc_x + doc_y points in the direction we need in order to\n        // correct the line weight of _both_ segments, but the magnitude of\n        // that correction is wrong. To correct it we first need to\n        // measure the width that would result from using doc_x + doc_y:\n        vec4 proj_y_x = dot(doc_x, doc_y) * doc_x;  // project y onto x\n        float cur_width = length(doc_y - proj_y_x);  // measure current weight\n\n        // And now we can adjust vertex position for line width:\n        adjusted = doc_pos + ($border_width / cur_width) * (doc_x + doc_y);\n    }\n\n    // Finally map the remainder of the way to render coordinates\n    gl_Position = $doc_to_render(adjusted);\n}\n'
FRAG_SHADER_BORDER = '\nvoid main() {\n    gl_FragColor = $border_color;\n}\n'

class _BorderVisual(Visual):
    """
    Visual subclass to display 2D pixel-width borders.

    Parameters
    ----------
    pos : tuple (x, y)
        Position where the colorbar is to be placed with
        respect to the center of the colorbar
    halfdim : tuple (half_width, half_height)
        Half the dimensions of the colorbar measured
        from the center. That way, the total dimensions
        of the colorbar is (x - half_width) to (x + half_width)
        and (y - half_height) to (y + half_height)
    border_width : float (in px)
        The width of the border the colormap should have. This measurement
        is given in pixels
    border_color : str | vispy.color.Color
        The color of the border of the colormap. This can either be a
        str as the color's name or an actual instace of a vipy.color.Color
    """

    def __init__(self, pos, halfdim, border_width=1.0, border_color=None, **kwargs):
        self._pos = pos
        self._halfdim = halfdim
        self._border_width = border_width
        self._border_color = Color(border_color)
        Visual.__init__(self, vcode=VERT_SHADER_BORDER, fcode=FRAG_SHADER_BORDER, **kwargs)

    @staticmethod
    def _prepare_transforms(view):
        program = view.shared_program
        program.vert['visual_to_doc'] = view.transforms.get_transform('visual', 'document')
        program.vert['doc_to_render'] = view.transforms.get_transform('document', 'render')

    @property
    def visual_border_width(self):
        """ The border width in visual coordinates
        """
        render_to_doc = self.transforms.get_transform('document', 'visual')
        vec = render_to_doc.map([self.border_width, self.border_width, 0])
        origin = render_to_doc.map([0, 0, 0])
        visual_border_width = [
         vec[0] - origin[0], vec[1] - origin[1]]
        visual_border_width[1] *= -1
        return visual_border_width

    def _update(self):
        x, y = self._pos
        halfw, halfh = self._halfdim
        border_vertices = np.array([
         [
          x - halfw, y - halfh],
         [
          x - halfw, y - halfh],
         [
          x + halfw, y - halfh],
         [
          x + halfw, y - halfh],
         [
          x + halfw, y + halfh],
         [
          x + halfw, y + halfh],
         [
          x - halfw, y + halfh],
         [
          x - halfw, y + halfh],
         [
          x - halfw, y - halfh],
         [
          x - halfw, y - halfh]], dtype=np.float32)
        adjust_dir = np.array([
         [
          0, 0], [-1, -1],
         [
          0, 0], [1, -1],
         [
          0, 0], [1, 1],
         [
          0, 0], [-1, 1],
         [
          0, 0], [-1, -1]], dtype=np.float32)
        self.shared_program['a_position'] = border_vertices
        self.shared_program['a_adjust_dir'] = adjust_dir
        self.shared_program.vert['border_width'] = self._border_width
        self.shared_program.frag['border_color'] = self._border_color.rgba

    def _prepare_draw(self, view=None):
        self._update()
        self._draw_mode = 'triangle_strip'
        return True

    @property
    def border_width(self):
        """ The width of the border
        """
        return self._border_width

    @border_width.setter
    def border_width(self, border_width):
        self._border_width = border_width
        self._update()

    @property
    def border_color(self):
        """ The color of the border in pixels
        """
        return self._border_color

    @border_color.setter
    def border_color(self, border_color):
        self._border_color = Color(border_color)
        self.shared_program.frag['border_color'] = self._border_color.rgba

    @property
    def pos(self):
        """ The center of the BorderVisual
        """
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos
        self._update()

    @property
    def halfdim(self):
        """ The half-dimensions measured from the center of the BorderVisual
        """
        return self._halfdim

    @halfdim.setter
    def halfdim(self, halfdim):
        self._halfdim = halfdim
        self._update()