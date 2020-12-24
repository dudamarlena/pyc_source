# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\samples\tetrico\soundex.py
# Compiled at: 2020-01-13 11:01:20
# Size of source mod 2**32: 2131 bytes
from __future__ import division, print_function, unicode_literals
import os
from constants import MUSIC, SOUND
import pyglet
try:
    import pyglet_ffmpeg2
except ImportError:
    pyglet_ffmpeg2 = None
else:
    if pyglet_ffmpeg2:
        try:
            pyglet_ffmpeg2.load_ffmpeg()
        except Exception as ex:
            try:
                print('While trying to use ffmpeg audio from package pyglet_ffmpeg2 an exception was rised:')
                print(ex)
            finally:
                ex = None
                del ex

    try:
        decoders = pyglet.media.codecs._decoder_extensions.get('.mp3', [])
    except Exception:
        decoders = None
    else:
        if decoders:
            have_mp3 = True
        else:
            print('warn: cocos running with no sound, no mp3 decoder found.')
            print('      Try installing pyglet_ffmpeg2.')
            pyglet.options['audio'] = ('silent', )
            have_mp3 = False
            MUSIC = False
            SOUND = False
        music_player = pyglet.media.Player()
        current_music = None
        sound_vol = 0.7
        music_player.volume = 0.4

        def set_music(name):
            global current_music
            current_music = name


        def music_volume(vol):
            """sets player volume, vol a float between 0 and 1"""
            music_player.volume = vol


        def play_music():
            if not music_player.playing:
                return current_music or None
            else:
                return have_mp3 or None
            name = current_music
            music_player.next_source()
            music_player.queue(pyglet.resource.media(name, streaming=True))
            music_player.play()
            music_player.volume = music_player.volume
            music_player.loop = True


        def stop_music():
            music_player.pause()


        sounds = {}

        def load(name, streaming=False):
            if not SOUND:
                return
            if name not in sounds:
                sounds[name] = pyglet.resource.media(name, streaming=streaming)
            return sounds[name]


        def play(name):
            global sound_vol
            if not SOUND:
                return
            load(name)
            a = sounds[name].play().volume = sound_vol


        def sound_volume(vol):
            global sound_vol
            sound_vol = vol