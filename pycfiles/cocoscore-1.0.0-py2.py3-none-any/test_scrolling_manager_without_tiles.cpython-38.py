# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_scrolling_manager_without_tiles.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 12896 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, t 1.1, s, t 2.1, s, t 3.1, s, t 4.1, s, t 5.1, s, t 6.1, s, q'
tags = 'scrolling, ScrollingManager, sutoscale'
autotest = 0
import math, pyglet
from pyglet.window import key
from pyglet.gl import *
pyglet.resource.path.append(pyglet.resource.get_script_home())
pyglet.resource.reindex()
import cocos
from cocos import tiles, actions, layer
import cocos.director as director
import cocos.euclid as eu
from cocos.actions import Delay, CallFunc, ScaleTo
view_width = 640
view_height = 480
world_width = 1392
world_height = 1000

class ProbeQuad(cocos.cocosnode.CocosNode):

    def __init__(self, r, color4):
        super(ProbeQuad, self).__init__()
        self.color4 = color4
        self.vertexes = [(r, 0, 0), (0, r, 0), (-r, 0, 0), (0, -r, 0)]

    def draw(self):
        glPushMatrix()
        self.transform()
        glBegin(GL_QUADS)
        glColor4ub(*self.color4)
        for v in self.vertexes:
            glVertex3i(*v)

        glEnd()
        glPopMatrix()


