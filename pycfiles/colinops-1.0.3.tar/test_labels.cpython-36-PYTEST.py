# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/tests/integration/test_labels.py
# Compiled at: 2018-08-17 09:32:41
# Size of source mod 2**32: 3220 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, logging, pytest, colin

@pytest.fixture()
def empty_ruleset():
    return {'version':'1', 
     'name':'Laughing out loud ruleset', 
     'description':'This set of checks is required to pass because we said it', 
     'contact_email':'forgot-to-reply@example.nope', 
     'checks':[]}


def get_results_from_colin_labels_image():
    return colin.run('colin-labels', ruleset_name='fedora', logging_level=(logging.DEBUG))


def test_colin_image():
    @py_assert1 = get_results_from_colin_labels_image()
    if not @py_assert1:
        @py_format3 = 'assert %(py2)s\n{%(py2)s = %(py0)s()\n}' % {'py0':@pytest_ar._saferepr(get_results_from_colin_labels_image) if 'get_results_from_colin_labels_image' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_results_from_colin_labels_image) else 'get_results_from_colin_labels_image',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None


def test_labels_in_image():
    result = get_results_from_colin_labels_image()
    if not result:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    expected_dict = {'maintainer_label':'PASS', 
     'name_label':'PASS', 
     'com.redhat.component_label':'PASS', 
     'summary_label':'PASS', 
     'version_label':'PASS', 
     'run_or_usage_label':'PASS', 
     'release_label':'FAIL', 
     'architecture_label':'FAIL', 
     'url_label':'FAIL', 
     'help_label':'FAIL', 
     'build-date_label':'FAIL', 
     'distribution-scope_label':'FAIL', 
     'vcs-ref_label':'FAIL', 
     'vcs-type_label':'FAIL', 
     'description_label':'PASS', 
     'io.k8s.description_label':'PASS', 
     'vcs-url_label':'FAIL', 
     'help_file_or_readme':'FAIL', 
     'cmd_or_entrypoint':'PASS', 
     'no_root':'FAIL'}
    labels_dict = {}
    for res in result.results:
        labels_dict[res.check_name] = res.status

    for key in expected_dict.keys():
        @py_assert0 = labels_dict[key]
        @py_assert3 = expected_dict[key]
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None


@pytest.mark.parametrize('check, result', [
 (
  {'name':'run_or_usage_label', 
   'labels':['run']}, 'PASS'),
 (
  {'name':'run_or_usage_label', 
   'labels':['usage']}, 'FAIL'),
 (
  {'name':'run_or_usage_label', 
   'labels':['run', 'usage']}, 'PASS'),
 (
  {'name':'run_or_usage_label', 
   'labels':['something', 'different']}, 'FAIL'),
 (
  {'name':'run_or_usage_label', 
   'labels':['something', 'completely', 'different']}, 'FAIL')])
def test_multiple_labels_check(check, result, empty_ruleset):
    new_ruleset = dict(empty_ruleset)
    new_ruleset['checks'] = [check]
    check_result = colin.run('colin-labels', ruleset=new_ruleset)
    if not check_result:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(check_result) if 'check_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_result) else 'check_result'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    @py_assert0 = list(check_result.results)[0]
    @py_assert2 = @py_assert0.status
    @py_assert4 = @py_assert2 == result
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.status\n} == %(py5)s', ), (@py_assert2, result)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None