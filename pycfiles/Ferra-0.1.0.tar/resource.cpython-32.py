# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Python32\lib\site-packages\Ferra\resource.py
# Compiled at: 2012-10-03 09:44:58
from pyglet import media
from pyglet import image

def load_image(name):
    """ load an image """
    return image.load(name)


def load_animation(name):
    """ load an animation """
    return image.load_animation(name)


def load_media(name, streaming=False):
    """ Load video or audio """
    return media.load(name, streaming=streaming)


class AudioPlayer(object):
    """ A simple audio player with the use:
        myaudio = Ferra.resource.AudioPlayer("myaudio.mp3", window)
        it automatically starts playing to make it not auto-start:
        myaudio = Ferra.resource.AudioPlayer("myaudio.mp3", window, autostart=False)
        VideoPlayer will be implemented soon
        window is the window this is important because AudioPlayer is an on_close handler
        it automatically stops the sound or music when the window is closed
        Experimental: NOT YET TESTED!
    """

    def __init__(self, audioname, window, autostart=True):
        self.media = load_media(audioname)
        if autostart == True:
            self.media.play()
            window.push_handlers(self)
        else:
            window.push_handlers(self)

    def on_close(self):
        self.seek(0.0)
        self.pause()

    def play(self):
        """ play the music or sound """
        self.media.play()

    def pause(self):
        """ Pause or stop(if you don't call play again it is stop) """
        self.media.pause()

    def seek(self, length):
        """ Fast forward or rewind to length """
        self.pause()
        self.media.seek(length)
        self.play()