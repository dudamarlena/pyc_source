# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/Datos/devel/hg-repos/scru/scru/screenshot.py
# Compiled at: 2011-06-17 00:35:45
import subprocess, tempfile
SCREENSHOT_SOUND = '/usr/share/sounds/scru_shot.wav'

class ScrotNotFound(Exception):
    """scrot must be installed"""
    pass


def grab(filename, select, sound, quality, delay):
    """Grab the screen as binary file"""
    if not filename:
        f = tempfile.NamedTemporaryFile(suffix='.png', prefix='screenshot_scrot_')
        filename = f.name
    grab_filename(filename, select, sound, quality, delay)
    return open(filename, 'rb')


def grab_filename(filename, select, sound, quality, delay):
    """Grab the screen as image file"""
    try:
        cmd = [
         'scrot', filename]
        if select:
            cmd.append('-s')
            cmd.append('-b')
        if quality:
            cmd.append('-q%d' % quality)
        if delay:
            cmd.append('-d%d' % delay)
            cmd.append('-c')
        subprocess.call(cmd)
        if sound:
            play_screenshot_sound()
    except Exception as e:
        raise ScrotNotFound


def play_screenshot_sound():
    """"Play a sound of a camera shot"""
    try:
        subprocess.Popen(['aplay', '-q', SCREENSHOT_SOUND])
    except OSError:
        subprocess.Popen(['ossplay', '-q', SCREENSHOT_SOUND])