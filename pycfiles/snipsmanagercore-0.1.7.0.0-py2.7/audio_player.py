# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/snipsmanagercore/audio_player.py
# Compiled at: 2017-10-06 07:49:42
""" A simple audio player based on pygame. """
import pygame, threading, time

class AudioPlayer:
    """ A simple audio player based on pygame. """

    @classmethod
    def play(cls, file_path, on_done=None, logger=None):
        """ Play an audio file.

        :param file_path: the path to the file to play.
        :param on_done: callback when audio playback completes.
        """
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(file_path)
        except pygame.error as e:
            if logger is not None:
                logger.warning(str(e))
            return

        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            continue

        if on_done:
            on_done()
        return

    @classmethod
    def play_async(cls, file_path, on_done=None):
        """ Play an audio file asynchronously.

        :param file_path: the path to the file to play.
        :param on_done: callback when audio playback completes.
        """
        thread = threading.Thread(target=AudioPlayer.play, args=(file_path, on_done))
        thread.start()

    @classmethod
    def stop(cls):
        """ Stop the audio. """
        pygame.mixer.init()
        pygame.mixer.music.stop()

    @classmethod
    def pause(cls):
        """ Pause the audio. """
        pygame.mixer.init()
        pygame.mixer.music.pause()

    @classmethod
    def resume(cls):
        """ Resume the audio. """
        pygame.mixer.init()
        pygame.mixer.music.unpause()