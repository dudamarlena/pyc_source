# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\dev\cocos2020\test\test_platformer.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 4567 bytes
from __future__ import division, print_function, unicode_literals
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
testinfo = 't 0.1, s, q'
tags = 'tilemap, collide_map, collider'
import pyglet
from pyglet.window import key
pyglet.resource.path.append(pyglet.resource.get_script_home())
pyglet.resource.reindex()
import cocos
from cocos import tiles, actions, layer, mapcolliders

class PlatformerController(actions.Action):
    on_ground = True
    MOVE_SPEED = 300
    JUMP_SPEED = 800
    GRAVITY = -1200

    def start(self):
        self.target.velocity = (0, 0)

    def step(self, dt):
        if dt > 0.1:
            return
        vx, vy = self.target.velocity
        vx = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * self.MOVE_SPEED
        vy += self.GRAVITY * dt
        if self.on_ground:
            if keyboard[key.SPACE]:
                vy = self.JUMP_SPEED
        dx = vx * dt
        dy = vy * dt
        last = self.target.get_rect()
        new = last.copy()
        new.x += dx
        new.y += dy
        self.target.velocity = self.target.collision_handler(last, new, vx, vy)
        self.on_ground = new.y == last.y
        self.target.position = new.center
        (scroller.set_focus)(*new.center)


description = '\nShows how to use a mapcollider to control collision between actors and\nthe terrain as described by a tilemap.\nUse Left-Right arrows and space to control.\nUse D to show cell / tile info\n'

def main():
    global keyboard
    global scroller
    import cocos.director as director
    director.init(width=800, height=600, autoscale=False)
    print(description)
    player_layer = layer.ScrollableLayer()
    player = cocos.sprite.Sprite('witch-standing.png')
    player_layer.add(player)
    player.do(PlatformerController())
    scroller = layer.ScrollingManager()
    fullmap = tiles.load('platformer-map.xml')
    tilemap_walls = fullmap['walls']
    scroller.add(tilemap_walls, z=0)
    tilemap_decoration = fullmap['decoration']
    scroller.add(tilemap_decoration, z=1)
    scroller.add(player_layer, z=2)
    start = tilemap_decoration.find_cells(player_start=True)[0]
    r = player.get_rect()
    r.midbottom = start.midbottom
    player.position = r.center
    mapcollider = mapcolliders.RectMapCollider(velocity_on_bump='slide')
    player.collision_handler = mapcolliders.make_collision_handler(mapcollider, tilemap_walls)
    platformer_scene = cocos.scene.Scene()
    platformer_scene.add((layer.ColorLayer(100, 120, 150, 255)), z=0)
    platformer_scene.add(scroller, z=1)
    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)

    def on_key_press(key, modifier):
        if key == pyglet.window.key.D:
            tilemap_walls.set_debug(True)

    director.window.push_handlers(on_key_press)
    director.run(platformer_scene)


if __name__ == '__main__':
    main()