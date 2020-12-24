# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\brett\git\verbecc\verbecc\person_ending.py
# Compiled at: 2019-07-28 19:42:21
# Size of source mod 2**32: 1412 bytes


class PersonEnding:
    __doc__ = '\n    p_elem\n    aka <p>\n    Ending for a specific verb template, mood, tense and grammatical person\n    May also have an alternate ending for an alternative spelling.\n    E.g. Ending for aim:er indicatif présent 2nd Person Plural = [\'ez\']\n    E.g. Ending for pa:yer indicatif présent 1st Person Singular = [\'ie\', \'ye\']\n    Explanation: \'ye\' is an alternate spelling (je paie, je paye)\n    p_elem\n        Example p_elems:\n            <p><i>ez</i></p>\n            <p><i>eoir</i><i>oir</i></p>\n            <p></p>\n\n    person\n    A grammar_defines.PERSONS value indicating which person \n    this PersonEnding is for, e.g. for aim:er, "ez" is \'2p\' (second person plural)\n    '

    def __init__(self, p_elem, person):
        self.person = person
        self.endings = []
        for i_elem in p_elem.findall('i'):
            ending = ''
            if i_elem.text is not None:
                ending += i_elem.text
            self.endings.append(ending)

    def get_person(self):
        return self.person

    def get_ending(self):
        return self.endings[0]

    def get_alternate_ending_if_available(self):
        if len(self.endings) > 1:
            return self.endings[1]
        return self.endings[0]

    def __repr__(self):
        return 'person={} endings={}'.format(self.person, self.endings)