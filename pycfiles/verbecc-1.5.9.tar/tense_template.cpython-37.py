# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\brett\git\verbecc\verbecc\tense_template.py
# Compiled at: 2019-07-28 19:42:17
# Size of source mod 2**32: 2936 bytes
from . import person_ending
from . import grammar_defines

class TenseTemplate:
    __doc__ = '\n    Contains PersonEndings for a specific verb template, mood and tense\n    Note: The template name and mood is only known by the Mood object\n          which owns this Tense.\n    Class relationships:\n        ConjugationTemplate has many Mood\n            Mood has many Tense\n                Tense has many PersonEnding\n    E.g. aim:er indicatif présent\n    name\n        the name of the tense, e.g. présent\n    tense_elem\n        A tense_elem contains one or more <p> (PersonEnding) elems\n        Example tense_elem children:\n            <p><i>e</i></p>\n            <p><i>es</i></p>\n            <p><i>e</i></p>\n            <p><i>ons</i></p>\n            <p><i>ez</i></p>\n            <p><i>ent</i></p>\n    '

    def __init__(self, tense_elem):
        self.name = tense_elem.tag
        self.person_endings = []
        person_num = 0
        for p_elem in tense_elem.findall('p'):
            person = grammar_defines.PERSONS[person_num]
            if self.name == 'imperatif-présent':
                person = grammar_defines.IMPERATIVE_PRESENT_PERSONS[person_num]
            pe = person_ending.PersonEnding(p_elem, person)
            person_num += 1
            if len(pe.endings) > 0:
                self.person_endings.append(pe)

    def __repr__(self):
        return 'person_endings={}'.format(self.person_endings)