# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robmoorman/Developer/moori/wagtail-speech/src/wagtailspeech/mixins.py
# Compiled at: 2017-05-23 05:38:49
# Size of source mod 2**32: 333 bytes


class SynthesizeSpeechMixin(object):
    __doc__ = '\n    Mixin class to support synthesize speech functionalities.\n\n    Example:\n        # File: models.py\n        class HomePage(SynthesizeSpeechMixin, Page):\n            def get_speech_text(self):\n                return self.title\n    '

    def get_speech_text(self):
        pass