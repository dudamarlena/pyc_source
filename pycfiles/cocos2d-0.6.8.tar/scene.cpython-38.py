# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../..\cocos\scene.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 5424 bytes
"""
Scene class.
"""
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
else:

    class Scene(cocosnode.CocosNode):
        __doc__ = '\n        Creates a Scene with layers and / or scenes.\n\n        Responsibilities:\n            Control the dispatching of events to its layers; and background \n            music playback.\n\n        Arguments:\n            children (list[Layer or Scene]):\n                Layers or Scenes that will be part of the scene.\n                They are automatically assigned a z-level from 0 to\n                num_children.\n        '

        def __init__(self, *children):
            super(Scene, self).__init__()
            self._handlers_enabled = False
            for i, c in enumerate(children):
                self.add(c, z=i)
            else:
                x, y = director.get_window_size()
                self.transform_anchor_x = x // 2
                self.transform_anchor_y = y // 2
                self.music = None
                self.music_playing = False

        def on_enter(self):
            for c in self.get_children():
                c.parent = self
            else:
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