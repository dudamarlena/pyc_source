# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\myconfig.py
# Compiled at: 2012-03-28 00:11:36
assfile = 'test.ass'
fx = 'fxs.simple'
video_in = 'tos open2.avi'
video_out = 'out.avi'
fps = 29.97
width = 640
height = 358
frames = 100000
start_frame = 0
out_parameters = [
 '-i', video_in, '-map', '0:0', '-map', '1:1',
 '-sameq',
 '-acodec', 'libmp3lame', '-ab', '192k',
 '-vcodec', 'mpeg4', '-vtag', 'xvid',
 '-y', video_out]