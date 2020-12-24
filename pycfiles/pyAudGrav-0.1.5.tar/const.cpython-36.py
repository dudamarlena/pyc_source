# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/const.py
# Compiled at: 2019-10-03 01:06:50
# Size of source mod 2**32: 1193 bytes
__doc__ = 'Constants used in the public API.'
MAJOR_VERSION = 0
MINOR_VERSION = 4
PATCH_VERSION = '0.dev0'
__short_version__ = '{}.{}'.format(MAJOR_VERSION, MINOR_VERSION)
__version__ = '{}.{}'.format(__short_version__, PATCH_VERSION)
PROTOCOL_DMAP = 1
PROTOCOL_MRP = 2
PROTOCOL_AIRPLAY = 3
MEDIA_TYPE_UNKNOWN = 1
MEDIA_TYPE_VIDEO = 2
MEDIA_TYPE_MUSIC = 3
MEDIA_TYPE_TV = 4
PLAY_STATE_IDLE = 0
PLAY_STATE_NO_MEDIA = 1
PLAY_STATE_LOADING = 2
PLAY_STATE_PAUSED = 3
PLAY_STATE_PLAYING = 4
PLAY_STATE_FAST_FORWARD = 5
PLAY_STATE_FAST_BACKWARD = 6
PLAY_STATE_STOPPED = 7
REPEAT_STATE_OFF = 0
REPEAT_STATE_TRACK = 1
REPEAT_STATE_ALL = 2