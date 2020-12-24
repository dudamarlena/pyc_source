# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\accessible_output\speech\outputs\jaws.py
# Compiled at: 2011-05-28 04:47:20
from pywintypes import com_error
import win32gui, win32com.client
from main import OutputError, ScreenreaderSpeechOutput

class Jaws(ScreenreaderSpeechOutput):
    """Speech output supporting the Jaws for Windows screen reader."""
    name = 'jaws'

    def __init__(self, *args, **kwargs):
        super(Jaws, self).__init__(*args, **kwargs)
        try:
            self.object = win32com.client.Dispatch('FreedomSci.JawsApi')
        except com_error:
            try:
                self.object = win32com.client.Dispatch('jfwapi')
            except com_error:
                raise OutputError

    def speak(self, text, interrupt=False):
        self.object.SayString('      %s' % text, interrupt)

    def canSpeak(self):
        try:
            return self.object.SayString('', 0) == True or win32gui.FindWindow('JFWUI2', 'JAWS') != 0 and super(Jaws, self).canSpeak()
        except:
            return False