# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/wyliozero/wlcd.py
# Compiled at: 2019-11-24 09:28:29
# Size of source mod 2**32: 493 bytes
import Adafruit_CharLCD as LCD
lcd_rs = 12
lcd_en = 25
lcd_d4 = 6
lcd_d5 = 26
lcd_d6 = 24
lcd_d7 = 16
lcd_columns = 16
lcd_rows = 2
single = None

def lcd():
    global single
    if single == None:
        single = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
    else:
        return single