# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Spencer/Dropbox/School/CSC454/pywatson/build/lib/tests/answer/test_answer.py
# Compiled at: 2014-11-01 02:15:55
# Size of source mod 2**32: 2231 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
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
        @py_assert1 = answer.raw
        @py_assert4 = answers[0]
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.raw\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = answer.id
        @py_assert4 = '32C4518E1542435A994320B933D98FEE'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.id\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert2 = answer.answers
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 5
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.answers\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py1': @pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer',  'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py8': @pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert1 = answer.answers[0]
        @py_assert3 = type(@py_assert1)
        @py_assert5 = @py_assert3 is Answer
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py6)s', ), (@py_assert3, Answer)) % {'py6': @pytest_ar._saferepr(Answer) if 'Answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Answer) else 'Answer',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = answer.category
        @py_assert4 = ''
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.category\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert2 = answer.error_notifications
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.error_notifications\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py1': @pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer',  'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py8': @pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        first_error_notification = answer.error_notifications[0]
        @py_assert2 = type(first_error_notification)
        @py_assert4 = @py_assert2 is ErrorNotification
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} is %(py5)s', ), (@py_assert2, ErrorNotification)) % {'py5': @pytest_ar._saferepr(ErrorNotification) if 'ErrorNotification' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ErrorNotification) else 'ErrorNotification',  'py1': @pytest_ar._saferepr(first_error_notification) if 'first_error_notification' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first_error_notification) else 'first_error_notification',  'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None
        @py_assert1 = first_error_notification.error
        @py_assert4 = 'test error'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.error\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(first_error_notification) if 'first_error_notification' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first_error_notification) else 'first_error_notification'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = first_error_notification.text
        @py_assert4 = 'test error text'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(first_error_notification) if 'first_error_notification' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first_error_notification) else 'first_error_notification'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert2 = answer.evidence_list
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 5
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.evidence_list\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py1': @pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer',  'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py8': @pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert1 = answer.evidence_list[0]
        @py_assert3 = type(@py_assert1)
        @py_assert5 = @py_assert3 is Evidence
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py6)s', ), (@py_assert3, Evidence)) % {'py6': @pytest_ar._saferepr(Evidence) if 'Evidence' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Evidence) else 'Evidence',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert2 = answer.focus_list
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.focus_list\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py1': @pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer',  'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py8': @pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert1 = answer.focus_list[0]
        @py_assert3 = type(@py_assert1)
        @py_assert5 = @py_assert3 is str
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py6)s', ), (@py_assert3, str)) % {'py6': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert2 = answer.lat_list
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 1
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.lat_list\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py1': @pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer',  'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py8': @pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert1 = answer.lat_list[0]
        @py_assert3 = type(@py_assert1)
        @py_assert5 = @py_assert3 is str
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py6)s', ), (@py_assert3, str)) % {'py6': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = answer.pipelineid
        @py_assert4 = '153681347'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.pipelineid\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert2 = answer.qclasslist
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 2
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.qclasslist\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py1': @pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer',  'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py8': @pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        @py_assert1 = answer.qclasslist[0]
        @py_assert3 = type(@py_assert1)
        @py_assert5 = @py_assert3 is str
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('is', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} is %(py6)s', ), (@py_assert3, str)) % {'py6': @pytest_ar._saferepr(str) if 'str' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(str) else 'str',  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        @py_assert1 = answer.status
        @py_assert4 = 'Complete'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.status\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = answer.supplemental
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.supplemental\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert2 = answer.synonym_list
        @py_assert4 = len(@py_assert2)
        @py_assert7 = 3
        @py_assert6 = @py_assert4 == @py_assert7
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.synonym_list\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py1': @pytest_ar._saferepr(answer) if 'answer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(answer) else 'answer',  'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py8': @pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
        first_synonym = answer.synonym_list[0]
        @py_assert2 = type(first_synonym)
        @py_assert4 = @py_assert2 is Synonym
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} is %(py5)s', ), (@py_assert2, Synonym)) % {'py5': @pytest_ar._saferepr(Synonym) if 'Synonym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Synonym) else 'Synonym',  'py1': @pytest_ar._saferepr(first_synonym) if 'first_synonym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first_synonym) else 'first_synonym',  'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None
        @py_assert1 = first_synonym.part_of_speech
        @py_assert4 = 'noun'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.part_of_speech\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(first_synonym) if 'first_synonym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first_synonym) else 'first_synonym'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert2 = first_synonym.syn_set
        @py_assert4 = type(@py_assert2)
        @py_assert6 = @py_assert4 == SynSet
        if not @py_assert6:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.syn_set\n})\n} == %(py7)s', ), (@py_assert4, SynSet)) % {'py7': @pytest_ar._saferepr(SynSet) if 'SynSet' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SynSet) else 'SynSet',  'py5': @pytest_ar._saferepr(@py_assert4),  'py1': @pytest_ar._saferepr(first_synonym) if 'first_synonym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first_synonym) else 'first_synonym',  'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type'}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert1 = first_synonym.syn_set
        @py_assert3 = @py_assert1.name
        @py_assert6 = 'Wordnet_labor-noun-1'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.syn_set\n}.name\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6),  'py4': @pytest_ar._saferepr(@py_assert3),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(first_synonym) if 'first_synonym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first_synonym) else 'first_synonym'}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
        @py_assert2 = first_synonym.syn_set
        @py_assert4 = @py_assert2.synonyms
        @py_assert6 = len(@py_assert4)
        @py_assert9 = 2
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.syn_set\n}.synonyms\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py7': @pytest_ar._saferepr(@py_assert6),  'py5': @pytest_ar._saferepr(@py_assert4),  'py1': @pytest_ar._saferepr(first_synonym) if 'first_synonym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first_synonym) else 'first_synonym',  'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py10': @pytest_ar._saferepr(@py_assert9),  'py3': @pytest_ar._saferepr(@py_assert2)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
        first_synset_synonym = first_synonym.syn_set.synonyms[0]
        @py_assert2 = type(first_synset_synonym)
        @py_assert4 = @py_assert2 is SynSetSynonym
        if not @py_assert4:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} is %(py5)s', ), (@py_assert2, SynSetSynonym)) % {'py5': @pytest_ar._saferepr(SynSetSynonym) if 'SynSetSynonym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SynSetSynonym) else 'SynSetSynonym',  'py1': @pytest_ar._saferepr(first_synset_synonym) if 'first_synset_synonym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first_synset_synonym) else 'first_synset_synonym',  'py3': @pytest_ar._saferepr(@py_assert2),  'py0': @pytest_ar._saferepr(type) if 'type' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type) else 'type'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert2 = @py_assert4 = None
        @py_assert1 = first_synset_synonym.is_chosen
        @py_assert4 = True
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.is_chosen\n} is %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(first_synset_synonym) if 'first_synset_synonym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first_synset_synonym) else 'first_synset_synonym'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = first_synset_synonym.value
        @py_assert4 = 'proletariat'
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.value\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(first_synset_synonym) if 'first_synset_synonym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first_synset_synonym) else 'first_synset_synonym'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = first_synset_synonym.weight
        @py_assert4 = 1.0
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.weight\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py5': @pytest_ar._saferepr(@py_assert4),  'py2': @pytest_ar._saferepr(@py_assert1),  'py0': @pytest_ar._saferepr(first_synset_synonym) if 'first_synset_synonym' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(first_synset_synonym) else 'first_synset_synonym'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        return