# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sah/bg/pubxml/src/pubxml/image.py
# Compiled at: 2019-11-16 12:28:39
# Size of source mod 2**32: 919 bytes
IMAGE_MODES = {'1':'1-bit pixels, black and white, stored with one pixel per byte', 
 'L':'8-bit pixels, black and white', 
 'P':'8-bit pixels, mapped to any other mode using a color palette', 
 'RGB':'3x8-bit pixels, true color', 
 'RGBA':'4x8-bit pixels, true color with transparency mask', 
 'CMYK':'4x8-bit pixels, color separation', 
 'YCbCr':'3x8-bit pixels, color video format', 
 'LAB':'3x8-bit pixels, the L*a*b color space', 
 'HSV':'3x8-bit pixels, Hue, Saturation, Value color space', 
 'I':'32-bit signed integer pixels', 
 'F':'32-bit floating point pixels', 
 'LA':'(8-bit pixels, black and white with alpha', 
 'RGBX':'true color with padding)', 
 'RGBa':'true color with premultiplied alpha'}