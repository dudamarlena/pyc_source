# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\myconfig2.py
# Compiled at: 2012-06-05 11:45:08
fx = 'fxs.used.pics3'
assfile = 'out.ass'
video_in = 'tos open2.avi'
video_out = 'out.avi'
start_frame = 0
_with_audio = [
 '-i', video_in, '-map', '0:0', '-map', '1:1']
_a_mp3 = ['-acodec', 'libmp3lame', '-ab', '192k']
_a_aac = ['-acodec', 'libvo_aacenc', '-ab', '96k']
_a_copy = ['-acodec', 'copy']
_v_mp4 = ['-vcodec', 'mpeg4', '-f', 'mp4']
_v_xvid = ['-vcodec', 'mpeg4', '-vtag', 'xvid']
_v_ffv1 = ['-vcodec', 'ffv1']
_webpm = ['-vcodec', 'libvpx', '-vpre', 'libvpx-720p', '-b:v', '3900k', '-acodec', 'libvorbis', '-b:a', '100k']
out_parameters = [
 '-sameq'] + _v_xvid + ['-y', video_out]