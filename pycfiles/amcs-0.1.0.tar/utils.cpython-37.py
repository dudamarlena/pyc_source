# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/utils.py
# Compiled at: 2019-05-14 22:48:33
# Size of source mod 2**32: 2463 bytes
import re
from distutils import util
PRECISION = 2

def clean_url(url):
    host = re.sub('^http[s]?://', '', url, flags=(re.IGNORECASE))
    host = re.sub('/$', '', host)
    return host


def pretty(value, delimiter='='):
    """Format string key=value."""
    try:
        return value.split(delimiter)[1]
    except AttributeError:
        pass


def percent(part, whole):
    """Convert data to percent"""
    return round(100 * float(part) / float(whole), PRECISION)


def str2bool(value):
    """
    Args:
        value - text to be converted to boolean
         True values: y, yes, true, t, on, 1
         False values: n, no, false, off, 0
    """
    try:
        if isinstance(value, (str, unicode)):
            return bool(util.strtobool(value))
    except NameError:
        if isinstance(value, str):
            return bool(util.strtobool(value))

    return bool(value)


def to_unit(value, unit='B'):
    """Convert bytes to give unit."""
    byte_array = [
     'B', 'KB', 'MB', 'GB', 'TB']
    if not isinstance(value, (int, float)):
        value = float(value)
    if unit in byte_array:
        result = value / 1024 ** byte_array.index(unit)
        return (
         round(result, PRECISION), unit)
    return value


def extract_audio_video_enabled(param, resp):
    """Extract if any audio/video stream enabled from response."""
    return 'true' in [part.split('=')[1] for part in resp.split() if '.{}Enable='.format(param) in part]


def enable_audio_video_cmd(param, enable):
    """Return command to enable/disable all audio/video streams."""
    cmd = 'configManager.cgi?action=setConfig'
    formats = [('Extra', 3), ('Main', 4)]
    if param == 'Video':
        formats.append(('Snap', 3))
    for fmt, num in formats:
        for i in range(num):
            cmd += '&Encode[0].{}Format[{}].{}Enable={}'.format(fmt, i, param, str(enable).lower())

    return cmd