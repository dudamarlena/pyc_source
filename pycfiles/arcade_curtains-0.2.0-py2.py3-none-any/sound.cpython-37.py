# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\sound.py
# Compiled at: 2020-04-19 09:45:09
# Size of source mod 2**32: 2538 bytes
__doc__ = '\nSound library.\n'
import pyglet
from pathlib import Path

class Sound:

    def __init__(self, file_name: str):
        if file_name.startswith(':resources:'):
            import os
            path = os.path.dirname(os.path.abspath(__file__))
            file_name = f"{path}/resources/{file_name[11:]}"
        if not Path(file_name).is_file():
            raise FileNotFoundError(f"The sound file '{file_name}' is not a file or can't be read")
        self.file_name = file_name
        self.player = pyglet.media.load(file_name)

    def play(self):
        if self.player.is_queued:
            player = pyglet.media.load(self.file_name)
            player.play()
        else:
            self.player.play()


class PlaysoundException(Exception):
    pass


def _load_sound_library():
    """
    Special code for Windows so we grab the proper library from our directory.
    Otherwise hope the correct package is installed.
    """
    import pyglet_ffmpeg2
    pyglet_ffmpeg2.load_ffmpeg()


_load_sound_library._sound_library_loaded = False

def load_sound(file_name: str):
    """
    Load a sound. Support for .wav files. If ffmpeg is available, will work
    with ogg and mp3 as well.

    :param str file_name: Name of the sound file to load.

    :returns: Sound object
    :rtype: Sound
    """
    try:
        sound = Sound(file_name)
        return sound
    except Exception as e:
        try:
            print(f'Unable to load sound file: "{file_name}". Exception: {e}')
            return
        finally:
            e = None
            del e


def play_sound(sound: Sound):
    """
    Play a sound.

    :param Sound sound: Sound loaded by load_sound. Do NOT use a string here for the filename.
    """
    if sound is None:
        print('Unable to play sound, no data passed in.')
        return
        if isinstance(sound, str):
            msg = 'Error, passed in a string as a sound. Make sure to use load_sound first, and use that result in play_sound.'
            raise Exception(msg)
    else:
        try:
            sound.play()
        except Exception as e:
            try:
                print('Error playing sound.', e)
            finally:
                e = None
                del e


def stop_sound(sound: pyglet.media.Source):
    """
    Stop a sound that is currently playing.

    :param sound:
    """
    sound.pause()


_load_sound_library()