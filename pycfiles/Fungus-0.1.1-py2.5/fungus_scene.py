# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fungus_scene.py
# Compiled at: 2009-02-09 13:51:12
"""An example for a fungus scene definition. 

Ideas: 
- Keyboard control via a dict similar to the command dict in Mercurial: Keyboard symbols or combinations (as tuple) as keys and methods of the scene as values. Convenience functions which add a whole set of actor control keys. This allows for dynamic key rebinding. 

"""
from fungus_core import Sprite
from pyglet.window import key

class MethodNotImplemented(Exception):
    """A warning to display if any necessary scripting function isn't implemented."""

    def __init__(self, func, implementation=None):
        self.func = func
        self.implementation = implementation

    def __str__(self):
        if self.implementation is None:
            return 'The method ' + str(self.func) + ' must be implemented.'
        else:
            return 'The method ' + str(self.func) + ' must be implemented.' + '\nThe simplest way is to just add the following lines to your class:' + self.implementation
        return


class BaseScene(object):
    """A dummy scene - mostly just the Scene API."""

    def __init__(self, core):
        """Initialize the scene with a core object for basic functions."""
        self.core = core
        self.visible = []
        self.colliding = []
        self.overlay = []
        self.switch_to_scene = False

    def update(self):
        """Update the stats of all scene objects. """
        raise MethodNotImplemented(self.update, implementation='    def update(self): \n        pass')

    def on_key_press(self, symbol, modifiers):
        """Forwarded keyboard input."""
        if symbol == key.ESCAPE:
            self.core.win.has_exit = True

    def on_key_release(self, symbol, modifiers):
        """Forwarded keyboard input."""
        pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        """Forwarded keyboard input."""
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Forwarded keyboard input."""
        pass

    def on_mouse_release(self, x, y, buttons, modifiers):
        """Forwarded keyboard input."""
        pass


IMAGE_TANK = 'tank.png'

class DummyScene(BaseScene):
    """A dummy scene - mostly just the Scene API."""

    def __init__(self, core, *args, **kwds):
        """Initialize the scene with a core object for basic functions."""
        super(DummyScene, self).__init__(core, *args, **kwds)
        self.tank = self.core.sprite(IMAGE_TANK, x=212, y=208, update_func=self.tank_update)
        self.visible.append(self.tank)

    def tank_update(self, x, y):
        """Update the tank position."""
        y -= 1
        if y < -68:
            y = 544
        return (
         x, y)

    def update(self):
        """Update the stats of all scene objects. 

Don't blit them, though. That's done by the Game itself.

To show something, add it to the self.visible list. 
To add a collider, add it to the self.colliding list. 
To add an overlay sprite, add it to the self.overlay list. 
"""
        self.tank.update()