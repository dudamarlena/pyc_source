# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/tests/match/test_GT_matching.py
# Compiled at: 2019-04-23 03:57:58
# Size of source mod 2**32: 2063 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from patientMatcher.utils.add import load_demo
from patientMatcher.parse.patient import mme_patient
from patientMatcher.match.genotype_matcher import match

def test_genotype_matching(demo_data_path, database, json_patients):
    """Testing the genotyping matching algorithm"""
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
    @py_assert2 = len(test_mme_patients)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(test_mme_patients) if 'test_mme_patients' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_mme_patients) else 'test_mme_patients',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    a_patient = test_mme_patients[0]
    if not a_patient:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(a_patient) if 'a_patient' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a_patient) else 'a_patient'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    gt_features = a_patient['genomicFeatures']
    @py_assert2 = len(gt_features)
    @py_assert5 = 3
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(gt_features) if 'gt_features' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(gt_features) else 'gt_features',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    matches = match(database, gt_features, 0.5)
    @py_assert2 = matches.keys
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 4
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.keys\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(matches) if 'matches' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(matches) else 'matches',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    for key, value in matches.items():
        @py_assert0 = 'patient_obj'
        @py_assert2 = @py_assert0 in value
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, value)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = value['geno_score']
        @py_assert3 = 0
        @py_assert2 = @py_assert0 > @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('>', ), (@py_assert2,), ('%(py1)s > %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    gt_features[0]['gene']['id'] = ''
    matches = match(database, gt_features, 0.5)
    @py_assert2 = len(matches)
    @py_assert5 = 4
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(matches) if 'matches' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(matches) else 'matches',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    gt_features[1]['variant'] = None
    matches = match(database, gt_features, 0.5)
    @py_assert2 = matches.keys
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 4
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.keys\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(matches) if 'matches' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(matches) else 'matches',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None