# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\accessible_output\speech\outputs\dolphin.py
# Compiled at: 2011-06-26 15:31:02
from ctypes import windll
from ... import output
from accessible_output import paths
from main import OutputError, ScreenreaderSpeechOutput

class Dolphin(ScreenreaderSpeechOutput):
    """Supports dolphin products."""
    name = 'dolphin'

    def __init__(self, *args, **kwargs):
        super(Dolphin, self).__init__(*args, **kwargs)
        try:
            self.dll = windll.LoadLibrary(paths.root('lib\\dolapi.dll'))
        except:
            raise OutputError

    def speak(self, text, interrupt=0):
        if interrupt:
            self.silence()
        if self.canSpeak():
            self.dll.DolAccess_Command(unicode(text), len(text) * 2 + 2, 1)

    def silence(self):
        self.dll.DolAccess_Action(141)

    def canSpeak(self):
        try:
            return self.dll.DolAccess_GetSystem() in (1, 4, 8) and super(Dolphin, self).canSpeak()
        except:
            return False