# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\dev\cocos2020\cocos\scene.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 5424 bytes
__doc__ = '\nScene class.\n'
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
__all__ = [
 'Scene']
import cocos
import cocos.director as director
import cocos.cocosnode as cocosnode
try:
    import cocos.audio.music
except Exception:
    pass

class Scene(cocosnode.CocosNode):
    """Scene"""

    def __init__(self, *children):
        super(Scene, self).__init__()
        self._handlers_enabled = False
        for i, c in enumerate(children):
            self.add(c, z=i)

        x, y = director.get_window_size()
        self.transform_anchor_x = x // 2
        self.transform_anchor_y = y // 2
        self.music = None
        self.music_playing = False

    def on_enter(self):
        for c in self.get_children():
            c.parent = self

        super(Scene, self).on_enter()
        if self.music is not None:
            cocos.audio.music.control.load(self.music)
        if self.music_playing:
            cocos.audio.music.control.play()

    def on_exit(self):
        super(Scene, self).on_exit()
        if self.music_playing:
            cocos.audio.music.control.stop()

    def end(self, value=None):
        """Ends the current scene.

        This is accomplished by calling :meth:`.Director.pop`.
        Also sets ``director.return_value`` to ``value``.

        Arguments:
            value(anything):
                The return value. It can be anything. A type or an instance.
        """
        director.return_value = value
        director.pop()

    def load_music(self, filename):
        """This prepares a streamed music file to be played in this scene.

        Music will be stopped after calling this (even if it was playing before).

        Arguments:
            filename (str): Filename of music to load.
                Depending on installed libraries, supported formats may be
                WAV, MP3, OGG, MOD. You can also use ``None`` to unset music.
        """
        self.music = filename
        self.music_playing = False
        if self.is_running:
            if filename is not None:
                cocos.audio.music.control.load(filename)
            else:
                cocos.audio.music.control.stop()

    def play_music(self):
        """Enable music playback for this scene. Nothing happens if music was 
        already playing.

        Note that if you call this method on an inactive scene, the music will
        start playing back only if/when the scene gets activated.
        """
        if self.music is not None:
            if not self.music_playing:
                self.music_playing = True
                if self.is_running:
                    cocos.audio.music.control.play()

    def stop_music(self):
        """Stops music playback for this scene.
        """
        self.load_music(None)