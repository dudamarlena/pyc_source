# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vincent/Projects/PythonMinitor/minitorgui/minitorgui/shapes.py
# Compiled at: 2020-02-22 08:55:39
# Size of source mod 2**32: 21179 bytes
"""
Main code for shapes.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import uuid
from abc import ABC, abstractmethod
from itertools import cycle
__author__ = 'Vincent Schouten <inquiry@intoreflection.co>'
__docformat__ = 'google'
__date__ = '06-12-2019'
__copyright__ = 'Copyright 2019, Vincent Schouten'
__credits__ = ['Vincent Schouten']
__license__ = 'MIT'
__maintainer__ = 'Vincent Schouten'
__email__ = '<inquiry@intoreflection.co>'
__status__ = 'Development'
THICKNESS_LINE_CLIENT = 2
THICKNESS_LINE_MACHINE = 2
THICKNESS_LINE_AGENT = 2
THICKNESS_LINE_TUNNEL = 1
THICKNESS_PACKET = 2
BACKGROUND_CANVAS = '#232729'
LABEL_FONT_COLOUR = 'white'
CLIENT_OUTLINE_COLOUR = 'white'
MACHINE_OUTLINE_COLOUR = 'white'
AGENT_OUTLINE_COLOUR = 'white'
TUNNEL_OUTLINE_COLOUR = 'white'
PACKET_OUTLINE_COLOUR = '#c0c0c0'
PACKET_FILL_COLOUR = '#232729'
BANNER_TUNNEL_SUCCESS = '#4d4dff'
BANNER_TUNNEL_FAILURE = 'red'

class Base(ABC):
    __doc__ = '______________.'

    def __init__(self, main_window):
        self.status = main_window.inner_window.canvas_window.status
        self.canvas = main_window.inner_window.canvas_window.canvas
        self.scale = main_window.scale
        self.type = None

    @property
    def _generate_tag(self):
        name = f"{self.type}-{uuid.uuid4().hex}"
        return name

    def _get_tunnel_metrics(self, component_a, component_b, factor=0.05):
        _, _, ax2, _ = self.canvas.coords(component_a)
        bx1, by1, _, by2 = self.canvas.coords(component_b)
        distance = bx1 - ax2
        height = (by2 - by1) * factor
        start_pos_x = ax2
        pos_y = (by2 - by1) / 2 + by1
        return (distance, height, start_pos_x, pos_y)


class Shape(Base):
    __doc__ = '______________.'

    def __init__(self, main_window):
        super().__init__(main_window)
        self.tag_shape = None
        self.tag_label = None

    @abstractmethod
    def render(self):
        """Creates an item (shape) on the canvas and hides it."""
        pass

    @abstractmethod
    def show(self):
        """Shows the hidden item (shape)."""
        pass

    def _add_label(self):
        coord_x1, coord_y1, coord_x2, _ = self.canvas.coords(self.tag_shape)
        distance = coord_x2 - coord_x1
        pos_x = coord_x1 + distance / 2
        pos_y = coord_y1 - 10 * self.scale
        self.canvas.create_text(pos_x, pos_y,
          text=(self.type),
          font=('', 8, 'normal'),
          fill=LABEL_FONT_COLOUR,
          tags=(self.tag_label))

    def setup_ok(self, line=False):
        """________."""
        colour = 'green'
        if line:
            self.canvas.itemconfig((self.tag_shape), fill=colour)
        else:
            self.canvas.itemconfig((self.tag_shape), outline=colour)

    def setup_nok(self, line=False):
        """________."""
        colour = 'red'
        if line:
            self.canvas.itemconfig((self.tag_shape), fill=colour)
        else:
            self.canvas.itemconfig((self.tag_shape), outline=colour)

    def dim(self, line=False):
        """________."""
        colour = 'white'
        if line:
            self.canvas.itemconfig((self.tag_shape), fill=colour)
        else:
            self.canvas.itemconfig((self.tag_shape), outline=colour)


class Animation(Base):
    __doc__ = '______________.'

    def __init__(self, main_window):
        Base.__init__(self, main_window)

    @abstractmethod
    def start(self):
        """______________."""
        pass

    @abstractmethod
    def stop(self):
        """______________."""
        pass


class ClientShape(Shape):
    __doc__ = '______________.'

    def __init__(self, main_window, start_pos_x, start_pos_y):
        super().__init__(main_window)
        self.type = 'client'
        self.tag_shape = self._generate_tag
        self.tag_label = self._generate_tag
        self.start_pos_x = start_pos_x
        self.start_pos_y = start_pos_y
        self.width = 90 * self.scale
        self.height = self.width * 0.7
        self.count_elements = 0

    def render(self):
        outer_screen = self._draw_outer_screen()
        self._draw_inner_screen(outer_screen)
        keyboard = self._draw_keyboard(outer_screen)
        self._draw_spacebar(keyboard)

    def show(self):
        self.canvas.itemconfig((self.tag_shape), state='normal')
        colours = ['#b2b2b2', '#b2b2b2', '#7f7f7f', '#b2b2b2', 'white']
        colour_cycle = cycle(colours)
        max_elements = len(colours) - 1

        def _flicker():
            if self.count_elements <= max_elements:
                self.count_elements += 1
                self.canvas.itemconfig((self.tag_shape), outline=(next(colour_cycle)))
                self.canvas.after(100, _flicker)

        _flicker()
        self._add_label()

    def _draw_outer_screen(self):
        shape = self.canvas.create_rectangle((self.start_pos_x), (self.start_pos_y),
          (self.start_pos_x + self.width),
          (self.start_pos_y + self.height),
          width=(THICKNESS_LINE_CLIENT * self.scale),
          outline=CLIENT_OUTLINE_COLOUR,
          tags=(self.tag_shape),
          state='hidden')
        return shape

    def _draw_inner_screen(self, tag_shape):
        coord_x1, coord_y1, coord_x2, coord_y2 = self.canvas.coords(tag_shape)
        total_width = coord_x2 - coord_x1
        total_height = coord_y2 - coord_y1
        width = (coord_x2 - coord_x1) * 0.9
        height = (coord_y2 - coord_y1) * 0.9
        start_pos_x = coord_x1 + (total_width - width) / 2
        start_pos_y = coord_y1 + (total_height - height) / 2
        shape = self.canvas.create_rectangle(start_pos_x, start_pos_y,
          (start_pos_x + width),
          (start_pos_y + height),
          width=1,
          outline=CLIENT_OUTLINE_COLOUR,
          tags=(self.tag_shape),
          state='hidden')
        return shape

    def _draw_keyboard(self, tag_shape):
        coord_x1, coord_y1, coord_x2, coord_y2 = self.canvas.coords(tag_shape)
        width = coord_x2 - coord_x1
        total_height = coord_y2 - coord_y1
        height = (coord_y2 - coord_y1) * 0.7
        start_pos_x = coord_x1
        start_pos_y = coord_y2 + total_height * 0.05
        shape = self.canvas.create_rectangle(start_pos_x, start_pos_y,
          (start_pos_x + width),
          (start_pos_y + height),
          width=(THICKNESS_LINE_CLIENT * self.scale),
          outline=CLIENT_OUTLINE_COLOUR,
          tags=(self.tag_shape),
          state='hidden')
        return shape

    def _draw_spacebar(self, tag_shape):
        coord_x1, coord_y1, coord_x2, coord_y2 = self.canvas.coords(tag_shape)
        total_width = coord_x2 - coord_x1
        total_height = coord_y2 - coord_y1
        width = total_width * 0.5
        height = total_height * 0.2
        start_pos_x = coord_x1 + (total_width - width) * 0.5
        start_pos_y = coord_y1 + (total_height - height) * 0.8
        shape = self.canvas.create_rectangle(start_pos_x, start_pos_y,
          (start_pos_x + width),
          (start_pos_y + height),
          fill='',
          width=1,
          outline=CLIENT_OUTLINE_COLOUR,
          tags=(self.tag_shape),
          state='hidden')
        return shape


class MachineShape(Shape):
    __doc__ = '______________.'

    def __init__(self, main_window, start_pos_x, start_pos_y):
        super().__init__(main_window)
        self.type = 'machine'
        self.tag_shape = self._generate_tag
        self.tag_label = self._generate_tag
        self.start_pos_x = start_pos_x
        self.start_pos_y = start_pos_y
        self.width = 90 * self.scale
        self.height = self.width * 1.4
        self.count_elements = 0

    def render(self):
        machine_x1 = self.start_pos_x
        machine_y1 = self.start_pos_y
        machine_x2 = self.start_pos_x + self.width
        machine_y2 = self.start_pos_y + self.height
        self.canvas.create_rectangle(machine_x1, machine_y1,
          machine_x2,
          machine_y2,
          width=(THICKNESS_LINE_MACHINE * self.scale),
          outline=MACHINE_OUTLINE_COLOUR,
          tags=(self.tag_shape),
          state='hidden')

    def show(self):
        self.canvas.itemconfig((self.tag_shape), state='normal')
        colours = ['#b2b2b2', '#b2b2b2', '#7f7f7f', '#b2b2b2', 'white']
        colour_cycle = cycle(colours)
        max_elements = len(colours) - 1

        def _flicker():
            if self.count_elements <= max_elements:
                self.count_elements += 1
                self.canvas.itemconfig((self.tag_shape), outline=(next(colour_cycle)))
                self.canvas.after(120, _flicker)

        _flicker()
        self._add_label()


class AgentShape(Shape):
    __doc__ = '______________.'

    def __init__(self, main_window, client, machine):
        super().__init__(main_window)
        self.type = 'agent'
        self.tag_shape = self._generate_tag
        self.tag_label = self._generate_tag
        self.tag_shape_machine = machine.tag_shape
        self.tag_shape_client = client.tag_shape
        self.terminate = False
        self.index = 0
        self.distance = 0

    def render(self):
        coords = self._derive_from_machine()
        self._move_to_start_pos(coords)

    def _derive_from_machine(self):
        mx1, my1, mx2, my2 = self.canvas.coords(self.tag_shape_machine)
        initial_x1 = mx2 - (mx2 - mx1) * 0.7
        initial_y1 = my2 - (my1 - my2) * -0.6
        initial_x2 = mx2 - (mx2 - mx1) * 0.2
        initial_y2 = my2 - (my1 - my2) * -0.1
        self.canvas.create_rectangle(initial_x1, initial_y1,
          initial_x2,
          initial_y2,
          fill=BACKGROUND_CANVAS,
          width=(THICKNESS_LINE_AGENT * self.scale),
          outline=AGENT_OUTLINE_COLOUR,
          tags=(self.tag_shape),
          state='hidden')
        return (initial_x1, initial_y1, initial_x2, initial_y2)

    def _move_to_start_pos(self, coords):
        _, _, cx2, _ = self.canvas.coords(self.tag_shape_client)
        self.distance = coords[0] - cx2
        width_agent = coords[2] - coords[0]
        start_pos_x1 = cx2
        pos_y1 = coords[1]
        pos_y2 = coords[3]
        self.canvas.coords(self.tag_shape, start_pos_x1, pos_y1, start_pos_x1 + width_agent, pos_y2)

    def show(self):
        self.canvas.itemconfig((self.tag_shape), state='normal')

    def move(self):
        """____________."""

        def _animate():
            if not self.terminate:
                self.canvas.move(self.tag_shape, 10 * self.scale, 0)
                self.index += 10 * self.scale
                if self.index >= self.distance:
                    self._add_label()
                    self.terminate = True
                self.canvas.after(15, _animate)

        self.canvas.itemconfig((self.tag_shape), dash=(5, 5), width=1)
        _animate()

    def transfer_ok(self):
        """________."""
        self.canvas.itemconfig((self.tag_shape), width=(THICKNESS_LINE_AGENT * self.scale),
          outline='white',
          dash=(1, 1))

    def transfer_nok(self):
        """________."""
        self.canvas.itemconfig((self.tag_shape), width=(THICKNESS_LINE_AGENT * self.scale),
          outline='red',
          dash=(5, 5))


class TunnelShape(Shape):
    __doc__ = '______________.'

    def __init__(self, main_window, from_, to):
        Shape.__init__(self, main_window)
        self.type = 'tunnel'
        self.pos_from_ = from_.tag_shape
        self.pos_to = to.tag_shape
        self.terminate = False
        self.index = 0
        self.line1 = None
        self.line2 = None
        self.tag_shape = self._generate_tag
        self.tag_label = self._generate_tag

    def render(self):
        self.line1 = self.canvas.create_line(0, 0, 0, 0, fill=TUNNEL_OUTLINE_COLOUR, width=(THICKNESS_LINE_TUNNEL * self.scale),
          tags=(self.tag_shape))
        self.line2 = self.canvas.create_line(0, 0, 0, 0, fill=TUNNEL_OUTLINE_COLOUR, width=(THICKNESS_LINE_TUNNEL * self.scale),
          tags=(self.tag_shape))

    def show(self):
        distance, height, start_pos_x, pos_y = self._get_tunnel_metrics(self.pos_from_, self.pos_to)

        def animate():
            if not self.terminate:
                self.canvas.coords(self.line1, start_pos_x, pos_y - height, start_pos_x + self.index, pos_y - height)
                self.canvas.coords(self.line2, start_pos_x, pos_y + height, start_pos_x + self.index, pos_y + height)
                self.index += 10
                self.canvas.after(15, animate)
                if self.index > distance:
                    self._add_label()
                    self.terminate = True

        animate()


class AnimateConnection(Animation):
    __doc__ = '______________.'

    def __init__(self, main_window, from_, to):
        super().__init__(main_window)
        self.tag_packet = self._generate_tag
        self.tag_status = self._generate_tag
        self.tag_frame = self._generate_tag
        self.pos_from_ = from_.tag_shape
        self.pos_to = to.tag_shape
        self.terminate = False
        self.index = 0

    def start(self):
        distance, height, start_pos_x1, pos_y = self._get_tunnel_metrics((self.pos_from_), (self.pos_to), factor=0.04)
        packet_width = 20 * self.scale
        self.canvas.create_rectangle(start_pos_x1, (pos_y - height),
          (start_pos_x1 + packet_width),
          (pos_y + height),
          fill=PACKET_FILL_COLOUR,
          outline=PACKET_OUTLINE_COLOUR,
          width=2,
          tags=(self.tag_packet))

        def _animate_forward():
            if not self.terminate:
                self.canvas.move(self.tag_packet, 10 * self.scale, 0)
                self.index += 10 * self.scale
                if self.index >= distance - packet_width:
                    self.canvas.move(self.tag_packet, (distance - packet_width) * -1, 0)
                    self.index = 0
                self.canvas.after(25, _animate_forward)

        _animate_forward()
        self._show_banner_connection_ok()

    def _show_banner_connection_ok(self):
        width = self.status.winfo_width()
        pos_x = width / 2
        status_height = self.status.winfo_height()
        pos_y = status_height / 2
        self.status.create_text(pos_x, pos_y,
          text='CONNECTION ESTABLISHED',
          font=('', 20, 'normal'),
          fill=BANNER_TUNNEL_SUCCESS,
          tags=(self.tag_status))
        ax1, ay1, ax2, ay2 = self.status.bbox(self.tag_status)
        ax1 -= 25 * self.scale
        ax2 += 25 * self.scale
        self.status.create_rectangle(ax1, ay1, ax2, ay2, outline=BANNER_TUNNEL_SUCCESS, width=THICKNESS_PACKET, tags=(self.tag_frame))

    def stop(self):
        self.terminate = True
        self.canvas.delete(self.tag_packet)
        self.status.delete(self.tag_status)
        self.status.delete(self.tag_frame)

    def broken(self):
        """___________."""
        self.canvas.itemconfig((self.tag_packet), state='hidden')
        self.status.itemconfig((self.tag_status), text='CONNECTION BROKEN', fill=BANNER_TUNNEL_FAILURE)
        self.status.itemconfig((self.tag_frame), outline=BANNER_TUNNEL_FAILURE)

    def restored(self):
        """___________."""
        self.canvas.itemconfig((self.tag_packet), state='normal')
        self.status.itemconfig((self.tag_status), text='CONNECTION RESTORED', fill=BANNER_TUNNEL_SUCCESS)
        self.status.itemconfig((self.tag_frame), outline=BANNER_TUNNEL_SUCCESS)