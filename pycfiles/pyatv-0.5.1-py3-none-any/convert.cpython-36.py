# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/convert.py
# Compiled at: 2019-10-03 01:06:50
# Size of source mod 2**32: 3119 bytes
"""Various types of extraction and conversion functions."""
from pyatv import const, exceptions

def media_kind(kind):
    """Convert iTunes media kind to API representation."""
    if kind in (1, ):
        return const.MEDIA_TYPE_UNKNOWN
    else:
        if kind in (3, 7, 11, 12, 13, 18, 32):
            return const.MEDIA_TYPE_VIDEO
        if kind in (2, 4, 10, 14, 17, 21, 36):
            return const.MEDIA_TYPE_MUSIC
        if kind in (8, 64):
            return const.MEDIA_TYPE_TV
    raise exceptions.UnknownMediaKind('Unknown media kind: ' + str(kind))


def media_type_str(mediatype):
    """Convert internal API media type to string."""
    if mediatype == const.MEDIA_TYPE_UNKNOWN:
        return 'Unknown'
    else:
        if mediatype == const.MEDIA_TYPE_VIDEO:
            return 'Video'
        else:
            if mediatype == const.MEDIA_TYPE_MUSIC:
                return 'Music'
            if mediatype == const.MEDIA_TYPE_TV:
                return 'TV'
        return 'Unsupported'


def playstate(state):
    """Convert iTunes playstate to API representation."""
    if state is None:
        return const.PLAY_STATE_NO_MEDIA
    else:
        if state == 0:
            return const.PLAY_STATE_IDLE
        else:
            if state == 1:
                return const.PLAY_STATE_LOADING
            else:
                if state == 2:
                    return const.PLAY_STATE_STOPPED
                if state == 3:
                    return const.PLAY_STATE_PAUSED
                if state == 4:
                    return const.PLAY_STATE_PLAYING
            if state == 5:
                return const.PLAY_STATE_FAST_FORWARD
        if state == 6:
            return const.PLAY_STATE_FAST_BACKWARD
    raise exceptions.UnknownPlayState('Unknown playstate: ' + str(state))


def playstate_str(state):
    """Convert internal API playstate to string."""
    if state == const.PLAY_STATE_NO_MEDIA:
        return 'No media'
    else:
        if state == const.PLAY_STATE_IDLE:
            return 'Idle'
        else:
            if state == const.PLAY_STATE_LOADING:
                return 'Loading'
            else:
                if state == const.PLAY_STATE_PAUSED:
                    return 'Paused'
                else:
                    if state == const.PLAY_STATE_PLAYING:
                        return 'Playing'
                    if state == const.PLAY_STATE_FAST_FORWARD:
                        return 'Fast forward'
                if state == const.PLAY_STATE_FAST_BACKWARD:
                    return 'Fast backward'
            if state == const.PLAY_STATE_STOPPED:
                return 'Stopped'
        return 'Unsupported'


def repeat_str(state):
    """Convert internal API repeat state to string."""
    if state == const.REPEAT_STATE_OFF:
        return 'Off'
    else:
        if state == const.REPEAT_STATE_TRACK:
            return 'Track'
        if state == const.REPEAT_STATE_ALL:
            return 'All'
        return 'Unsupported'


def ms_to_s(time):
    """Convert time in ms to seconds."""
    if time is None:
        return 0
    else:
        if time >= 4294967295:
            return 0
        return round(time / 1000.0)


def protocol_str(protocol):
    """Convert internal API protocol to string."""
    if protocol == const.PROTOCOL_MRP:
        return 'MRP'
    else:
        if protocol == const.PROTOCOL_DMAP:
            return 'DMAP'
        if protocol == const.PROTOCOL_AIRPLAY:
            return 'AirPlay'
        return 'Unknown'