# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Spencer/Dropbox/School/CSC454/pywatson/build/lib/tests/answer/test_answer.py
# Compiled at: 2014-11-01 02:15:55
# Size of source mod 2**32: 2231 bytes
from pywatson.answer.answer import Answer
from pywatson.answer.error_notification import ErrorNotification
from pywatson.answer.evidence import Evidence
from pywatson.answer.synonym import Synonym, SynSetSynonym, SynSet
from pywatson.answer.watson_answer import WatsonAnswer

class TestAnswer(object):
    __doc__ = 'Unit tests for the WatsonQuestion class'

    def test___init___complete(self, answers):
        """WatsonAnswer is constructed properly with all parameters provided"""
        answer = WatsonAnswer(answers[0])
        assert answer.raw == answers[0]
        assert answer.id == '32C4518E1542435A994320B933D98FEE'
        assert len(answer.answers) == 5
        assert type(answer.answers[0]) is Answer
        assert answer.category is ''
        assert len(answer.error_notifications) == 1
        first_error_notification = answer.error_notifications[0]
        assert type(first_error_notification) is ErrorNotification
        assert first_error_notification.error == 'test error'
        assert first_error_notification.text == 'test error text'
        assert len(answer.evidence_list) == 5
        assert type(answer.evidence_list[0]) is Evidence
        assert len(answer.focus_list) == 1
        assert type(answer.focus_list[0]) is str
        assert len(answer.lat_list) == 1
        assert type(answer.lat_list[0]) is str
        assert answer.pipelineid == '153681347'
        assert len(answer.qclasslist) == 2
        assert type(answer.qclasslist[0]) is str
        assert answer.status == 'Complete'
        assert answer.supplemental is None
        assert len(answer.synonym_list) == 3
        first_synonym = answer.synonym_list[0]
        assert type(first_synonym) is Synonym
        assert first_synonym.part_of_speech == 'noun'
        assert type(first_synonym.syn_set) == SynSet
        assert first_synonym.syn_set.name == 'Wordnet_labor-noun-1'
        assert len(first_synonym.syn_set.synonyms) == 2
        first_synset_synonym = first_synonym.syn_set.synonyms[0]
        assert type(first_synset_synonym) is SynSetSynonym
        assert first_synset_synonym.is_chosen is True
        assert first_synset_synonym.value == 'proletariat'
        assert first_synset_synonym.weight == 1.0