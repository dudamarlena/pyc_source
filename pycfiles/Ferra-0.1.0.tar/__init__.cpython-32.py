# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Python32\lib\site-packages\Ferra\__init__.py
# Compiled at: 2012-10-03 11:22:38
import pyglet
from pyglet import media
from pyglet import image
from .errors import *
from . import sprite
from . import resource
from . import gl
from pyglet.window import key
from pyglet.window import mouse
__all__ = ['Window',
 'sprite',
 'resource',
 'KeyHandler',
 'schedule',
 'schedule_interval',
 'Batch',
 'run',
 'gl']

class Window(pyglet.window.Window):
    """ This updated Window class' clear method allows you to specify your own color e.g:
        #[OMMITTED: Creation of window]
        window.clear(1, 1, 1, 1) # white
        window.clear(1, 0, 1, 0) # pink
        window.clear() # for default black color
        you can use others.
    """

    def clear(self, *args):
        super(Window, self).clear()
        if args:
            try:
                pyglet.gl.glClearColor(*args)
            except:
                raise ClearException('Invalid color: %s' % args)


class KeyHandler(pyglet.window.key.KeyStateHandler):
    """ Simple key handler with the use:
        class MyKeyHandler(Ferra.KeyHandler):
            pass
        keys = MyKeyHandler()
        if keys[Ferra.keys.LEFT]:
            ......
    """
    pass


def schedule(func):
    """ clall func every frame """
    return pyglet.clock.schedule(func)


def schedule_interval(func, interval):
    """ call func at interval frames """
    return pyglet.clock.schedule_interval(func, interval)


def Batch(*args, **kwargs):
    """ return pyglet.graphics.Batch(*args, **kwargs) """
    return pyglet.graphics.Batch(*args, **kwargs)


def run():
    pyglet.app.run()