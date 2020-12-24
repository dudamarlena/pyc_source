# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/scene/cameras/fly.py
# Compiled at: 2016-11-03 01:40:19
from __future__ import division
import math, numpy as np
from ...app import Timer
from ...util.quaternion import Quaternion
from ...util import keys
from .perspective import PerspectiveCamera

class FlyCamera(PerspectiveCamera):
    """ The fly camera provides a way to explore 3D data using an
    interaction style that resembles a flight simulator.

    For this camera, the ``scale_factor`` indicates the speed of the
    camera in units per second, and the ``center`` indicates the
    position of the camera.

    Parameters
    ----------
    fov : float
        Field of view. Default 60.0.
    rotation : float | None
        Rotation to use.
    **kwargs : dict
        Keyword arguments to pass to `BaseCamera`.

    Notes
    -----
    Interacting with this camera might need a bit of practice.
    The reaction to key presses can be customized by modifying the
    keymap property.

    Moving:

      * arrow keys, or WASD to move forward, backward, left and right
      * F and C keys move up and down
      * Space bar to brake

    Viewing:

      * Use the mouse while holding down LMB to control the pitch and yaw.
      * Alternatively, the pitch and yaw can be changed using the keys
        IKJL
      * The camera auto-rotates to make the bottom point down, manual
        rolling can be performed using Q and E.

    """
    _state_props = PerspectiveCamera._state_props + ('rotation', )

    def __init__(self, fov=60, rotation=None, **kwargs):
        self._speed = np.zeros((6, ), 'float64')
        self._distance = None
        self._brake = np.zeros((6, ), 'uint8')
        self._acc = np.zeros((6, ), 'float64')
        self._auto_roll = True
        self._rotation1 = Quaternion()
        self._rotation2 = Quaternion()
        PerspectiveCamera.__init__(self, fov=fov, **kwargs)
        self.rotation = rotation if rotation is not None else Quaternion()
        self._event_value = None
        self._update_from_mouse = False
        self._keymap = {keys.UP: (
                   +1, 1), 
           keys.DOWN: (-1, 1), keys.RIGHT: (
                      +1, 2), 
           keys.LEFT: (-1, 2), 'W': (
               +1, 1), 
           'S': (-1, 1), 'D': (
               +1, 2), 
           'A': (-1, 2), 'F': (
               +1, 3), 
           'C': (-1, 3), 'I': (
               +1, 4), 
           'K': (-1, 4), 'L': (
               +1, 5), 
           'J': (-1, 5), 'Q': (
               +1, 6), 
           'E': (-1, 6), keys.SPACE: (0, 1, 2, 3)}
        self._timer = Timer(0.01, start=False, connect=self.on_timer)
        return

    @property
    def rotation(self):
        """ Get the full rotation. This rotation is composed of the
        normal rotation plus the extra rotation due to the current
        interaction of the user.
        """
        rotation = self._rotation2 * self._rotation1
        return rotation.normalize()

    @rotation.setter
    def rotation(self, value):
        assert isinstance(value, Quaternion)
        self._rotation1 = value

    @property
    def auto_roll(self):
        """ Whether to rotate the camera automaticall to try and attempt
        to keep Z up.
        """
        return self._auto_roll

    @auto_roll.setter
    def auto_roll(self, value):
        self._auto_roll = bool(value)

    @property
    def keymap(self):
        """ A dictionary that maps keys to thruster directions

        The keys in this dictionary are vispy key descriptions (from
        vispy.keys) or characters that represent keys. These are matched
        to the "key" attribute of key-press and key-release events.

        The values are tuples, in which the first element specifies the
        magnitude of the acceleration, using negative values for
        "backward" thrust. A value of zero means to brake. The remaining
        elements specify the dimension to which the acceleration should
        be applied. These are 1, 2, 3 for forward/backward, left/right,
        up/down, and 4, 5, 6 for pitch, yaw, roll.
        """
        return self._keymap

    def _set_range(self, init):
        """ Reset the view.
        """
        self._speed *= 0.0
        w, h = self._viewbox.size
        w, h = float(w), float(h)
        x1, y1, z1 = self._xlim[0], self._ylim[0], self._zlim[0]
        x2, y2, z2 = self._xlim[1], self._ylim[1], self._zlim[1]
        rx, ry, rz = x2 - x1, y2 - y1, z2 - z1
        if w / h > 1:
            rx /= w / h
            ry /= w / h
        else:
            rz /= h / w
        self._scale_factor = max(rx, ry, rz) / 3.0
        margin = np.mean([rx, ry, rz]) * 0.1
        self._center = (x1 - margin, y1 - margin, z1 + margin)
        yaw = 45 * self._flip_factors[0]
        pitch = -90 - 20 * self._flip_factors[2]
        if self._flip_factors[1] < 0:
            yaw += 90 * np.sign(self._flip_factors[0])
        q1 = Quaternion.create_from_axis_angle(pitch * math.pi / 180, 1, 0, 0)
        q2 = Quaternion.create_from_axis_angle(0 * math.pi / 180, 0, 1, 0)
        q3 = Quaternion.create_from_axis_angle(yaw * math.pi / 180, 0, 0, 1)
        self._rotation1 = (q1 * q2 * q3).normalize()
        self._rotation2 = Quaternion()
        self.view_changed()

    def _get_directions(self):
        pf = (0, 0, -1)
        pr = (1, 0, 0)
        pl = (-1, 0, 0)
        pu = (0, 1, 0)
        rotation = self.rotation.inverse()
        pf = rotation.rotate_point(pf)
        pr = rotation.rotate_point(pr)
        pl = rotation.rotate_point(pl)
        pu = rotation.rotate_point(pu)

        def _normalize(p):
            L = sum(x ** 2 for x in p) ** 0.5
            return np.array(p, 'float64') / L

        pf = _normalize(pf)
        pr = _normalize(pr)
        pl = _normalize(pl)
        pu = _normalize(pu)
        return (
         pf, pr, pl, pu)

    def on_timer(self, event):
        """Timer event handler

        Parameters
        ----------
        event : instance of Event
            The event.
        """
        rel_speed = event.dt
        rel_acc = 0.1
        pf, pr, pl, pu = self._get_directions()
        self._speed += self._acc * rel_acc
        reduce = np.array([0.05, 0.05, 0.05, 0.1, 0.1, 0.1])
        reduce[self._brake > 0] = 0.2
        self._speed -= self._speed * reduce
        if np.abs(self._speed).max() < 0.05:
            self._speed *= 0.0
        if self._speed[:3].any():
            dv = np.array([ 1.0 / d for d in self._flip_factors ])
            vf = pf * dv * rel_speed * self._scale_factor
            vr = pr * dv * rel_speed * self._scale_factor
            vu = pu * dv * rel_speed * self._scale_factor
            direction = (vf, vr, vu)
            center_loc = np.array(self._center, dtype='float32')
            center_loc += self._speed[0] * direction[0] + self._speed[1] * direction[1] + self._speed[2] * direction[2]
            self._center = tuple(center_loc)
        roll_angle = 0
        if self._speed[3:].any():
            angleGain = np.array([1.0, 1.5, 1.0]) * 3 * math.pi / 180
            angles = self._speed[3:] * angleGain
            q1 = Quaternion.create_from_axis_angle(angles[0], -1, 0, 0)
            q2 = Quaternion.create_from_axis_angle(angles[1], 0, 1, 0)
            q3 = Quaternion.create_from_axis_angle(angles[2], 0, 0, -1)
            q = q1 * q2 * q3
            self._rotation1 = (q * self._rotation1).normalize()
        if self.auto_roll:
            up = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}[self.up[1]]
            up = np.array(up) * {'+': +1, '-': -1}[self.up[0]]

            def angle(p1, p2):
                return np.arccos(p1.dot(p2))

            ar = angle(pr, up)
            al = angle(pl, up)
            af = angle(pf, up)
            roll_angle = math.sin(0.5 * (al - ar))
            roll_angle *= abs(math.sin(af))
            if abs(roll_angle) < 0.05:
                roll_angle = 0
            if roll_angle:
                roll_angle = np.sign(roll_angle) * np.abs(roll_angle) ** 0.5
                angle_correction = 1.0 * roll_angle * math.pi / 180
                q = Quaternion.create_from_axis_angle(angle_correction, 0, 0, 1)
                self._rotation1 = (q * self._rotation1).normalize()
        if self._speed.any() or roll_angle or self._update_from_mouse:
            self._update_from_mouse = False
            self.view_changed()

    def viewbox_key_event(self, event):
        """ViewBox key event handler

        Parameters
        ----------
        event : instance of Event
            The event.
        """
        PerspectiveCamera.viewbox_key_event(self, event)
        if event.handled or not self.interactive:
            return
        if not self._timer.running:
            self._timer.start()
        if event.key in self._keymap:
            val_dims = self._keymap[event.key]
            val = val_dims[0]
            if val == 0:
                vec = self._brake
                val = 1
            else:
                vec = self._acc
            if event.type == 'key_release':
                val = 0
            for dim in val_dims[1:]:
                factor = 1.0
                vec[dim - 1] = val * factor

    def viewbox_mouse_event(self, event):
        """ViewBox mouse event handler

        Parameters
        ----------
        event : instance of Event
            The event.
        """
        PerspectiveCamera.viewbox_mouse_event(self, event)
        if event.handled or not self.interactive:
            return
        if event.type == 'mouse_wheel':
            if not event.mouse_event.modifiers:
                self._speed[0] += 0.5 * event.delta[1]
            else:
                if keys.SHIFT in event.mouse_event.modifiers:
                    s = 1.1 ** (-event.delta[1])
                    self.scale_factor /= s
                    print 'scale factor: %1.1f units/s' % self.scale_factor
                return
            if event.type == 'mouse_press':
                event.handled = True
            if event.type == 'mouse_release':
                self._event_value = None
                self._rotation1 = (self._rotation2 * self._rotation1).normalize()
                self._rotation2 = Quaternion()
            else:
                if not self._timer.running:
                    self._timer.start()
                if event.type == 'mouse_move':
                    if event.press_event is None:
                        return
                    return event.buttons or None
            modifiers = event.mouse_event.modifiers
            pos1 = event.mouse_event.press_event.pos
            pos2 = event.mouse_event.pos
            w, h = self._viewbox.size
            if 1 in event.buttons and not modifiers:
                d_az = -float(pos2[0] - pos1[0]) / w
                d_el = +float(pos2[1] - pos1[1]) / h
                d_az *= -0.5 * math.pi
                d_el *= +0.5 * math.pi
                q_az = Quaternion.create_from_axis_angle(d_az, 0, 1, 0)
                q_el = Quaternion.create_from_axis_angle(d_el, 1, 0, 0)
                self._rotation2 = (q_el.normalize() * q_az).normalize()
            elif 2 in event.buttons and keys.CONTROL in modifiers:
                if self._event_value is None:
                    self._event_value = self._fov
                p1 = np.array(event.press_event.pos)[:2]
                p2 = np.array(event.pos)[:2]
                p1c = event.map_to_canvas(p1)[:2]
                p2c = event.map_to_canvas(p2)[:2]
                d = p2c - p1c
                fov = self._event_value * math.exp(-0.01 * d[1])
                self._fov = min(90.0, max(10, fov))
        self._update_from_mouse = True
        return

    def _update_projection_transform(self, fx, fy):
        PerspectiveCamera._update_projection_transform(self, fx, fy)
        axis_angle = self.rotation.get_axis_angle()
        angle = axis_angle[0] * 180 / math.pi
        tr = self.transform
        tr.reset()
        tr.rotate(-angle, axis_angle[1:])
        tr.scale([ 1.0 / a for a in self._flip_factors ])
        tr.translate(self._center)