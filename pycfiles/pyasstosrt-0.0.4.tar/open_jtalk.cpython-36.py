# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/garicchi/projects/remote/python/pi-assistant/assistant/tts/open_jtalk.py
# Compiled at: 2018-01-03 19:52:02
# Size of source mod 2**32: 1076 bytes
import subprocess, tempfile, assistant.util.package as package

class OpenJtalk:

    def __init__(self):
        package.install('open_jtalk', 'sudo apt-get install -y open-jtalk-mecab-naist-jdic hts-voice-nitech-jp-atr503-m001 open-jtalk')
        self.hts_voice = '/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice'
        self.speech_rate = 1.0

    def say(self, text):
        temp = tempfile.NamedTemporaryFile()
        file_text = temp.name + '.txt'
        with open(file_text, 'w') as (f):
            f.write(text + '\n')
        temp = tempfile.NamedTemporaryFile()
        file_audio = temp.name + '.wav'
        dic = '/var/lib/mecab/dic/open-jtalk/naist-jdic'
        cmd = 'open_jtalk -m %s -x %s -ow %s %s -r %f' % (
         self.hts_voice,
         dic,
         file_audio,
         file_text,
         self.speech_rate)
        subprocess.call(cmd.split(' '))
        cmd = 'aplay %s' % file_audio
        subprocess.call(cmd.split(' '))