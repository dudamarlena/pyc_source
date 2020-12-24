# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/tests/integration/test_dynamic_checks.py
# Compiled at: 2018-06-08 08:01:48
# Size of source mod 2**32: 1381 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, colin, pytest
from tests.conftest import LS_IMAGE, BASH_IMAGE

@pytest.fixture()
def ruleset():
    return {'version':'1', 
     'name':'Laughing out loud ruleset', 
     'description':'This set of checks is required to pass because we said it', 
     'contact_email':'forgot-to-reply@example.nope', 
     'checks':[
      {'name': 'shell_runnable'}]}


def test_dynamic_check_ls(ruleset):
    results = colin.run(target=LS_IMAGE, ruleset=ruleset, logging_level=10)
    @py_assert1 = results.ok
    @py_assert3 = not @py_assert1
    if not @py_assert3:
        @py_format4 = ('' + 'assert not %(py2)s\n{%(py2)s = %(py0)s.ok\n}') % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format4))
    @py_assert1 = @py_assert3 = None


def test_dynamic_check_bash(ruleset):
    results = colin.run(target=BASH_IMAGE, ruleset=ruleset, logging_level=10)
    @py_assert1 = results.ok
    if not @py_assert1:
        @py_format3 = ('' + 'assert %(py2)s\n{%(py2)s = %(py0)s.ok\n}') % {'py0':@pytest_ar._saferepr(results) if 'results' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(results) else 'results',  'py2':@pytest_ar._saferepr(@py_assert1)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format3))
    @py_assert1 = None