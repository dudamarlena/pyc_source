# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\accessible_output\speech\outputs\sa.py
# Compiled at: 2011-05-10 06:50:18
from ctypes import windll
from accessible_output import paths
from main import OutputError, ScreenreaderSpeechOutput

class SystemAccess(ScreenreaderSpeechOutput):
    """Supports System Access and System Access Mobile"""
    name = 'System Access'

    def __init__(self, *args, **kwargs):
        super(SystemAccess, self).__init__(*args, **kwargs)
        try:
            self.dll = windll.LoadLibrary(paths.root('lib\\SAAPI32.dll'))
        except:
            raise OutputError

    def speak(self, text, interrupt=0):
        if self.dll.SA_IsRunning():
            self.dll.SA_SayW(unicode(text))

    def canSpeak(self):
        try:
            return self.dll.SA_IsRunning() and super(SystemAccess, self).canSpeak()
        except:
            return False