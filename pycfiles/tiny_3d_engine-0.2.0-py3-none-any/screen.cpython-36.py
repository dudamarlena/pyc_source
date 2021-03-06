# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/tiny_3d_engine/src/tiny_3d_engine/screen.py
# Compiled at: 2020-04-20 18:54:32
# Size of source mod 2**32: 5651 bytes
"""
Screen utilities
----------------

All the graphical toolkit of the 3D engine.
This module take care of the declaration and packing of the canvas,
and the drawing of the polylines.
"""
__all__ = [
 'Screen', 'shade_color']
import tkinter
from tkinter import font

def hex2rgb(str_rgb):
    """Convert hexadecimal color to rgb"""
    try:
        rgb = str_rgb[1:]
        if len(rgb) == 6:
            red, grn, blu = rgb[0:2], rgb[2:4], rgb[4:6]
        else:
            if len(rgb) == 9:
                red, grn, blu = rgb[0:3], rgb[3:6], rgb[6:9]
            else:
                if len(rgb) == 3:
                    red, grn, blu = rgb[0] * 2, rgb[1] * 2, rgb[2] * 2
                else:
                    raise ValueError()
    except:
        raise ValueError('Invalid value %r provided for rgb color.' % str_rgb)

    return tuple(int(val, 16) for val in (red, grn, blu))


def rgb2hex(list_rgb):
    """Convert rgb list to hex"""
    return '#{:02x}{:02x}{:02x}'.format(list_rgb[0], list_rgb[1], list_rgb[2])


def shade_color(hex_color, bg_hex_color, shade):
    """Return the same color, bkended with background.

    :param color: color in HEX
    :param shade: float : 0 no blend, 1 transparent"
    """
    shade = max(shade, 0)
    shade = min(shade, 1)
    rgb_color = hex2rgb(hex_color)
    rgb_back = hex2rgb(bg_hex_color)
    blend = list()
    for i in range(3):
        val = int(rgb_color[i] * (1.0 - shade) + shade * rgb_back[i])
        blend.append(val)

    return rgb2hex(blend)


class Screen:
    __doc__ = 'Handle all the memory-to-screen dialog\n    '

    def __init__(self, width, height, background, root=None, title=None):
        """Startup class"""
        self.holder = self._create_holder(root)
        self.motion_allowed = True
        self.help_lbl = tkinter.Label((self.holder),
          text='Command help')
        self.help_lbl.bind('<Button-1>', self.spawn_help_panel)
        self.help_lbl.pack(side='bottom', fill='x')
        self.current_tag = None
        self.can = tkinter.Canvas((self.holder),
          width=width,
          height=height,
          bg=background)
        self.can.pack(side='bottom', fill='x')
        self.font_hud = font.Font(family='Helvetica', size=24)
        self.bg_color = background
        self.focus_color = '#00ccff'
        self.colors = None
        if self.standalone:
            self.holder.title(title)

    def update(self, colors):
        """Update informations on parts to show"""
        self.colors = colors

    def spawn_help_panel(self, event):
        """ add a help panel"""
        top = tkinter.Toplevel()
        top.title('Command help...')
        msg = tkinter.Message(top, text='\n=======================\nTiny 3D engine commands\n=======================\n\nr / R : *** reset view ***\n\nMouse + Butt. 1 : rotation\n\nShift + Mouse + Butt. 1 : translation\n\nZ / z : zoom in / zoom out\n\nD / d : fisheye / perspective\n\nh / H : hide part / hide family\n\nw / W : rotate 90deg. left / right\n\nx / X : rotate 90deg. up / down\n\nc / C : spin 90deg. clockwise / anticl.\n\n')
        msg.pack()

    def _create_holder(self, root):
        """Creet the main window if needed"""
        if root is None:
            holder = tkinter.Tk()
            self.standalone = True
        else:
            holder = root
            self.standalone = False
        return holder

    def createShape(self, points, tag, s_color):
        """draw shape on screen"""
        self.can.create_polygon(points,
          fill=s_color,
          outline=s_color,
          tags=tag)

    def add_tags_bindings(self, list_tags):
        """Add the tag bindings on all parts"""
        for tag in list_tags:
            self.can.tag_bind(tag, '<Enter>', lambda event, arg=tag: self.enter_tag(event, arg))
            self.can.tag_bind(tag, '<Leave>', lambda event, arg=tag: self.leave_tag(event, arg))

    def enter_tag(self, event, tag):
        """Callback whe the mouse enters on a tagged surface"""
        self.motion_allowed = False
        self.current_tag = tag
        self.can.itemconfigure(tag,
          outline=(self.focus_color),
          width=4)
        self.print_text_info(event.x + 11, event.y - 11, tag, 'white')
        self.print_text_info(event.x + 13, event.y - 11, tag, 'white')
        self.print_text_info(event.x + 11, event.y - 13, tag, 'white')
        self.print_text_info(event.x + 13, event.y - 13, tag, 'white')
        self.print_text_info(event.x + 12, event.y - 12, tag, 'black')

    def leave_tag(self, event, tag):
        """Callback whe the mouse leaves a tagged surface"""
        self.motion_allowed = True
        self.current_tag = None
        self.can.delete('info')
        self.can.itemconfigure(tag,
          outline=(self.colors[tag]),
          width=1)

    def print_text_info(self, xpix, ypix, text, color):
        """CPrint some text on the screen"""
        self.can.create_text(xpix,
          ypix, text=text,
          anchor='w',
          tags='info',
          fill=color,
          font=(self.font_hud))

    def clear(self):
        """clear the display"""
        self.can.delete('all')

    def mainloop(self):
        """ Start the interactive mode of the screen"""
        self.holder.mainloop()