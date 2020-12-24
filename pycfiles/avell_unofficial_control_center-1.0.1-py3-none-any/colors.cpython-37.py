# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/home/rodgomesc/avell-unofficial-control-center/aucc/core/colors.py
# Compiled at: 2019-06-06 19:37:05
# Size of source mod 2**32: 771 bytes
_colors_available = {'red':[0, 255, 0, 0],  'green':[
  0, 0, 255, 0], 
 'blue':[
  0, 0, 0, 255], 
 'teal':[
  0, 0, 255, 255], 
 'purple':[
  0, 255, 0, 255], 
 'pink':[
  0, 255, 0, 119], 
 'yellow':[
  0, 255, 119, 0], 
 'white':[
  0, 255, 255, 255], 
 'orange':[
  0, 255, 28, 0]}

def get_mono_color_vector(color_name):
    return bytearray(16 * _colors_available[color_name])


def get_h_alt_color_vector(color_name_a, color_name_b):
    return bytearray(8 * (_colors_available[color_name_a] + _colors_available[color_name_b]))


def get_v_alt_color_vector(color_name_a, color_name_b):
    return bytearray(8 * _colors_available[color_name_a] + 8 * _colors_available[color_name_b])