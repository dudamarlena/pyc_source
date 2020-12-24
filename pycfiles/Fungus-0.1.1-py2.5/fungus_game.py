# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fungus_game.py
# Compiled at: 2009-02-26 08:40:30
"""Fungus - Live and survive in a world filled with mold.

The main script for starting Fungus games. 

Usage: 
    - python fungus_game.py
      start the default Scene. 
    - python fungus_game.py gamefile.Scene
      start with a custom Scene

Examples: 
    - python fungus_game.py fungus_01_intro.Scene
      Start the fungus Intro

For developers: 
    - Just clone the fungus project from the Mercurial repository and add your scenes inside it. 
      Distribute them along with the fungus engine. 

Mercurial repository: 
    - http://freehg.org/u/ArneBab/fungus/

To adjust the default scene, just import another one as Scene in fungus_game.py
"""
from time import sleep
from pyglet import window
from pyglet.gl import *
from fungus_core import Core
from fungus_scene import DummyScene as Scene

class Game(object):
    """The main game class. 

Basics: 
- The Game class acts as basic game layer and provides an API which the scenes can use. 
- It starts the scenes and passes them a core object. 
- It also contains the main event loop in which it calls the update function of 
the scenes. 
- Additionally it forwards events to the scene. 

    """

    def __init__(self, name='Fungus', width=480, height=360, fullscreen=False, graphics_dir='graphics', first_scene=Scene, *args, **kwds):
        """Initialize the game.
        
        @param first_scene: The Scene the game starts with. 
        @type first_scene: BaseScene
        """
        if not fullscreen:
            self.win = window.Window(width=width, height=height, fullscreen=fullscreen, caption=name)
        else:
            self.win = window.Window(fullscreen=fullscreen, resizable=False, caption=name)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.core = Core(graphics_dir=graphics_dir)
        self.core.win = self.win
        self.scene = first_scene(self.core)

    def event_loop(self):
        """Start the main event loop."""
        while not self.win.has_exit:
            self.win.dispatch_events()
            sleep(0.001)
            self.win.clear()
            self.update()
            self.win.flip()

    def update(self):
        """Update the screen. 

This means first updating the state of everything and then blitting it on the 
screen.

Also do scene switching, when the scene calls for it. 
        """
        try:
            self.scene.update()
            for i in self.scene.visible:
                i.blit()

            for i in self.scene.overlay:
                i.blit()

        except:
            pass

        if self.scene.switch_to_scene:
            self.scene = self.scene.switch_to_scene

    def on_key_press(self, symbol, modifiers):
        """Forward all key events to the scene, if the scene takes them. 

        Ideas: 
            - catch some key events directly as game controls (right, left, up, down, fire, ...), so we can define a keyboard layout at the game level and have every scene take that automatically. 
        """
        try:
            self.scene.on_key_press(symbol, modifiers)
        except:
            pass


def _help():
    return ('\n').join(__doc__.splitlines()[2:])


if __name__ == '__main__':
    from sys import argv
    if '--help' in argv or '-h' in argv:
        print _help()
        exit()
    if '--fullscreen' in argv:
        argv.remove('--fullscreen')
        game = Game(fullscreen=True)
    else:
        game = Game()
    if len(argv) > 1:
        mod = eval("__import__('" + argv[1].split('.')[0] + "')")
        game.scene = mod.__dict__[argv[1].split('.')[1]](game.core)

    @game.win.event
    def on_key_press(symbol, modifiers):
        game.on_key_press(symbol, modifiers)


    @game.win.event
    def on_key_release(symbol, modifiers):
        game.scene.on_key_release(symbol, modifiers)


    @game.win.event
    def on_mouse_press(x, y, buttons, modifiers):
        game.scene.on_mouse_press(x, y, buttons, modifiers)


    @game.win.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        game.scene.on_mouse_drag(x, y, dx, dy, buttons, modifiers)


    @game.win.event
    def on_mouse_release(x, y, buttons, modifiers):
        game.scene.on_mouse_release(x, y, buttons, modifiers)


    game.event_loop()