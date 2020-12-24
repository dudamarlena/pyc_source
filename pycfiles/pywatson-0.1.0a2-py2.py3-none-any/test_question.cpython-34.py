# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Spencer/Dropbox/School/CSC454/pywatson/build/lib/tests/question/test_question.py
# Compiled at: 2014-11-01 02:19:56
# Size of source mod 2**32: 1688 bytes
from pywatson.question.evidence_request import EvidenceRequest
from pywatson.question.filter import Filter
from pywatson.question.watson_question import WatsonQuestion

class TestQuestion(object):
    __doc__ = 'Unit tests for the WatsonQuestion class'

    def test___init___basic(self, questions):
        """Question is constructed properly with just question_text"""
        question = WatsonQuestion(questions[0]['questionText'])
        assert question.question_text == questions[0]['questionText']

    def test___init___complete(self, questions):
        """Question is constructed properly with all parameters provided"""
        q = questions[1]
        er = q['evidenceRequest']
        evidence_request = EvidenceRequest(er['items'], er['profile'])
        filters = tuple(Filter(f['filterType'], f['filterName'], f['values']) for f in q['filters'])
        question = WatsonQuestion(question_text=q['questionText'], answer_assertion=q['answerAssertion'], category=q['category'], context=q['context'], evidence_request=evidence_request, filters=filters, formatted_answer=q['formattedAnswer'], items=q['items'], lat=q['lat'], passthru=q['passthru'], synonym_list=q['synonyms'])
        assert question.question_text == q['questionText']
        assert question.answer_assertion == q['answerAssertion']
        assert question.category == q['category']
        assert question.context == q['context']
        assert question.evidence_request == evidence_request
        assert question.filters == filters