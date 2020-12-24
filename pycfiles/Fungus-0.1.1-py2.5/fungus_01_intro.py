# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fungus_01_intro.py
# Compiled at: 2009-02-09 13:55:54
"""An example for a fungus scene definition. """
from os import path
from pyglet.window import key
from fungus_scene import BaseScene
from fungus_core import __copyright__
o = 'floor1.png'
t = 'tile2.png'
g = 'tile3.png'
r = 'tile4.png'
level = [
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, t, o, o, r, r, r, o, o, t, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, t, o, o, o, o, o],
 [
  o, o, g, o, o, o, r, r, r, t, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, g, o, o, o, o, o, o],
 [
  o, o, o, o, o, g, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o],
 [
  o, o, o, o, o, o, r, r, r, o, o, o, o, o, o, o, o]]

class Scene(BaseScene):
    """A dummy scene - mostly just the Scene API."""

    def __init__(self, core, *args, **kwds):
        """Initialize the scene with a core object for basic functions."""
        super(Scene, self).__init__(core, *args, **kwds)
        self.actor = self.core.sprite('tank5.png', x=217, y=183)
        self.text_box = self.core.sprite('box2.png', y=-2)
        self.text = self.core.load_text('Just get us back to the bunker before sunset.', x=14, y=48)
        self.level = self.load_level(level)
        for y in self.level:
            for x in y:
                self.visible.append(x)

        self.visible.append(self.actor)
        self.overlay.append(self.text_box)
        self.overlay.append(self.text)

    def actor_update(self, x, y):
        """Update the actor position.
        
        To change the movement pattern, just use self.actor.update_func=new_fun
        """
        y -= 1
        if y <= -32:
            y = 511
        return (
         x, y)

    def load_level(self, level):
        """Load a level with image names and return it as level with image objects."""
        new_level = []
        for y in range(len(level)):
            new_level.append([])
            for x in range(len(level[y])):
                sprite = self.core.sprite(level[y][x], x=32 * x, y=32 * y)
                new_level[y].append(sprite)

        return new_level

    def update(self):
        """Update the stats of all scene objects. 

Don't blit them, though. That's done by the Game itself.

To show something, add it to the self.visible list. 
To add a collider, add it to the self.colliding list. 
To add an overlay sprite, add it to the self.overlay list. 
"""
        self.actor.update()
        for x in self.level:
            for y in x:
                y.y += 1
                if y.y >= 512:
                    y.y = -31

    def on_key_press(self, symbol, modifiers):
        """Forwarded keyboard input."""
        if symbol == key.ESCAPE:
            self.core.win.has_exit = True
        else:
            print modifiers, symbol
        self.core.keyboard_movement_key_press(self.actor, symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        """Forwarded keyboard input."""
        self.core.keyboard_movement_key_release(self.actor, symbol, modifiers)