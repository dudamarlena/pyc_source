# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/samples/rainbow.py
# Compiled at: 2018-01-02 08:48:33
"""This is an example on how to use WS2801_RPI."""
import WS2801_RPI as Leds, time, logging, colorsys
logging.getLogger().setLevel(31)
velocity = 300
s = Leds.set_led_colors_buffer_list_multi_call
while True:
    for i in range(1440):
        red, green, blue = colorsys.hsv_to_rgb(i / 720.0, 1, 1)
        s([ i + 1 for i in range(128) ], [
         int(red * 255), int(green * 255), int(blue * 255)])
        Leds.flush()
        time.sleep(1.0 / velocity)