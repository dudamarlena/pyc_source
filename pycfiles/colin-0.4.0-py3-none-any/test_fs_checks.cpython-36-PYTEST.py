# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/tests/integration/test_fs_checks.py
# Compiled at: 2018-06-08 08:01:48
# Size of source mod 2**32: 1527 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, colin, pytest
from tests.conftest import BASH_IMAGE, LS_IMAGE

@pytest.fixture()
def ruleset():
    """ simple ruleset as a pytest fixture """
    return {'version':'1', 
     'name':'Laughing out loud ruleset', 
     'description':'This set of checks is required to pass because we said it', 
     'contact_email':'forgot-to-reply@example.nope', 
     'checks':[
      {'name': 'help_file_or_readme'}]}


@pytest.mark.parametrize('image_name,should_pass', [
 (
  LS_IMAGE, False),
 (
  BASH_IMAGE, True)])
def test_help_file_or_readme(ruleset, image_name, should_pass):
    """ verify that help_file_or_readme check works well """
    results = colin.run(target=image_name, ruleset=ruleset, logging_level=10)
    @py_assert1 = results.ok
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.ok\n}') % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None
    @py_assert1 = results.fail
    @py_assert3 = @py_assert1 is not should_pass
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.fail\n} is not %(py4)s', ), (@py_assert1, should_pass)) % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(should_pass) if 'should_pass' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(should_pass) else 'should_pass'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None