# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/samples/snow.py
# Compiled at: 2018-01-02 08:48:33
import WS2801_RPI as led
from random import randint
led.clear()
led.flush()
while True:
    n = randint(1, 128)
    h = randint(0, 255)
    led.set_led_colors_buffer_list_multi_call(n, [h, h, h])
    led.flush()