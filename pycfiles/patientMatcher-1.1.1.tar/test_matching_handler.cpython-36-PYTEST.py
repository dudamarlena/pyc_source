# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/tests/match/test_matching_handler.py
# Compiled at: 2019-04-23 03:57:58
# Size of source mod 2**32: 2613 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from patientMatcher.utils.add import load_demo, backend_add_patient
from patientMatcher.parse.patient import mme_patient
from patientMatcher.match.handler import internal_matcher, save_async_response, external_matcher

def test_internal_matching(demo_data_path, database, json_patients):
    """Testing the combined matching algorithm"""
    inserted_ids = load_demo(demo_data_path, database, False)
    @py_assert2 = len(inserted_ids)
    @py_assert5 = 50
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(inserted_ids) if 'inserted_ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inserted_ids) else 'inserted_ids',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    test_mme_patients = [mme_patient(patient) for patient in json_patients]
    a_patient = test_mme_patients[0]
    if not a_patient:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(a_patient) if 'a_patient' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a_patient) else 'a_patient'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    match_obj = internal_matcher(database, a_patient, 0.5, 0.5)
    matches = match_obj['results'][0]['patients']
    @py_assert2 = len(matches)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 > @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('>', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} > %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(matches) if 'matches' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(matches) else 'matches',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    higest_scored_patient = matches[0]
    lowest_scored_patient = matches[(-1)]
    @py_assert0 = higest_scored_patient['score']['patient']
    @py_assert3 = lowest_scored_patient['score']['patient']
    @py_assert2 = @py_assert0 > @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('>', ), (@py_assert2,), ('%(py1)s > %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_external_matching(database, test_node, json_patients):
    """Testing the function that trigger patient matching across connected nodes"""
    patient = json_patients[0]
    database['nodes'].insert_one(test_node)
    inserted_ids = backend_add_patient(mongo_db=database, host='patientMatcher.host.se', patient=patient, match_external=False)
    if not inserted_ids:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(inserted_ids) if 'inserted_ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inserted_ids) else 'inserted_ids'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    ext_m_result = external_matcher(database, 'pmatcher', patient, test_node['_id'])
    @py_assert3 = isinstance(ext_m_result, dict)
    if not @py_assert3:
        @py_format5 = 'assert %(py4)s\n{%(py4)s = %(py0)s(%(py1)s, %(py2)s)\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(ext_m_result) if 'ext_m_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ext_m_result) else 'ext_m_result',  'py2':@pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict',  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert3 = None
    @py_assert0 = ext_m_result['data']['patient']['id']
    @py_assert3 = patient['id']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = ext_m_result['has_matches']
    @py_assert3 = False
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = ext_m_result['match_type']
    @py_assert3 = 'external'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_save_async_response(database, test_node):
    """Testing the function that saves an async response object to database"""
    @py_assert0 = database['async_responses']
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
    save_async_response(database=database, node_obj=test_node, query_id='test',
      query_patient_id='test_patient')
    async_response = database['async_responses'].find_one()
    @py_assert0 = async_response['query_id']
    @py_assert3 = 'test'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = async_response['query_patient_id']
    @py_assert3 = 'test_patient'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = async_response['node']['id']
    @py_assert3 = test_node['_id']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = async_response['node']['label']
    @py_assert3 = test_node['label']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None