# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/snipsmanagercore/tts.py
# Compiled at: 2017-12-14 05:47:52
""" Wrapper for various TTS services (currently only Google). """
import json, os, time
from socket import error as socket_error
from gtts import gTTS
from .audio_player import AudioPlayer

class GTTS:
    """ Google TTS service. """

    def __init__(self, locale, logger=None):
        """ Initialise the service.
        :param locale: the language locale, e.g. "fr" or "en_US".
        """
        self.logger = logger
        self.locale = locale.split('_')[0]

    def speak(self, sentence):
        """ Speak a sentence using Google TTS.
        :param sentence: the sentence to speak.
        """
        temp_dir = '/tmp/'
        filename = 'gtts.mp3'
        file_path = ('{}/{}').format(temp_dir, filename)
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        def delete_file():
            try:
                os.remove(file_path)
                if not os.listdir(temp_dir):
                    try:
                        os.rmdir(temp_dir)
                    except OSError:
                        pass

            except:
                pass

        if self.logger is not None:
            self.logger.info(('Google TTS: {}').format(sentence))
        tts = gTTS(text=sentence, lang=self.locale)
        tts.save(file_path)
        AudioPlayer.play_async(file_path, delete_file)
        return