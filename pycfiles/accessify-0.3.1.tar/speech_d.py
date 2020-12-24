# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\accessible_output\speech\outputs\speech_d.py
# Compiled at: 2011-05-10 06:37:41
import atexit
from main import OutputError, SpeechOutput, ScreenreaderSpeechOutput
import platform
speechd_object = None

class SpeechDispatcherOutput(SpeechOutput):
    """Linux output using Speech Dispatcher. Uses an SSIP connection. Uses default localhost, 6560."""
    name = 'speech-dispatcher'

    def __init__(self, *args, **kwargs):
        global speechd_object
        super(SpeechDispatcherOutput, self).__init__(*args, **kwargs)
        try:
            if not speechd_object:
                if platform.linux_distribution()[0] == 'Ubuntu' and platform.linux_distribution()[1] >= '10.10':
                    import speechd_client_new
                    speechd_object = speechd_client_new.SSIPClient('Accessible_Output')
                else:
                    import speechd_client
                    speechd_object = speechd_client.SSIPClient('Accessible_Output')
        except Exception as e:
            raise OutputError(e)

    def speak(self, text, interrupt=False):
        if interrupt:
            self.silence()
        speechd_object.speak(text)

    def silence(self):
        speechd_object.cancel()

    def canSpeak(self):
        if speechd_object is None:
            return False
        else:
            return True
            return

    def SwitchOutput(self, VoiceName):
        """Allows you to switch the output (to Espeak for example)"""
        Voices = speechd_object.list_output_modules()
        if VoiceName in Voices:
            speechd_object.set_output_module(str(VoiceName))
        else:
            return

    def SetLang(self, langstr):
        """Sets the two letter language according to RFC 1776."""
        speechd_object.set_language(str(langstr))

    def SetPitch(self, PitchInt):
        """" Sets the pitch. Takes an integer between -100 and 100, with 0 being the default."""
        speechd_object.set_pitch(int(PitchInt))

    def SetRate(self, RateInt):
        """Sets the rate of the voice. Takes an integer between -100 and 100, with 0 being the default."""
        speechd_object.set_rate(int(RateInt))

    def SetVoice(self, VoiceStr):
        """Sets the voice by symbolic name. Possible combinations are shown below.
      Symbolic voice names are mapped to real synthesizer voices in the
      configuration of the output module.  Use SwitchOutput() to use real voices."""
        if VoiceStr.lower() in ('male1', 'male2', 'male3', 'female1', 'female2', 'female3',
                                'child_male', 'child_female'):
            speechd_object.set_voice(VoiceStr)


def on_exit_event():
    global speechd_object
    del speechd_object


atexit.register(on_exit_event)