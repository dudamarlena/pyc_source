# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\components\spiral.py
# Compiled at: 2019-10-06 18:48:06
# Size of source mod 2**32: 18140 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np, gdspy
import picwriter.toolkit as tk
from picwriter.components.waveguide import Waveguide
from picwriter.components.sbend import SBend

class Spiral(tk.Component):
    __doc__ = " Spiral Waveguide Cell class.  The desired length of the spiral is first set, along with the spacing between input and output (the 'width' paramter).  Then, the corresponding height of the spiral is automatically set.\n\n        Args:\n           * **wgt** (WaveguideTemplate):  WaveguideTemplate object\n           * **width** (float): width of the spiral (i.e. distance between input/output ports)\n           * **length** (float): desired length of the waveguide\n\n        Keyword Args:\n           * **spacing** (float): distance between parallel waveguides\n           * **parity** (int): If 1 spiral on right side, if -1 spiral on left side (mirror flip)\n           * **port** (tuple): Cartesian coordinate of the input port\n           * **direction** (string): Direction that the component will point *towards*, can be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians)\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['output'] = {'port': (x2, y2), 'direction': 'dir2'}\n\n        Where in the above (x1,y1) are the first elements of the spiral trace, (x2, y2) are the last elements of the spiral trace, and 'dir1', 'dir2' are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n\n    "

    def __init__(self, wgt, width, length, spacing=None, parity=1, port=(0, 0), direction='NORTH'):
        tk.Component.__init__(self, 'Spiral', locals())
        self.portlist = {}
        self.width = width
        self.length = length
        self.parity = parity
        self.port = port
        self.spacing = 3 * wgt.clad_width if spacing == None else spacing
        self.wgt = wgt
        if self.wgt.euler == True:
            self.bend_radius = wgt.effective_bend_radius
            self.corner_dl = 2 * wgt.effective_bend_radius - wgt.bend_length_90
        else:
            self.bend_radius = wgt.bend_radius
            self.corner_dl = 2 * wgt.bend_radius - 0.5 * np.pi * wgt.bend_radius
        self.direction = direction
        if width < self.spacing + 5 * self.bend_radius:
            print('width = ' + str(width))
            print('spacing = ' + str(self.spacing))
            print('bend_radius = ' + str(self.bend_radius))
            raise ValueError("Warning!  Given the WaveguideTemplate 'bend radius' and 'spacing' specified, no spiral can be fit within the requested 'width'.  Please increase the 'width'.")
        self.nmax = int((self.width - self.spacing - 5 * self.bend_radius) / (2 * self.spacing))
        self._Spiral__build_cell()
        self._Spiral__build_ports()
        self._auto_transform_()

    def __fixed_len(self, h):
        w = self.width
        s = self.spacing
        br = self.bend_radius
        wcent = (w - s - br) / 2.0
        return 2 * wcent + (h - s) + wcent + br + h + (w - br) + (h - s) + wcent

    def __spiral_len(self, h, n):
        if n == 0:
            return 0
        w = self.width
        s = self.spacing
        br = self.bend_radius
        wcent = (w - s - br) / 2.0
        return 2 * (2 * (wcent - n * s) + (h - s - 2 * n * s))

    def __middle_len(self, h, n):
        return h - 2 * self.spacing - 2 * n * self.spacing

    def get_length(self, h, n):
        num_points = 10 + 4 * n
        length = self._Spiral__fixed_len(h)
        length += sum([self._Spiral__spiral_len(h, i + 1) for i in range(n)])
        length += self._Spiral__middle_len(h, n)
        length -= (num_points - 2) * self.corner_dl
        return length

    def __get_hmin(self, n):
        br = self.bend_radius
        s = self.spacing
        return 2 * br + 2 * s + 2 * n * s

    def get_spiral_length(self):
        return self.actual_length

    def __get_number_of_spirals(self):
        length_goal = self.length
        n = 0
        hmin = self._Spiral__get_hmin(n)
        length_min = self.get_length(hmin, n)
        while length_min < length_goal and n < self.nmax:
            n += 1
            hmin = self._Spiral__get_hmin(n)
            length_min = self.get_length(hmin, n)

        if n == 0:
            if length_min > length_goal:
                return
            return n
        else:
            return n - 1

    def __get_spiral_height(self, n):
        num_wg_segments = 4 + 2 * n
        hmin = self._Spiral__get_hmin(n)
        delta_length = self.length - self.get_length(hmin, n)
        hnew = hmin + delta_length / num_wg_segments
        return hnew

    def __build_cell(self):
        skip_length_check = False
        n = self._Spiral__get_number_of_spirals()
        if n != None:
            h = self._Spiral__get_spiral_height(n)
            w = self.width
            length = self.length
            br = self.bend_radius
            s = self.spacing
            if abs(length - self.get_length(h, n)) > 1e-06:
                raise ValueError('Warning! The computed length and desired length are not equal!')
            wcent = (w - s - br) / 2.0
            p = self.parity
            x0, y0 = (0, 0)
            start_points = [
             (
              x0, y0),
             (
              x0 + 2 * wcent, y0),
             (
              x0 + 2 * wcent, y0 - p * (h - s))]
            end_points = [
             (
              x0, y0 - p * s),
             (
              x0, y0 - p * h),
             (
              x0 + w - br, y0 - p * h),
             (
              x0 + w - br, y0),
             (
              x0 + w, y0)]
            spiral_in_pts = []
            x_left_start, x_right_start = x0 + s, x0 + 2 * wcent - 2 * s
            y_top_start, y_bot_start = y0 - p * 2 * s, y0 - p * (h - s)
            for j in range(n):
                i = j + 1
                if i % 2 == 1:
                    left_segment_index = (i - 1) / 2
                    spiral_in_pts.append((
                     x_left_start + 2 * s * left_segment_index,
                     y_bot_start + p * (2 * s * left_segment_index)))
                    spiral_in_pts.append((
                     x_left_start + 2 * s * left_segment_index,
                     y_top_start - p * (2 * s * left_segment_index)))
                    if j + 1 == n:
                        spiral_in_pts.append((
                         x0 + wcent, y_top_start - p * (2 * s * left_segment_index)))
                    if i % 2 == 0:
                        right_segment_index = (i - 2) / 2
                        spiral_in_pts.append((
                         x_right_start - 2 * s * right_segment_index,
                         y_top_start - p * (2 * s * right_segment_index)))
                        spiral_in_pts.append((
                         x_right_start - 2 * s * right_segment_index,
                         y_bot_start + p * (2 * s * right_segment_index + 2 * s)))
                        if j + 1 == n:
                            spiral_in_pts.append((
                             x0 + wcent,
                             y_bot_start + p * (2 * s * right_segment_index + 2 * s)))

            if n == 0:
                spiral_in_pts.append((x0 + wcent, y_bot_start))
            spiral_out_pts = []
            x_left_start, x_right_start = x0 + 2 * s, x0 + 2 * wcent - s
            y_top_start, y_bot_start = y0 - p * s, y0 - p * (h - 2 * s)
            for j in range(n):
                i = j + 1
                if i % 2 == 1:
                    right_segment_index = (i - 1) / 2
                    spiral_out_pts.append((
                     x_right_start - 2 * s * right_segment_index,
                     y_top_start - p * 2 * s * right_segment_index))
                    spiral_out_pts.append((
                     x_right_start - 2 * s * right_segment_index,
                     y_bot_start + p * (2 * s * right_segment_index)))
                    if j + 1 == n:
                        spiral_out_pts.append((
                         x0 + wcent, y_bot_start + p * 2 * s * right_segment_index))
                    elif i % 2 == 0:
                        left_segment_index = (i - 2) / 2
                        spiral_out_pts.append((
                         x_left_start + 2 * s * left_segment_index,
                         y_bot_start + p * 2 * s * left_segment_index))
                        spiral_out_pts.append((
                         x_left_start + 2 * s * left_segment_index,
                         y_top_start - p * (2 * s * left_segment_index + 2 * s)))
                        if j + 1 == n:
                            spiral_out_pts.append((
                             x0 + wcent,
                             y_top_start - p * (2 * s * left_segment_index + 2 * s)))

            if n == 0:
                spiral_out_pts.append((x0 + wcent, y_top_start))
            spiral_out_pts.reverse()
            waypoints = start_points + spiral_in_pts + spiral_out_pts + end_points
        else:
            length = self.length
            w = self.width
            br = self.bend_radius
            dl = self.corner_dl
            if length < w + 4 * br - 4 * dl:
                from scipy.optimize import fsolve
                from scipy.special import ellipeinc
                func = lambda s_height: length - ellipeinc(2 * np.pi, 1 - 1 / (1 + s_height ** 2 * np.pi ** 2 / w ** 2)) / (2 * np.pi / w / np.sqrt(1 + s_height ** 2 * np.pi ** 2 / w ** 2))
                h_guess = np.sqrt((length / 2.0) ** 2 - (w / 2) ** 2)
                h_solution = fsolve(func, h_guess)
                h = -self.parity * h_solution[0]
                sbend1 = SBend((self.wgt), (w / 2.0), h, port=(0, 0), direction='EAST')
                self.add(sbend1)
                sbend2 = SBend((self.wgt),
                  (w / 2.0), (-h), port=(w / 2.0, h), direction='EAST')
                self.add(sbend2)
                self.actual_length = ellipeinc(2 * np.pi, 1 - 1 / (1 + h ** 2 * np.pi ** 2 / w ** 2)) / (2 * np.pi / w / np.sqrt(1 + h ** 2 * np.pi ** 2 / w ** 2))
                skip_length_check = True
            else:
                p = self.parity
                x0, y0 = (0, 0)
                extra_height = (length - (w + 4 * br - 4 * dl)) / 2.0
                max_turns = (w - 4 * br) // (4 * br)
                extra_length_per_turn = 8 * br - 4 * dl - 4 * br
                waypoints = [
                 (
                  x0, y0), (x0 + br, y0)]
                number_of_turns = extra_height // extra_length_per_turn
                if number_of_turns > max_turns:
                    number_of_turns = max_turns
                dh = (length - (w + 4 * br - 4 * dl) - number_of_turns * extra_length_per_turn) / (number_of_turns * 2 + 2)
                waypoints.append((x0 + br, y0 - p * (2 * br + dh)))
                for i in range(int(number_of_turns)):
                    waypoints.append((x0 + 3 * br + i * br * 4, y0 - p * (2 * br + dh)))
                    waypoints.append((x0 + 3 * br + i * br * 4, y0))
                    waypoints.append((x0 + 5 * br + i * br * 4, y0))
                    waypoints.append((x0 + 5 * br + i * br * 4, y0 - p * (2 * br + dh)))

                waypoints.append((x0 + w - br, y0 - p * (2 * br + dh)))
                waypoints.append((x0 + w - br, y0))
                waypoints.append((x0 + w, y0))
        if not skip_length_check:
            l = 0
            for i in range(len(waypoints) - 1):
                dx, dy = waypoints[(i + 1)][0] - waypoints[i][0], waypoints[(i + 1)][1] - waypoints[i][1]
                l += np.sqrt(dx ** 2 + dy ** 2)

            num_corners = len(waypoints) - 2
            l -= num_corners * self.corner_dl
            self.actual_length = l
            if abs(l - self.length) > 1e-06:
                print('Actual computed length = ' + str(l))
                print('Expected length = ' + str(self.length))
                raise ValueError('Warning! Spiral generated is significantly different from what is expected.')
            wg = Waveguide(waypoints, self.wgt)
            self.add(wg)
        self.portlist_input = (0, 0)
        self.portlist_output = (self.width, 0)

    def __build_ports(self):
        self.portlist['input'] = {'port':self.portlist_input, 
         'direction':'WEST'}
        self.portlist['output'] = {'port':self.portlist_output,  'direction':'EAST'}


if __name__ == '__main__':
    from picwriter.components.waveguide import WaveguideTemplate
    gdspy.current_library = gdspy.GdsLibrary()
    top = gdspy.Cell('top')
    wgt = WaveguideTemplate(bend_radius=50,
      wg_width=1.0,
      clad_width=10.0,
      euler_bend=True)
    sp1 = Spiral(wgt,
      width=2700.0,
      length=2900.0,
      spacing=20.0,
      parity=1,
      port=(0, 0),
      direction='EAST')
    tk.add(top, sp1)
    print('length is ' + str(sp1.get_spiral_length()))
    print('portlist = ' + str(sp1.portlist))
    gdspy.LayoutViewer(cells='top')