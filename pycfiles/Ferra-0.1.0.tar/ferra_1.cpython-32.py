# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Python32\lib\site-packages\Ferra\ferra_1.py
# Compiled at: 2012-10-03 11:22:20
import Ferra, pyglet, random
window = Ferra.Window(caption='Ferra Test 1')
sprite = Ferra.sprite.StaticSprite('ast.png', x=window.width // 2, y=window.height // 2)

@window.event
def on_draw():
    r = random.randint(0, 2)
    g = random.randint(0, 2)
    b = random.randint(0, 1)
    a = random.randint(0, 2)
    window.clear(r, g, b, a)
    sprite.draw()


def update(dt):
    pass


Ferra.schedule_interval(update, 0.008333333333333333)
Ferra.run()