# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pytalker/tts.py
# Compiled at: 2014-12-23 03:03:54
import sys, gobject
from urllib2 import Request, urlopen
try:
    import gst
except:
    print 'The gst library seems not to be installed. Please, try under Debian the following command and try again:\n\tsudo apt-get install python-gst0.10'

class Pytalker:

    def on_finish(self, bus, message):
        """ 
                    Callback triggered at the end of the stream.
        """
        self.player.set_state(gst.STATE_NULL)
        self.mainloop.quit()

    def __init__(self):
        """ 
                    Constructor of the internal player.
        """
        self.player = None
        self.mainloop = gobject.MainLoop()
        return

    def say(self, text, lang='en', volume=5.0):
        """ 
            Downloading and playing a text.

            :param text:    Text to be played.
            :param lang:    Languague in two-letter ISO standard. Default: 'en'.
            :param volume:  Volume of the reproduction. Default: 5.0.
        """
        music_stream_uri = 'http://translate.google.com/translate_tts?' + 'q=' + text + '&tl=' + lang + '&ie=UTF-8'
        self.player = gst.element_factory_make('playbin', 'player')
        self.player.set_property('uri', music_stream_uri)
        self.player.set_property('volume', volume)
        self.player.set_state(gst.STATE_PLAYING)
        bus = self.player.get_bus()
        bus.add_signal_watch_full(1)
        bus.connect('message::eos', self.on_finish)
        self.mainloop.run()

    def sayNB(self, text, lang='en', volume=5.0):
        """
            Downloading and playing a text in a Non Blocking way.

            :param text:    Text to be played.
            :param lang:    Languague in two-letter ISO standard. Default: 'en'.
            :param volume:  Volume of the reproduction. Default: 5.0.
        """
        music_stream_uri = 'http://translate.google.com/translate_tts?tl=' + lang + '&q=' + text + '&ie=UTF-8'
        self.player = gst.element_factory_make('playbin', 'player')
        self.player.set_property('uri', music_stream_uri)
        self.player.set_property('volume', volume)
        self.player.set_state(gst.STATE_PLAYING)

    def download(self, text, lang='en', filename='tts.mp3'):
        """
            Downloading the pronunciation of a text onto a given file.

            :param text:    Text to be played.
            :param lang:    Languague in two-letter ISO standard. Default: 'en'.
            :param filenam:  A valid filename for the downloadable file. Default: 'tts.mp3'.
        """
        req = Request(url='http://translate.google.com/translate_tts')
        req.add_header('User-Agent', 'My agent !')
        req.add_data('tl=' + lang + '&q=' + text + '&ie=UTF-8')
        fin = urlopen(req)
        mp3 = fin.read()
        with open(filename, 'wb') as (oF):
            oF.write(mp3)

    def play(self, audio_uri):
        """
            Tiny function to play any audio. This method is useful to play a sound locally.

            :param audio_uri:   Path to the file.
        """
        import pyglet
        sound = pyglet.resource.media(audio_uri)
        sound.play()
        pyglet.app.run()

    def setVolume(self, val):
        self.player.set_property('volume', val)