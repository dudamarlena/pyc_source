# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\brett\git\verbecc\verbecc\conjugation_template.py
# Compiled at: 2019-07-28 19:40:14
# Size of source mod 2**32: 893 bytes
from lxml import etree
from .mood import Mood
from . import exceptions

class ConjugationTemplate:

    def __init__(self, template_elem):
        if template_elem.tag != 'template':
            raise exceptions.ConjugationTemplateError('Unexpected element')
        try:
            self.name = '' + template_elem.get('name')
            self.moods = {}
            for mood_elem in template_elem:
                mood = Mood(mood_elem)
                self.moods[mood_elem.tag.lower()] = mood

        except AttributeError as e:
            try:
                raise exceptions.ConjugationTemplateError('Error parsing {}: {}'.format(etree.tostring(template_elem), str(e)))
            finally:
                e = None
                del e

    def __repr__(self):
        return 'name={} moods={}'.format(self.name, self.moods)