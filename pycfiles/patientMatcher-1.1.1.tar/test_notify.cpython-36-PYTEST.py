# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/tests/utils/test_notify.py
# Compiled at: 2019-04-23 03:57:58
# Size of source mod 2**32: 1736 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pymongo
from patientMatcher.utils.notify import notify_match_external, notify_match_internal, html_format

def test_notify_match_external(match_objs, mock_sender, mock_mail):
    match_obj = match_objs[0]
    @py_assert0 = match_obj['match_type']
    @py_assert3 = 'external'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    notify_complete = True
    notify_match_external(match_obj, mock_sender, mock_mail, notify_complete)
    @py_assert1 = mock_mail._send_was_called
    if not @py_assert1:
        @py_format3 = 'assert %(py2)s\n{%(py2)s = %(py0)s._send_was_called\n}' % {'py0':@pytest_ar._saferepr(mock_mail) if 'mock_mail' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_mail) else 'mock_mail',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = mock_mail._message
    if not @py_assert1:
        @py_format3 = 'assert %(py2)s\n{%(py2)s = %(py0)s._message\n}' % {'py0':@pytest_ar._saferepr(mock_mail) if 'mock_mail' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_mail) else 'mock_mail',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None


def test_notify_match_internal(database, match_objs, mock_sender, mock_mail):
    match_obj = match_objs[2]
    @py_assert0 = match_obj['match_type']
    @py_assert3 = 'internal'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = database['patients']
    @py_assert2 = @py_assert0.find
    @py_assert4 = @py_assert2()
    @py_assert6 = @py_assert4.count
    @py_assert8 = @py_assert6()
    @py_assert11 = 0
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.find\n}()\n}.count\n}()\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    database['patients'].insert_one({'_id': 'external_patient_1'})
    @py_assert0 = database['patients']
    @py_assert2 = @py_assert0.find
    @py_assert4 = @py_assert2()
    @py_assert6 = @py_assert4.count
    @py_assert8 = @py_assert6()
    @py_assert11 = 1
    @py_assert10 = @py_assert8 == @py_assert11
    if not @py_assert10:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.find\n}()\n}.count\n}()\n} == %(py12)s', ), (@py_assert8, @py_assert11)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = None
    notify_complete = False
    notify_match_internal(database, match_obj, mock_sender, mock_mail, notify_complete)
    formatted_results = html_format(match_obj['results'])
    @py_assert0 = '<div style="margin-left: 0em">'
    @py_assert2 = @py_assert0 in formatted_results
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, formatted_results)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(formatted_results) if 'formatted_results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(formatted_results) else 'formatted_results'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert1 = mock_mail._send_was_called
    if not @py_assert1:
        @py_format3 = 'assert %(py2)s\n{%(py2)s = %(py0)s._send_was_called\n}' % {'py0':@pytest_ar._saferepr(mock_mail) if 'mock_mail' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_mail) else 'mock_mail',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = mock_mail._message
    if not @py_assert1:
        @py_format3 = 'assert %(py2)s\n{%(py2)s = %(py0)s._message\n}' % {'py0':@pytest_ar._saferepr(mock_mail) if 'mock_mail' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(mock_mail) else 'mock_mail',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None