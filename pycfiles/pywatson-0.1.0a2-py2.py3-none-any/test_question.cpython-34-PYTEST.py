# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Spencer/Dropbox/School/CSC454/pywatson/build/lib/tests/question/test_question.py
# Compiled at: 2014-11-01 02:19:56
# Size of source mod 2**32: 1688 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pywatson.question.evidence_request import EvidenceRequest
from pywatson.question.filter import Filter
from pywatson.question.watson_question import WatsonQuestion

class TestQuestion(object):
    __doc__ = 'Unit tests for the WatsonQuestion class'

    def test___init___basic(self, questions):
        """Question is constructed properly with just question_text"""
        question = WatsonQuestion(questions[0]['questionText'])
        @py_assert1 = question.question_text
        @py_assert4 = questions[0]['questionText']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.question_text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(question) if 'question' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(question) else 'question'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        return

    def test___init___complete(self, questions):
        """Question is constructed properly with all parameters provided"""
        q = questions[1]
        er = q['evidenceRequest']
        evidence_request = EvidenceRequest(er['items'], er['profile'])
        filters = tuple(Filter(f['filterType'], f['filterName'], f['values']) for f in q['filters'])
        question = WatsonQuestion(question_text=q['questionText'], answer_assertion=q['answerAssertion'], category=q['category'], context=q['context'], evidence_request=evidence_request, filters=filters, formatted_answer=q['formattedAnswer'], items=q['items'], lat=q['lat'], passthru=q['passthru'], synonym_list=q['synonyms'])
        @py_assert1 = question.question_text
        @py_assert4 = q['questionText']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.question_text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(question) if 'question' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(question) else 'question'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = question.answer_assertion
        @py_assert4 = q['answerAssertion']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.answer_assertion\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(question) if 'question' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(question) else 'question'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = question.category
        @py_assert4 = q['category']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.category\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(question) if 'question' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(question) else 'question'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = question.context
        @py_assert4 = q['context']
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.context\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(question) if 'question' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(question) else 'question'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = question.evidence_request
        @py_assert3 = @py_assert1 == evidence_request
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.evidence_request\n} == %(py4)s', ), (@py_assert1, evidence_request)) % {'py4': @pytest_ar._saferepr(evidence_request) if 'evidence_request' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(evidence_request) else 'evidence_request',  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(question) if 'question' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(question) else 'question'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        @py_assert1 = question.filters
        @py_assert3 = @py_assert1 == filters
        if not @py_assert3:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.filters\n} == %(py4)s', ), (@py_assert1, filters)) % {'py4': @pytest_ar._saferepr(filters) if 'filters' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(filters) else 'filters',  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(question) if 'question' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(question) else 'question'}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        return