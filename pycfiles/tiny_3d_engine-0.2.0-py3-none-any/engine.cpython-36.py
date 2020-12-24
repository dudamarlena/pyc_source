# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/tiny_3d_engine/src/tiny_3d_engine/engine.py
# Compiled at: 2020-04-23 17:13:36
# Size of source mod 2**32: 10393 bytes
"""
3D interaction engine
---------------------

This module load a **Scene3D** object, 
pass to a **ViewField** object** 
(i.e the coordinates of the scene transformed with
respect to the user POV),
and dialog with e **Screen** Object.

"""
import numpy as np
from tiny_3d_engine.viewfield import ViewField
from tiny_3d_engine.screen import Screen
from tiny_3d_engine import Scene3D
from tiny_3d_engine.color import rgb_to_hex, hex_to_rgb, rgb_arr_to_hex_list, rgb_shade
__all__ = [
 'Engine3D']

class Engine3D:
    __doc__ = '3D engine.\n\n    :param scene: scene to be loaded.\n\n    :param root: Tk window to graft the engine\n\n    :param width: integer in pix the view width.\n\n    :param height: integer in pix the view height.\n\n    :param shading: str. the shading (flat|radial|linear|none)\n\n    :param background: str. the backgound color in Hex (#000000)\n\n    :param title: the title of the engine window\n\n    .. note:\n        The engine does not render at startup.\n        Use Engine3d.render() to get your image.\n\n        The engine is not starting user interaction at startup.\n        Use Engine3d.mainloop() to get the show running.\n    \n    '

    def __init__(self, scene=None, root=None, width=1000, height=700, shading='flat', background='#666699', title='Tiny 3D Engine'):
        """Startup class."""
        self.title = title
        self.shading = shading
        self.view = ViewField(width, height)
        self.screen = Screen(width,
          height,
          background,
          root=root,
          title=(self.title))
        self.back_color = hex_to_rgb(background)
        self.scene = None
        self.screen.can.bind('<B1-Motion>', self._Engine3D__drag)
        self.screen.can.bind('<Shift-B1-Motion>', self._Engine3D__shiftdrag)
        self.screen.can.bind('<ButtonRelease-1>', self._Engine3D__resetDrag)
        self.screen.can.bind_all('<Key>', self._Engine3D__keypress)
        self._Engine3D__dragprev = []
        if scene is not None:
            self.update(scene)

    def update(self, scene):
        """ Update the scene to show."""
        if scene.is_void():
            self.scene = None
            self.clear()
        else:
            self.scene = scene
            self.conn = scene.conn()
            self.tags = scene.tags()
            self.screen.update(scene.colors())
            shade = self._compute_shade()
            self.shaded_colors = rgb_arr_to_hex_list(rgb_shade(self.scene.color_arrays(), self.back_color, shade))
            self._reset_view()
            self.screen.add_tags_bindings(scene.parts())

    def rotate(self, axis, angle):
        """rotate model around axis"""
        if self.scene is not None:
            self.view.rotate(axis, angle)

    def translate(self, axis, angle):
        """rotate model around axis"""
        if self.scene is not None:
            self.view.translate(axis, angle)

    def render(self, motion=False):
        """Render the viewfield on screen."""
        if self.scene is not None:
            projxy = self.view.flatten(self.distance, self.scale)
            if motion:
                mask = self.mot_visible
            else:
                mask = self.stat_visible
            ordered_z_indices = np.flip(np.argsort(self.view.pts[(self.conn[(mask, 0)], 2)]))
            reordered_conn = self.conn[mask, :][ordered_z_indices]
            reordered_colors = self.shaded_colors[mask][ordered_z_indices]
            reordered_tags = self.tags[mask][ordered_z_indices]
            n_vertices = self.conn.shape[1]
            m_elements = ordered_z_indices.shape[0]
            poly_coords = np.take(projxy,
              (reordered_conn.ravel()),
              axis=0).reshape(m_elements, n_vertices, 2)
            for elmt, tag, color in zip(poly_coords.tolist(), reordered_tags.tolist(), reordered_colors.tolist()):
                self.screen.createShape(elmt, tag, color)

    def clear(self):
        """clear display"""
        self.screen.clear()

    def after(self, time, function):
        """call screen after() method, for animations"""
        self.screen.after(time, function)

    def mainloop(self):
        """call screen mainloop() method to stay interactive"""
        self.screen.mainloop()

    def dump(self, fname):
        """Dump the scene into a file."""
        if self.scene is not None:
            self.scene.dump(fname)
        else:
            raise ValueError('No scene to dump...')

    def _reset_view(self):
        if self.scene is not None:
            self.view.update(self.scene.points())
        else:
            self.scale = float(self.view.init_scale)
            self.distance = 64
            m_elements = self.conn.shape[0]
            self.mot_visible = np.full(m_elements, True)
            rotate_max = 2000
            if m_elements > rotate_max:
                p = rotate_max / m_elements
                self.mot_visible = np.random.choice(a=[
                 True, False],
                  size=m_elements,
                  p=[
                 p, 1 - p])
            self.stat_visible = np.full(m_elements, True)
            stat_max = 100000
            if m_elements > stat_max:
                p = stat_max / m_elements
                self.stat_visible = np.random.choice(a=[
                 True, False],
                  size=m_elements,
                  p=[
                 p, 1 - p])

    def _compute_shade(self):
        """ compute the shading of the scene"""
        light = np.array([1.0, 1.0, 1.0], dtype=(np.float32))
        norm = np.linalg.norm(light)
        light /= norm
        pts = self.scene.points()
        if self.conn.shape[1] < 3:
            print('No polygons, Switch to radial shading...')
            self.shading = 'radial'
        else:
            if self.shading == 'flat':
                vect1 = pts[self.conn[:, 1], :] - pts[self.conn[:, 0], :]
                vect2 = pts[self.conn[:, 2], :] - pts[self.conn[:, 1], :]
                normal = np.cross(vect1, vect2)
                norm = np.clip(np.linalg.norm(normal, axis=1), 1e-08, None)
                normal = normal / norm[:, np.newaxis]
                align = np.dot(normal, light)
            else:
                if self.shading == 'linear':
                    axis = np.dot(pts[self.conn[:, 0], :], light)
                    align = 2.0 * (axis - axis.min()) / (axis.max() - axis.min()) - 1.0
                else:
                    if self.shading == 'radial':
                        radial = np.linalg.norm((pts[self.conn[:, 0], :] - light), axis=1)
                        align = 2.0 * (radial - radial.min()) / (radial.max() - radial.min()) - 1.0
                    else:
                        if self.shading == 'none':
                            align = np.zeros(self.conn.shape[0])
                        else:
                            if self.shading == 'gouraud':
                                raise NotImplementedError('As if I could implement gouraud shading from Tkinter!')
                            else:
                                raise RuntimeError('Shading ' + str(self.shading) + ' not implemented')
        align *= 0.8
        return align

    def __drag(self, event):
        """handler for mouse drag event"""
        if self._Engine3D__dragprev:
            if self.screen.motion_allowed:
                self.rotate('y', -(event.x - self._Engine3D__dragprev[0]) / 3)
                self.rotate('x', -(event.y - self._Engine3D__dragprev[1]) / 3)
                self.clear()
                self.render(motion=True)
        self._Engine3D__dragprev = [
         event.x, event.y]

    def __shiftdrag(self, event):
        """handler for mouse drag event"""
        if self._Engine3D__dragprev:
            if self.screen.motion_allowed:
                self.translate('x', -(event.x - self._Engine3D__dragprev[0]) / 350)
                self.translate('y', -(event.y - self._Engine3D__dragprev[1]) / 350)
                self.clear()
                self.render(motion=True)
        self._Engine3D__dragprev = [
         event.x, event.y]

    def __resetDrag(self, event):
        """reset mouse drag handler"""
        self._Engine3D__dragprev = []
        self.render()

    def __hide_by_tag(self, hide_family=False):
        """reset mouse drag handler"""
        tag = self.screen.current_tag
        if tag is not None:
            if hide_family:
                root = tag.split('.')[0]
                print('Hiding family', root)
                tohide = np.invert(np.char.startswith(self.tags, root))
            else:
                print('Hiding part ', tag)
                tohide = np.invert(np.char.equal(self.tags, tag))
            self.stat_visible = np.logical_and(self.stat_visible, tohide)
            self.mot_visible = np.logical_and(self.mot_visible, tohide)
            self.screen.motion_allowed = True
            self.screen.current_tag = None
            self.screen.can.delete('info')
            self.render()

    def __keypress(self, event):
        """handler for keyboard events"""
        if event.keysym == 'Z':
            self.scale *= 1.2
        else:
            if event.keysym == 'z':
                if self.scale > 20:
                    self.scale /= 1.2
            else:
                if event.keysym == 'd':
                    if self.distance < 128:
                        self.distance *= 2
                else:
                    if event.keysym == 'D':
                        if self.distance > 2:
                            self.distance /= 2
                    else:
                        if event.keysym == 'r':
                            self._reset_view()
                        else:
                            if event.keysym == 'w':
                                self.rotate('y', 90)
                            else:
                                if event.keysym == 'W':
                                    self.rotate('y', -90)
                                else:
                                    if event.keysym == 'x':
                                        self.rotate('x', 90)
                                    else:
                                        if event.keysym == 'X':
                                            self.rotate('x', -90)
                                        else:
                                            if event.keysym == 'c':
                                                self.rotate('z', 90)
                                            else:
                                                if event.keysym == 'C':
                                                    self.rotate('z', -90)
                                                else:
                                                    if event.keysym == 'h':
                                                        self._Engine3D__hide_by_tag()
                                                    else:
                                                        if event.keysym == 'H':
                                                            self._Engine3D__hide_by_tag(hide_family=True)
        self.clear()
        self.render()