# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\brett\git\verbecc\verbecc\mood.py
# Compiled at: 2019-07-28 19:41:48
# Size of source mod 2**32: 380 bytes
from .tense_template import TenseTemplate

class Mood:

    def __init__(self, mood_elem):
        self.name = mood_elem.tag.lower()
        self.tenses = {}
        for tense_elem in mood_elem:
            self.tenses[tense_elem.tag] = TenseTemplate(tense_elem)

    def __repr__(self):
        return 'name={} tenses={}'.format(self.name, self.tenses)