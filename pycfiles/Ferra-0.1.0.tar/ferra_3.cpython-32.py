# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Python32\lib\site-packages\Ferra\ferra_3.py
# Compiled at: 2012-10-03 10:24:09
import Ferra
window = Ferra.Window(width=900, height=200, caption='Rotating Sprites')
spritebatch = Ferra.Batch()
sprites = []
for i in range(5):
    i = i + 1
    bubbleimage = Ferra.resource.load_image('bubble%d.png' % i)
    sprite = Ferra.sprite.RotatingSprite(img=bubbleimage, x=i * 150, y=100, rotate_speed=180.0, batch=spritebatch)
    sprites.append(sprite)

@window.event
def on_draw():
    window.clear()
    spritebatch.draw()


def update(dt):
    for sprite in sprites:
        sprite.update(dt)


Ferra.schedule_interval(update, 0.016666666666666666)
Ferra.run()