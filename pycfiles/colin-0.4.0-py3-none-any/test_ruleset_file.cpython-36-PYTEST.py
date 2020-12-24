# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/tests/integration/test_ruleset_file.py
# Compiled at: 2018-08-17 09:32:41
# Size of source mod 2**32: 3382 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, yaml, tempfile, colin, pytest

@pytest.fixture()
def ruleset():
    return {'version':'1', 
     'name':'Laughing out loud ruleset', 
     'description':'This set of checks is required to pass because we said it', 
     'contact_email':'forgot-to-reply@example.nope', 
     'checks':[
      {'name': 'maintainer_label'},
      {'name': 'name_label'},
      {'name': 'com.redhat.component_label'},
      {'name': 'help_label'}]}


@pytest.fixture()
def ruleset_coupled():
    return {'version':'1', 
     'name':'Laughing out loud coublet ruleset', 
     'description':'This set of checks is required to pass because we said it', 
     'contact_email':'forgot-to-reply@example.nope', 
     'checks':[
      {'names':[
        'maintainer_label', 'name_label', 'com.redhat.component_label'], 
       'additional_tags':[
        'required']}]}


@pytest.fixture()
def expected_dict():
    return {'maintainer_label':'PASS',  'name_label':'PASS', 
     'com.redhat.component_label':'PASS', 
     'help_label':'FAIL'}


def get_results_from_colin_labels_image(ruleset_name=None, ruleset_file=None, ruleset=None):
    return colin.run('colin-labels', ruleset_name=ruleset_name, ruleset_file=ruleset_file,
      ruleset=ruleset)


def test_specific_ruleset_as_fileobj(tmpdir, ruleset, expected_dict):
    _, t = tempfile.mkstemp(dir=(str(tmpdir)))
    with open(t, 'w') as (f):
        yaml.dump(ruleset, f)
    with open(t, 'r') as (f):
        result = get_results_from_colin_labels_image(ruleset_file=f)
    if not result:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
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


def test_specific_ruleset_directly(ruleset, expected_dict):
    result = get_results_from_colin_labels_image(ruleset=ruleset)
    if not result:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
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


def test_get_checks_directly(ruleset):
    checks = colin.get_checks(ruleset=ruleset)
    if not checks:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(checks) if 'checks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checks) else 'checks'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))


def test_coupled_ruleset(ruleset_coupled):
    checks = colin.get_checks(ruleset=ruleset_coupled)
    if not checks:
        @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(checks) if 'checks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checks) else 'checks'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format1))
    @py_assert2 = len(checks)
    @py_assert5 = 3
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(checks) if 'checks' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(checks) else 'checks',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    for c in checks:
        @py_assert0 = 'required'
        @py_assert4 = c.tags
        @py_assert2 = @py_assert0 in @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py5)s\n{%(py5)s = %(py3)s.tags\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c',  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None