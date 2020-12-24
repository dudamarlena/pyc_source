# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/tests/match/test_pheno_matching.py
# Compiled at: 2019-04-25 05:55:40
# Size of source mod 2**32: 4771 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from patientMatcher.utils.add import load_demo
from patientMatcher.match.phenotype_matcher import match, similarity_wrapper
from patientMatcher.parse.patient import mme_patient
from patientMatcher.resources import path_to_hpo_terms, path_to_phenotype_annotations
from patient_similarity import HPO, Diseases, HPOIC, Patient
from patient_similarity.__main__ import compare_patients
PHENOTYPE_ROOT = 'HP:0000118'

def test_patient_similarity_wrapper():
    """test the wrapper around this repo: https://github.com/buske/patient-similarity"""
    hpo = HPO(path_to_hpo_terms, new_root=PHENOTYPE_ROOT)
    if not hpo:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(hpo) if 'hpo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hpo) else 'hpo'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    diseases = Diseases(path_to_phenotype_annotations)
    if not diseases:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(diseases) if 'diseases' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(diseases) else 'diseases'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    hpoic = HPOIC(hpo, diseases, orphanet=None, patients=False, use_disease_prevalence=False, use_phenotype_frequency=False,
      distribute_ic_to_leaves=False)
    if not hpoic:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(hpoic) if 'hpoic' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hpoic) else 'hpoic'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    query_p_terms = ['HP:0008058', 'HP:0007033', 'HP:0002194', 'HP:0002281']
    score = similarity_wrapper(hpoic=hpoic, hpo=hpo, max_hpo_score=1.0, hpo_terms_q=query_p_terms, hpo_terms_m=query_p_terms)
    @py_assert2 = 12
    @py_assert4 = round(score, @py_assert2)
    @py_assert7 = 1
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(round) if 'round' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(round) else 'round',  'py1':@pytest_ar._saferepr(score) if 'score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(score) else 'score',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    match_p_terms = [
     'HP:0008058', 'HP:0007033', 'HP:0002194']
    related_pheno_score = similarity_wrapper(hpoic=hpoic, hpo=hpo, max_hpo_score=1.0, hpo_terms_q=query_p_terms, hpo_terms_m=match_p_terms)
    @py_assert2 = 2
    @py_assert4 = round(related_pheno_score, @py_assert2)
    @py_assert6 = @py_assert4 < score
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('<', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} < %(py7)s', ), (@py_assert4, score)) % {'py0':@pytest_ar._saferepr(round) if 'round' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(round) else 'round',  'py1':@pytest_ar._saferepr(related_pheno_score) if 'related_pheno_score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(related_pheno_score) else 'related_pheno_score',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(score) if 'score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(score) else 'score'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert2 = 0.8
    @py_assert1 = related_pheno_score > @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('>', ), (@py_assert1,), ('%(py0)s > %(py3)s', ), (related_pheno_score, @py_assert2)) % {'py0':@pytest_ar._saferepr(related_pheno_score) if 'related_pheno_score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(related_pheno_score) else 'related_pheno_score',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    match_p_terms = [
     'HP:0003002', 'HP:0000218']
    unrelated_pheno_score = similarity_wrapper(hpoic=hpoic, hpo=hpo, max_hpo_score=1.0, hpo_terms_q=query_p_terms, hpo_terms_m=match_p_terms)
    @py_assert2 = 2
    @py_assert4 = round(unrelated_pheno_score, @py_assert2)
    @py_assert7 = 0
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(round) if 'round' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(round) else 'round',  'py1':@pytest_ar._saferepr(unrelated_pheno_score) if 'unrelated_pheno_score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(unrelated_pheno_score) else 'unrelated_pheno_score',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    if not unrelated_pheno_score:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(unrelated_pheno_score) if 'unrelated_pheno_score' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(unrelated_pheno_score) else 'unrelated_pheno_score'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))