class SquareLand(cocos.layer.ScrollableLayer):
    is_event_handler = True

    def __init__(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height
        super(SquareLand, self).__init__()
        self.px_width = world_width
        self.px_height = world_height
        bg = cocos.layer.ColorLayer(170, 170, 0, 255, width=world_width, height=world_height)
        self.add(bg, z=0)
        margin = int(world_width * 0.01)
        self.margin = margin
        bg = cocos.layer.ColorLayer(0, 170, 170, 255, width=(world_width - 2 * margin), height=(world_height - 2 * margin))
        bg.position = (margin, margin)
        self.add(bg, z=1)
        mod = (world_width - 2.0 * margin) / 10.0
        y = margin + mod
        self.marks_positions = []
        while y < world_height - mod:
            x = margin + mod
            if x < world_width - mod:
                red = 55 + int(200.0 * x / world_width)
                blue = 55 + int(200.0 * y / world_height)
                actor = cocos.layer.ColorLayer(red, 0, blue, 255, width=(2 * int(mod)),
                  height=(2 * int(mod)))
                actor.position = (x, y)
                self.marks_positions.append((x, y))
                self.add(actor, z=3)
                x += 3 * mod
            else:
                y += 3 * mod

        self.marks_positions = self.marks_positions[:3]
        self.player = cocos.sprite.Sprite('grossinis_sister1.png')
        self.player.scale = 0.4
        self.player.model_width = self.player.width
        self.player.model_height = self.player.height
        self.player.position = (
         mod / 2 + margin, mod / 2 + margin)
        self.player.fastness = 200
        self.add((self.player), z=4)
        self.bindings = {key.LEFT: 'left', 
         key.RIGHT: 'right', 
         key.UP: 'up', 
         key.DOWN: 'down', 
         key.PLUS: 'zoomin', 
         key.MINUS: 'zoomout'}
        self.buttons = {'left':0, 
         'right':0, 
         'up':0, 
         'down':0, 
         'zoomin':0, 
         'zoomout':0}
        self.schedule(self.step)

    def on_enter(self):
        super(SquareLand, self).on_enter()
        self.scroller = self.get_ancestor(cocos.layer.ScrollingManager)
        self.scene = self.get_ancestor(cocos.scene.Scene)
        self.scene.f_refresh_marks = self.refresh_marks

    def on_key_press(self, k, m):
        binds = self.bindings
        if k in binds:
            self.buttons[binds[k]] = 1
            return True
        return False

    def on_key_release(self, k, m):
        binds = self.bindings
        if k in binds:
            self.buttons[binds[k]] = 0
            return True
        return False

    def on_mouse_press(self, x, y, button, modifiers):
        print('on_mouse_press:')
        vx, vy = self.scroller.screen_to_world(x, y)
        print('\tscreen_to_world(x, y):', vx, vy)

    def clamp(self, actor, new_pos):
        x, y = new_pos
        if x - actor.model_width // 2 < self.margin:
            x = self.margin + actor.model_width // 2
        elif x + actor.model_width // 2 > self.world_width - self.margin:
            x = self.world_width - self.margin - actor.model_width // 2
        if y - actor.model_height // 2 < self.margin:
            y = self.margin + actor.model_height // 2
        elif y + actor.model_height // 2 > self.world_height - self.margin:
            y = self.world_height - self.margin - actor.model_height // 2
        return (x, y)

    def step(self, dt):
        buttons = self.buttons
        move_dir = eu.Vector2(buttons['right'] - buttons['left'], buttons['up'] - buttons['down'])
        changed = False
        if move_dir:
            new_pos = self.player.position + self.player.fastness * dt * move_dir.normalize()
            new_pos = self.clamp(self.player, new_pos)
            self.player.position = new_pos
            changed = True
        else:
            new_zoom = self.scroller.scale + (buttons['zoomin'] - buttons['zoomout']) * 0.2 * dt
            if new_zoom < 0.3:
                new_zoom = 0.3
            elif new_zoom > 2.0:
                new_zoom = 2.0
        if new_zoom != self.scroller.scale:
            self.scroller.scale = new_zoom
            changed = True
        if changed:
            self.update_after_change()

    def update_after_change(self):
        (self.scroller.set_focus)(*self.player.position)
        self.refresh_marks()

    def refresh_marks(self):
        for mark, position in zip(self.scene.marks, self.marks_positions):
            screen_pos = (self.scroller.world_to_screen)(*position)
            mark.position = screen_pos

    def teleport_player(self, x, y):
        """ only used by autotest """
        self.player.position = (
         x, y)
        self.update_after_change()


class TestScene(cocos.scene.Scene):

    def __init__(self):
        super(TestScene, self).__init__()
        self.marks = []
        for i in range(1, 4):
            mark = ProbeQuad(3, (0, 255 // i, 0, 255))
            mark.position = (-20, -20)
            self.marks.append(mark)
            self.add(mark, z=2)

    def on_enter(self):
        director.push_handlers(self.on_cocos_resize)
        super(TestScene, self).on_enter()

    def on_cocos_resize(self, usable_width, usable_height):
        self.f_refresh_marks()


def show_common_text():
    print("\ntests ScrollingManager and ScrollableLayer when the contents are not provided\nby a tilemap.\n\nYou can run the test in the two available modes:'autoscale' True/False\nLook at the start of main to choose the mode; the instructions and expected\nresults text will match the mode.\n\nuse arrows to move, +- in the main keyboard (not the keypad) for zoom,\nctrl-f to toggle fullscreen status.\n\nFor clarity set view_width, view_height to respect your desktop aspect\nratio; look near the script begin\n\n")


def show_mode_1_text():
    print("\nMode: autoscale == True\n\n1. scroll constraits works:\n    verify that moving the player you can make the view scroll to reveal all\n    of the world, and not more than that.\n\n2. resize maps the correct area and the scroll constraits work ok after a\nresize:\n    a. move the player to bottom left corner. Use ctrl-f to repeatedly switch\n    between windowed and fullscreen.\n    Both screens should show the same world area, only at different scale.\n\n    b. Repeat at the top-right corner.\n\n    c. when in fullscreen,  verify that moving the player you can make the\n    view scroll to reveal all of the world, and not more than that.\n\n3. zooming ( ScrollerManager scale) works:\n    zoom in or out using key '+' or '-', not so much that all the world shows\n    in a single screen, then repeat 1), 2)\n\n4. consistency screen to world coordinates conversion:\n    a. restart the script, mouse click the inner bottom left corner, do ctrl-f\n    click again over the inner bottom left corner, zoom a little, click again\n    over the the inner bottom left corner.\n    Now look at the console: the screen_to_world values must all be near a\n    common value.\n\n    b. restart the script, scroll to the top right corner, repeat a. replacing\n    'botton left' by 'top left'\n\n5. world to screen coordinate changes correctness:\n    restart the script; move a bit. Look at the lower left corners in the lower\n    row of squares; you should see a small square in the shades of green.\n    moving, zomming, resizing (ctrl-f) should not alter the relative position of\n    small green squeares with respect to the world.\n\n6. good behavior when world small that the view:\n    scale down (zoom out) to the max. When the world becomes smaller than the\n    view, it should nicely center in the screen.\n    Moving the player from left to right border should not produce 'jumps' on\n    the view.\n")


def show_mode_2_text():
    print("\nMode: not autoscale, that is 'autoscale' == False\n\n1. scroll constraits works:\n    verify that moving the player you can make the view scroll to reveal all\n    of the world, and not more than that.\n\n2. resize maps the correct area and the scroll constraits work ok after a\nresize:\n    a. move the player to bottom left corner. Use ctrl-f to repeatedly switch\n    between windowed and fullscreen.\n    Both screens should depict the world at the same scale, thus the bigger\n    view will more area in the world.\n    When going from big to small, the player must be visible n the small view.\n    When going small to big, the bg should show all showed in the small plus\n    some extra area.\n\n    b. Repeat at the top-right corner.\n\n    c. when in fullscreen,  verify that moving the player you can make the\n    view scroll to reveal all of the world, and not more than that.\n\n3. zooming ( ScrollerManager scale) works:\n    zoom in or out using key '+' or '-', not so much that all the world shows\n    in a single screen, then repeat 1), 2)\n\n4. consistency screen to world coordinates conversion:\n    a. restart the script, mouse click the inner bottom left corner, do ctrl-f\n    click again over the inner bottom left corner, zoom a litle, click again\n    over the the inner bottom left corner.\n    Now look at the console: the screen_to_world values must all be near a\n    common value.\n\n    b. restart the script, scroll to the top right corner, repeat a. replacing\n    'botton left' by 'top left'\n\n5. world to screen coordinate changes correctness:\n    restart the script; move a bit. Look at the lower left corners in the lower\n    row of squares; you should see a small square in the shades of green.\n    moving, zomming, resizing (ctrl-f) should not alter the relative position of\n    small green squeares with respect to the world.\n\n6. good behavior when world small that the view:\n    scale down (zoom out) to the max. When the world becomes smaller than the\n    view, it should nicely center in the screen.\n    Moving the player from left to right border should not produce 'jumps' on\n    the view.\n")


def main():
    show_common_text()
    autoscale = True
    if autoscale:
        show_mode_1_text()
    else:
        show_mode_2_text()
    director.init(view_width, view_height, autoscale=autoscale)
    scene = TestScene()
    world_layer = SquareLand(world_width, world_height)
    scroller = cocos.layer.ScrollingManager()
    if autotest:

        def resize_scroller():
            scroller.scale = 0.75

        w, h = world_width, world_height
        template_action = Delay(0.05) + CallFunc(world_layer.teleport_player, 0, 0) + Delay(1) + CallFunc(world_layer.teleport_player, w // 2, 0) + Delay(1) + CallFunc(world_layer.teleport_player, w // 2, h) + Delay(1) + CallFunc(world_layer.teleport_player, w, h) + Delay(1) + CallFunc(resize_scroller) + Delay(1) + CallFunc(director.window.set_size, 800, 600) + CallFunc(world_layer.update_after_change)
        world_layer.do(template_action)
    scroller.add(world_layer)
    scene.add(scroller)
    director.run(scene)


if __name__ == '__main__':
    main()