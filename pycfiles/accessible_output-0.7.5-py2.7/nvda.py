# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\accessible_output\speech\outputs\nvda.py
# Compiled at: 2011-05-10 06:51:05
from ctypes import windll
from accessible_output import paths
from main import OutputError, ScreenreaderSpeechOutput

class NVDA(ScreenreaderSpeechOutput):
    """Supports The NVDA screen reader"""
    name = 'NVDA'

    def __init__(self, *args, **kwargs):
        super(NVDA, self).__init__(*args, **kwargs)
        try:
            self.dll = windll.LoadLibrary(paths.root('lib\\nvdaControllerClient32.dll'))
        except:
            raise OutputError

    def speak(self, text, interrupt=0):
        if interrupt:
            self.silence()
        self.dll.nvdaController_speakText(unicode(text))

    def silence(self):
        self.dll.nvdaController_cancelSpeech()

    def canSpeak(self):
        try:
            return self.dll.nvdaController_testIfRunning() == 0 and super(NVDA, self).canSpeak()
        except:
            return False