def test_phenotype_matching(json_patients, database, demo_data_path):
    """test the algorithm that compares the phenotype of a query patient against the database"""
    inserted_ids = load_demo(demo_data_path, database, 'patientMatcher.host.se')
    @py_assert2 = len(inserted_ids)
    @py_assert5 = 50
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(inserted_ids) if 'inserted_ids' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inserted_ids) else 'inserted_ids',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    query_patient = json_patients[0]
    if not query_patient:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(query_patient) if 'query_patient' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(query_patient) else 'query_patient'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    formatted_patient = mme_patient(query_patient)
    @py_assert1 = formatted_patient['features']
    @py_assert3 = len(@py_assert1)
    @py_assert6 = 0
    @py_assert5 = @py_assert3 > @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('>', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} > %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = formatted_patient['disorders']
    @py_assert3 = len(@py_assert1)
    @py_assert6 = 0
    @py_assert5 = @py_assert3 > @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('>', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} > %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    matches_HPO_OMIM = match(database, 0.75, formatted_patient['features'], formatted_patient['disorders'])
    @py_assert2 = matches_HPO_OMIM.keys
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 50
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.keys\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(matches_HPO_OMIM) if 'matches_HPO_OMIM' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(matches_HPO_OMIM) else 'matches_HPO_OMIM',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    for key, value in matches_HPO_OMIM.items():
        @py_assert0 = 'patient_obj'
        @py_assert2 = @py_assert0 in value
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, value)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = value['pheno_score']
        @py_assert3 = 0
        @py_assert2 = @py_assert0 > @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('>', ), (@py_assert2,), ('%(py1)s > %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    features = formatted_patient['features']
    disorders = formatted_patient['disorders']
    formatted_patient['features'] = []
    matches_OMIM = match(database, 0.75, formatted_patient['features'], formatted_patient['disorders'])
    @py_assert1 = []
    @py_assert4 = matches_OMIM.keys
    @py_assert6 = @py_assert4()
    @py_assert8 = len(@py_assert6)
    @py_assert11 = 0
    @py_assert10 = @py_assert8 > @py_assert11
    @py_assert0 = @py_assert10
    if @py_assert10:
        @py_assert18 = matches_OMIM.keys
        @py_assert20 = @py_assert18()
        @py_assert22 = len(@py_assert20)
        @py_assert25 = 50
        @py_assert24 = @py_assert22 < @py_assert25
        @py_assert0 = @py_assert24
    if not @py_assert0:
        @py_format13 = @pytest_ar._call_reprcompare(('>', ), (@py_assert10,), ('%(py9)s\n{%(py9)s = %(py2)s(%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.keys\n}()\n})\n} > %(py12)s', ), (@py_assert8, @py_assert11)) % {'py2':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py3':@pytest_ar._saferepr(matches_OMIM) if 'matches_OMIM' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(matches_OMIM) else 'matches_OMIM',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = '%(py14)s' % {'py14': @py_format13}
        @py_assert1.append(@py_format15)
        if @py_assert10:
            @py_format27 = @pytest_ar._call_reprcompare(('<', ), (@py_assert24,), ('%(py23)s\n{%(py23)s = %(py16)s(%(py21)s\n{%(py21)s = %(py19)s\n{%(py19)s = %(py17)s.keys\n}()\n})\n} < %(py26)s', ), (@py_assert22, @py_assert25)) % {'py16':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py17':@pytest_ar._saferepr(matches_OMIM) if 'matches_OMIM' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(matches_OMIM) else 'matches_OMIM',  'py19':@pytest_ar._saferepr(@py_assert18),  'py21':@pytest_ar._saferepr(@py_assert20),  'py23':@pytest_ar._saferepr(@py_assert22),  'py26':@pytest_ar._saferepr(@py_assert25)}
            @py_format29 = '%(py28)s' % {'py28': @py_format27}
            @py_assert1.append(@py_format29)
        @py_format30 = @pytest_ar._format_boolop(@py_assert1, 0) % {}
        @py_format32 = 'assert %(py31)s' % {'py31': @py_format30}
        raise AssertionError(@pytest_ar._format_explanation(@py_format32))
    @py_assert0 = @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert11 = @py_assert18 = @py_assert20 = @py_assert22 = @py_assert24 = @py_assert25 = None
    for key, value in matches_OMIM.items():
        @py_assert0 = 'patient_obj'
        @py_assert2 = @py_assert0 in value
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, value)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = value['pheno_score']
        @py_assert3 = 0
        @py_assert2 = @py_assert0 > @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('>', ), (@py_assert2,), ('%(py1)s > %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    formatted_patient['disorders'] = []
    matches_no_phenotypes = match(database, 0.75, formatted_patient['features'], formatted_patient['disorders'])
    @py_assert2 = matches_no_phenotypes.keys
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 0
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.keys\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(matches_no_phenotypes) if 'matches_no_phenotypes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(matches_no_phenotypes) else 'matches_no_phenotypes',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    formatted_patient['features'] = features
    matches_HPO = match(database, 0.75, formatted_patient['features'], formatted_patient['disorders'])
    @py_assert2 = matches_HPO.keys
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert9 = 50
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.keys\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(matches_HPO) if 'matches_HPO' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(matches_HPO) else 'matches_HPO',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    for key, value in matches_HPO.items():
        @py_assert0 = 'patient_obj'
        @py_assert2 = @py_assert0 in value
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, value)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(value) if 'value' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(value) else 'value'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        @py_assert0 = value['pheno_score']
        @py_assert3 = 0
        @py_assert2 = @py_assert0 > @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('>', ), (@py_assert2,), ('%(py1)s > %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    @py_assert2 = matches_HPO_OMIM.keys
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert11 = matches_OMIM.keys
    @py_assert13 = @py_assert11()
    @py_assert15 = len(@py_assert13)
    @py_assert8 = @py_assert6 >= @py_assert15
    if not @py_assert8:
        @py_format17 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.keys\n}()\n})\n} >= %(py16)s\n{%(py16)s = %(py9)s(%(py14)s\n{%(py14)s = %(py12)s\n{%(py12)s = %(py10)s.keys\n}()\n})\n}', ), (@py_assert6, @py_assert15)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(matches_HPO_OMIM) if 'matches_HPO_OMIM' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(matches_HPO_OMIM) else 'matches_HPO_OMIM',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py10':@pytest_ar._saferepr(matches_OMIM) if 'matches_OMIM' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(matches_OMIM) else 'matches_OMIM',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = None
    @py_assert2 = matches_HPO_OMIM.keys
    @py_assert4 = @py_assert2()
    @py_assert6 = len(@py_assert4)
    @py_assert11 = matches_HPO.keys
    @py_assert13 = @py_assert11()
    @py_assert15 = len(@py_assert13)
    @py_assert8 = @py_assert6 >= @py_assert15
    if not @py_assert8:
        @py_format17 = @pytest_ar._call_reprcompare(('>=', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.keys\n}()\n})\n} >= %(py16)s\n{%(py16)s = %(py9)s(%(py14)s\n{%(py14)s = %(py12)s\n{%(py12)s = %(py10)s.keys\n}()\n})\n}', ), (@py_assert6, @py_assert15)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(matches_HPO_OMIM) if 'matches_HPO_OMIM' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(matches_HPO_OMIM) else 'matches_HPO_OMIM',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py10':@pytest_ar._saferepr(matches_HPO) if 'matches_HPO' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(matches_HPO) else 'matches_HPO',  'py12':@pytest_ar._saferepr(@py_assert11),  'py14':@pytest_ar._saferepr(@py_assert13),  'py16':@pytest_ar._saferepr(@py_assert15)}
        @py_format19 = 'assert %(py18)s' % {'py18': @py_format17}
        raise AssertionError(@pytest_ar._format_explanation(@py_format19))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert11 = @py_assert13 = @py_assert15 = None