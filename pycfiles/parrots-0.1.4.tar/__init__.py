# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xuming06/Codes/parrots/parrots/__init__.py
# Compiled at: 2018-09-13 07:28:11
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""
from .pinyin2hanzi import Pinyin2Hanzi
from .speech_recognition import SpeechRecognition
from .tts import TextToSpeech
__version__ = '0.1.4'
sr = SpeechRecognition()
recognize_speech_from_file = sr.recognize_speech_from_file
p2h = Pinyin2Hanzi()
pinyin_2_hanzi = p2h.pinyin_2_hanzi
t2s = TextToSpeech()
update_syllables_dir = t2s.update_syllables_dir
speak = t2s.speak
synthesize = t2s.synthesize