# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/tiny_3d_engine/src/tiny_3d_engine/engine.py
# Compiled at: 2020-02-25 17:37:31
# Size of source mod 2**32: 6283 bytes
"""
3D interaction engine
---------------------

This module load a **Scene3D** object, 
pass to a **ViewField** object** 
(i.e the coordinates of the scene transformed with
respect to the user POV),
and dialog with e **Screen** Object.

**Note that there is NO Graphical Toolkit here.
The Graphical part is totally imiter to the Screen Object**

"""
import time, numpy as np
from tiny_3d_engine.viewfield import ViewField
from tiny_3d_engine.screen import Screen
__all__ = [
 'Engine3D']

class Engine3D:

    def __init__(self, scene=None, root=None, width=1000, height=700, background='#666699', title='Tiny 3D Engine'):
        self.title = title
        self.view = ViewField(width, height)
        self.screen = Screen(width,
          height,
          background,
          root=root,
          title=(self.title))
        self.scene = None
        self.screen.can.bind('<B1-Motion>', self._Engine3D__drag)
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
            self.reset_view()
            self.screen.add_tags_bindings(scene.parts())

    def reset_view(self):
        self.view.update(self.scene.points())
        self.scale = float(self.view.init_scale)
        self.distance = 6 * self.view.size

    def rotate(self, axis, angle):
        """rotate model around axis"""
        if self.scene is not None:
            self.view.rotate(axis, angle)

    def translate(self, axis, angle):
        """rotate model around axis"""
        if self.scene is not None:
            self.view.translate(axis, angle)

    def dump(self, fname):
        """Dump the scene into a file."""
        if self.scene is not None:
            self.scene.dump(fname)
        else:
            raise ValueError('No scene to dump...')

    def render(self):
        """Render the viewfield on screen."""
        if self.scene is not None:
            projxy = self.view.flatten(self.distance, self.scale)
            ordered_z_indices = np.flip(np.argsort(self.view.pts[(self.conn[:, 0], 2)]))
            m_elements, n_vertices = self.conn.shape
            reordered_conn = self.conn[ordered_z_indices]
            poly_coords = np.take(projxy,
              (reordered_conn.ravel()),
              axis=0)
            poly_coords = poly_coords.reshape(m_elements, n_vertices, 2)
            for i, elmt in enumerate(poly_coords):
                tag = self.tags[ordered_z_indices[i]]
                self.screen.createShape(elmt.tolist(), tag, self.elmt_color(tag))

    def elmt_color(self, tag):
        """Redirects to part color

        colors shades should be computed
        with numpy in integers, not at drawing step"""
        return self.scene.part_color(tag)

    def clear(self):
        """clear display"""
        self.screen.clear()

    def after(self, time, function):
        """call screen after() method, for animations"""
        self.screen.after(time, function)

    def mainloop(self):
        """call screen mainloop() method to stay interactive"""
        self.screen.mainloop()

    def bench_speed(self, trials=10):
        """Benchmark on rendering speed"""
        print('Benchmark on speed')
        perf_list = list()
        for i in range(trials):
            start = time.time()
            self.rotate('y', 1.0)
            end = time.time()
            perf_list.append(end - start)

        perf = sum(perf_list) / len(perf_list)
        print('Rotate', str(round(1000 * perf, 3)) + ' ms')
        perf_list = list()
        for i in range(trials):
            start = time.time()
            self.clear()
            self.render()
            end = time.time()
            perf_list.append(end - start)

        perf = sum(perf_list) / len(perf_list)
        print('Render', str(round(1 / perf, 3)) + ' fps')

    def __drag(self, event):
        """handler for mouse drag event"""
        if self._Engine3D__dragprev:
            self.rotate('y', -(event.x - self._Engine3D__dragprev[0]) / 20)
            self.rotate('x', -(event.y - self._Engine3D__dragprev[1]) / 20)
            self.clear()
            self.render()
        self._Engine3D__dragprev = [
         event.x, event.y]

    def __resetDrag(self, event):
        """reset mouse drag handler"""
        self._Engine3D__dragprev = []

    def __keypress(self, event):
        """handler for keyboard events"""
        if event.keysym == 'Up':
            self.rotate('x', -0.5)
        else:
            if event.keysym == 'Down':
                self.rotate('x', 0.5)
            else:
                if event.keysym == 'Right':
                    self.rotate('y', -0.5)
                else:
                    if event.keysym == 'Left':
                        self.rotate('y', 0.5)
                    else:
                        if event.keysym == 'w':
                            self.translate('x', 0.1)
                        else:
                            if event.keysym == 'c':
                                self.translate('x', -0.1)
                            else:
                                if event.keysym == 's':
                                    self.translate('y', -0.1)
                                else:
                                    if event.keysym == 'x':
                                        self.translate('y', 0.1)
                                    else:
                                        if event.keysym == 'Z':
                                            self.scale *= 2
                                        else:
                                            if event.keysym == 'z':
                                                if self.scale > 20:
                                                    self.scale /= 2
                                            else:
                                                if event.keysym == 'r':
                                                    self.reset_view()
                                                self.clear()
                                                self.render()