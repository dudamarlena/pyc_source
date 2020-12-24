# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/samples/rainbow_banner.py
# Compiled at: 2018-01-02 08:48:33
"""This is an example on how to use WS2801_RPI."""
import WS2801_RPI as Leds, time, logging, colorsys
granularity = 180.0
logging.getLogger().setLevel(31)
velocity = 300
Leds.set_gamma(3)
s = Leds.set_led_colors_buffer_list_multi_call
i = 0
while True:
    i = (i + 1) % int(granularity)
    rgb = Leds.get_led_colors_buffer_list()
    red, green, blue = colorsys.hsv_to_rgb(i / granularity, 1, 1)
    rgb.insert(0, [int(red * 255), int(green * 255), int(blue * 255)])
    rgb.pop()
    s([ j + 1 for j in range(128) ], rgb)
    Leds.flush()
    time.sleep(1.0 / velocity)