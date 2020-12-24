# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treedraw/render.py
# Compiled at: 2017-10-18 08:39:32
# Size of source mod 2**32: 4255 bytes
import cairo, math

class Renderer:

    def __init__(self, f, width=800, height=600, border=2):
        self.filename = f
        self.width = width
        self.height = height
        self.border = border / math.sqrt(width ** 2 + height ** 2)
        self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, self.width, self.height)
        self.ctx = cairo.Context(self.surface)
        self.ctx.scale(self.width, self.height)
        self.ctx.rectangle(0, 0, 1, 1)
        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.fill()
        self.ctx.select_font_face('Inconsolata', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)

    def box(self, x, y, w, h, text=None):
        self.ctx.set_source_rgb(0, 0, 0)
        self.ctx.rectangle(x, y, w, h)
        self.ctx.fill()
        self.ctx.set_source_rgb(1, 1, 1)
        self.ctx.rectangle(x + self.border, y + self.border, w - 2 * self.border, h - 2 * self.border)
        self.ctx.fill()
        self.ctx.set_source_rgb(0, 0, 0)
        tx, ty, tw, th, tdx, tdy = self.ctx.text_extents(text)
        self.ctx.move_to(x + w / 2 - 3 * tw / 5, y + h / 2 + 2 * th / 5)
        self.ctx.show_text(text)

    def render_tree(self, tree):
        """
        Renders and exports a tree.
        """
        GAP_TOP = 0.1
        GRAPH_SPACE = 1 - GAP_TOP
        box_height = 0.6666666666666666 * (GRAPH_SPACE / tree.height)
        box_width = 0.8 * (GRAPH_SPACE / tree.width)
        gap_height = GRAPH_SPACE / (3 * tree.height)
        self.ctx.set_font_size(0.6666666666666667 * box_height)
        next_line = [
         tree.root]
        y = 0
        while not all([x == ' ' for x in next_line]):
            len_this_line = len(next_line)
            line_after = tree.get_children(next_line)
            len_next_line = len(line_after)
            gap = (1 - box_width * len_this_line) / (len_this_line + 1)
            gap_next = (1 - box_width * len_next_line) / (len_next_line + 1)
            x = 0
            for child in next_line:
                if child == ' ':
                    x += 1
                else:
                    self.box(gap + x * (box_width + gap), GAP_TOP + y * (box_height + gap_height), box_width, box_height, tree.symbols[child])
                    self.ctx.set_source_rgb(0, 0, 0)
                    self.ctx.set_line_width(self.border)
                    self.ctx.move_to(gap + x * (box_width + gap) + box_width / 2, GAP_TOP + y * (box_height + gap_height) + box_height)
                    if child in tree.links:
                        for grandchild in tree.links[child]:
                            if grandchild is ' ':
                                pass
                            else:
                                index = line_after.index(grandchild)
                                x_pos = gap_next + index * (box_width + gap_next) + box_width / 2
                                y_pos = GAP_TOP + (y + 1) * (box_height + gap_height)
                                self.ctx.line_to(x_pos, y_pos)
                                self.ctx.move_to(gap + x * (box_width + gap) + box_width / 2, 0.1 + y * (box_height + gap_height) + box_height)

                        self.ctx.stroke()
                    x += 1

            y += 1
            next_line = tree.get_children(next_line)

        self.surface.write_to_png('.'.join(self.filename.split('.')[:-1]) + '.png')