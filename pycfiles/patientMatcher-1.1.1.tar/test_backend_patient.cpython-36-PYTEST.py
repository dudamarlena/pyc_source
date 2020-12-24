# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/tests/backend/test_backend_patient.py
# Compiled at: 2019-04-23 03:57:58
# Size of source mod 2**32: 2345 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, pytest
from patientMatcher.utils.add import load_demo, backend_add_patient
from patientMatcher.utils.delete import delete_by_query
from patientMatcher.parse.patient import mme_patient

def test_load_demo_patients(demo_data_path, database):
    """Testing if loading of 50 test patients in database is working as it should"""
    @py_assert1 = os.path
    @py_assert3 = @py_assert1.isfile
    @py_assert6 = @py_assert3(demo_data_path)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.isfile\n}(%(py5)s)\n}' % {'py0':@pytest_ar._saferepr(os) if 'os' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(os) else 'os',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(demo_data_path) if 'demo_data_path' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(demo_data_path) else 'demo_data_path',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    inserted_ids = load_demo(demo_data_path, database, 'patientMatcher.host.se')
    @py_assert2 = len(inserted_ids)
    @py_assert5 = 50
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(inserted_ids) if 'inserted_ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inserted_ids) else 'inserted_ids',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    re_inserted_ids = load_demo(demo_data_path, database, 'patientMatcher.host.se')
    @py_assert2 = len(re_inserted_ids)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(re_inserted_ids) if 're_inserted_ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(re_inserted_ids) else 're_inserted_ids',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    inserted_ids = load_demo('this_is_a_fakey_json_file.json', database, 'patientMatcher.host.se')
    @py_assert2 = len(inserted_ids)
    @py_assert5 = 0
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(inserted_ids) if 'inserted_ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inserted_ids) else 'inserted_ids',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None


def test_backend_remove_patient(json_patients, database):
    """ Test adding 2 test patients and then removing them using label or ID """
    test_mme_patients = [mme_patient(json_patient=patient) for patient in json_patients]
    @py_assert2 = len(test_mme_patients)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(test_mme_patients) if 'test_mme_patients' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_mme_patients) else 'test_mme_patients',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    inserted_ids = [backend_add_patient(mongo_db=database, host='patientMatcher.host.se', patient=mme_patient, match_external=False) for mme_patient in test_mme_patients]
    @py_assert2 = len(inserted_ids)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(inserted_ids) if 'inserted_ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inserted_ids) else 'inserted_ids',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    a_patient = database['patients'].find_one()
    if not a_patient:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(a_patient) if 'a_patient' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(a_patient) else 'a_patient'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    remove_query = {'_id': 'patient_1'}
    deleted = delete_by_query(remove_query, database, 'patients')
    db_patients = database['patients'].find()
    @py_assert1 = db_patients.count
    @py_assert3 = @py_assert1()
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.count\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(db_patients) if 'db_patients' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(db_patients) else 'db_patients',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    remove_query = {'label': 'Patient number 2'}
    deleted = delete_by_query(remove_query, database, 'patients')
    db_patients = database['patients'].find()
    @py_assert1 = db_patients.count
    @py_assert3 = @py_assert1()
    @py_assert6 = 0
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.count\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(db_patients) if 'db_patients' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(db_patients) else 'db_patients',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None