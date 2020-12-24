# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\despres\Desktop\reaper\scripts\reapy\reapy\core\reaper\ui.py
# Compiled at: 2019-03-23 06:48:50
# Size of source mod 2**32: 1019 bytes
"""User interface-related functions."""
import reapy
import reapy.reascript_api as RPR

def get_color_theme():
    """
    Return path to last color theme file.

    Returns
    -------
    color_theme : str
        Path to last color theme file.
    """
    return RPR.GetLastColorThemeFile()


def get_leftmost_track_in_mixer():
    """Return leftmost track in mixer."""
    return reapy.Track(RPR.GetMixerScroll())


def set_color_theme(path):
    """
    Set REAPER color theme.

    Parameters
    ----------
    path : str
        Path to color theme file.
    """
    RPR.OpenColorThemeFile(path)


def set_leftmost_track_in_mixer(track):
    """Set leftmost track in mixer.

    The actual leftmost track in mixer might be different after
    calling if there is not enough tracks to the right of the
    specified track.

    Parameters
    ----------
    track : Track
        Track to set as leftmost track in mixer.
    """
    RPR.SetMixerScroll(track.id)