# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\brett\git\verbecc\verbecc\conjugator.py
# Compiled at: 2019-07-28 19:15:08
# Size of source mod 2**32: 1775 bytes
from . import inflector_fr, inflector_es, inflector_it, inflector_pt, inflector_ro
SUPPORTED_LANGUAGES = {'fr':'français', 
 'es':'español', 
 'it':'italiano', 
 'pt':'português', 
 'ro':'română'}

class Conjugator:
    __doc__ = '\n    :param lang: two-letter language code\n    '

    def __init__(self, lang):
        if lang == 'fr':
            self._inflector = inflector_fr.InflectorFr()
        else:
            if lang == 'es':
                self._inflector = inflector_es.InflectorEs()
            else:
                if lang == 'it':
                    self._inflector = inflector_it.InflectorIt()
                else:
                    if lang == 'pt':
                        self._inflector = inflector_pt.InflectorPt()
                    else:
                        if lang == 'ro':
                            self._inflector = inflector_ro.InflectorRo()
                        else:
                            raise InvalidLangError

    def conjugate(self, infinitive):
        return self._inflector.conjugate(infinitive)

    def conjugate_mood(self, infinitive, mood_name):
        return self._inflector.conjugate_mood(infinitive, mood_name)

    def conjugate_mood_tense(self, infinitive, mood_name, tense_name, alternate=False):
        return self._inflector.conjugate_mood_tense(infinitive, mood_name, tense_name, alternate)

    def get_verbs_list(self):
        return self._inflector.get_verbs_list()

    def get_templates_list(self):
        return self._inflector.get_templates_list()

    def find_verb_by_infinitive(self, infinitive):
        return self._inflector.find_verb_by_infinitive(infinitive)

    def find_template(self, name):
        return self._inflector.find_template(name)

    def get_verbs_that_start_with(self, query, max_results):
        return self._inflector.get_verbs_that_start_with(query, max_results)