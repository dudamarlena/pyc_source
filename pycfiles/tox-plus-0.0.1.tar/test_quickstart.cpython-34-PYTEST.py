# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/itxaka/Projects/tox-plus/tests/test_quickstart.py
# Compiled at: 2015-09-01 06:06:20
# Size of source mod 2**32: 14727 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, tox_plus._quickstart

@pytest.fixture(autouse=True)
def cleandir(tmpdir):
    tmpdir.chdir()


class TestToxQuickstartMain(object):

    def mock_term_input_return_values(self, return_values):
        for return_val in return_values:
            yield return_val

    def get_mock_term_input(self, return_values):
        generator = self.mock_term_input_return_values(return_values)

        def mock_term_input(prompt):
            try:
                return next(generator)
            except NameError:
                return generator.next()

        return mock_term_input

    def test_quickstart_main_choose_individual_pythons_and_pytest(self, monkeypatch):
        monkeypatch.setattr(tox_plus._quickstart, 'term_input', self.get_mock_term_input([
         '4',
         'Y',
         'Y',
         'Y',
         'Y',
         'Y',
         'Y',
         'Y',
         'N',
         'py.test',
         'pytest']))
        tox_plus._quickstart.main(argv=['tox-quickstart'])
        expected_tox_ini = '\n# Tox (http://tox.testrun.org/) is a tool for running tests\n# in multiple virtualenvs. This configuration file will run the\n# test suite on all supported python versions. To use it, "pip install tox"\n# and then run "tox" from this directory.\n\n[tox]\nenvlist = py26, py27, py32, py33, py34, py35, pypy\n\n[testenv]\ncommands = py.test\ndeps =\n    pytest\n'.lstrip()
        result = open('tox.ini').read()
        @py_assert1 = result == expected_tox_ini
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected_tox_ini)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(expected_tox_ini) if 'expected_tox_ini' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_tox_ini) else 'expected_tox_ini'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_quickstart_main_choose_individual_pythons_and_nose_adds_deps(self, monkeypatch):
        monkeypatch.setattr(tox_plus._quickstart, 'term_input', self.get_mock_term_input([
         '4',
         'Y',
         'Y',
         'Y',
         'Y',
         'Y',
         'Y',
         'Y',
         'N',
         'nosetests',
         '']))
        tox_plus._quickstart.main(argv=['tox-quickstart'])
        expected_tox_ini = '\n# Tox (http://tox.testrun.org/) is a tool for running tests\n# in multiple virtualenvs. This configuration file will run the\n# test suite on all supported python versions. To use it, "pip install tox"\n# and then run "tox" from this directory.\n\n[tox]\nenvlist = py26, py27, py32, py33, py34, py35, pypy\n\n[testenv]\ncommands = nosetests\ndeps =\n    nose\n'.lstrip()
        result = open('tox.ini').read()
        @py_assert1 = result == expected_tox_ini
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected_tox_ini)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(expected_tox_ini) if 'expected_tox_ini' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_tox_ini) else 'expected_tox_ini'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_quickstart_main_choose_individual_pythons_and_trial_adds_deps(self, monkeypatch):
        monkeypatch.setattr(tox_plus._quickstart, 'term_input', self.get_mock_term_input([
         '4',
         'Y',
         'Y',
         'Y',
         'Y',
         'Y',
         'Y',
         'Y',
         'N',
         'trial',
         '']))
        tox_plus._quickstart.main(argv=['tox-quickstart'])
        expected_tox_ini = '\n# Tox (http://tox.testrun.org/) is a tool for running tests\n# in multiple virtualenvs. This configuration file will run the\n# test suite on all supported python versions. To use it, "pip install tox"\n# and then run "tox" from this directory.\n\n[tox]\nenvlist = py26, py27, py32, py33, py34, py35, pypy\n\n[testenv]\ncommands = trial\ndeps =\n    twisted\n'.lstrip()
        result = open('tox.ini').read()
        @py_assert1 = result == expected_tox_ini
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected_tox_ini)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(expected_tox_ini) if 'expected_tox_ini' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_tox_ini) else 'expected_tox_ini'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_quickstart_main_choose_individual_pythons_and_pytest_adds_deps(self, monkeypatch):
        monkeypatch.setattr(tox_plus._quickstart, 'term_input', self.get_mock_term_input([
         '4',
         'Y',
         'Y',
         'Y',
         'Y',
         'Y',
         'Y',
         'Y',
         'N',
         'py.test',
         '']))
        tox_plus._quickstart.main(argv=['tox-quickstart'])
        expected_tox_ini = '\n# Tox (http://tox.testrun.org/) is a tool for running tests\n# in multiple virtualenvs. This configuration file will run the\n# test suite on all supported python versions. To use it, "pip install tox"\n# and then run "tox" from this directory.\n\n[tox]\nenvlist = py26, py27, py32, py33, py34, py35, pypy\n\n[testenv]\ncommands = py.test\ndeps =\n    pytest\n'.lstrip()
        result = open('tox.ini').read()
        @py_assert1 = result == expected_tox_ini
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected_tox_ini)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(expected_tox_ini) if 'expected_tox_ini' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_tox_ini) else 'expected_tox_ini'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_quickstart_main_choose_py27_and_pytest_adds_deps(self, monkeypatch):
        monkeypatch.setattr(tox_plus._quickstart, 'term_input', self.get_mock_term_input([
         '1',
         'py.test',
         '']))
        tox_plus._quickstart.main(argv=['tox-quickstart'])
        expected_tox_ini = '\n# Tox (http://tox.testrun.org/) is a tool for running tests\n# in multiple virtualenvs. This configuration file will run the\n# test suite on all supported python versions. To use it, "pip install tox"\n# and then run "tox" from this directory.\n\n[tox]\nenvlist = py27\n\n[testenv]\ncommands = py.test\ndeps =\n    pytest\n'.lstrip()
        result = open('tox.ini').read()
        @py_assert1 = result == expected_tox_ini
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected_tox_ini)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(expected_tox_ini) if 'expected_tox_ini' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_tox_ini) else 'expected_tox_ini'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_quickstart_main_choose_py27_and_py33_and_pytest_adds_deps(self, monkeypatch):
        monkeypatch.setattr(tox_plus._quickstart, 'term_input', self.get_mock_term_input([
         '2',
         'py.test',
         '']))
        tox_plus._quickstart.main(argv=['tox-quickstart'])
        expected_tox_ini = '\n# Tox (http://tox.testrun.org/) is a tool for running tests\n# in multiple virtualenvs. This configuration file will run the\n# test suite on all supported python versions. To use it, "pip install tox"\n# and then run "tox" from this directory.\n\n[tox]\nenvlist = py27, py33\n\n[testenv]\ncommands = py.test\ndeps =\n    pytest\n'.lstrip()
        result = open('tox.ini').read()
        @py_assert1 = result == expected_tox_ini
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected_tox_ini)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(expected_tox_ini) if 'expected_tox_ini' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_tox_ini) else 'expected_tox_ini'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_quickstart_main_choose_all_pythons_and_pytest_adds_deps(self, monkeypatch):
        monkeypatch.setattr(tox_plus._quickstart, 'term_input', self.get_mock_term_input([
         '3',
         'py.test',
         '']))
        tox_plus._quickstart.main(argv=['tox-quickstart'])
        expected_tox_ini = '\n# Tox (http://tox.testrun.org/) is a tool for running tests\n# in multiple virtualenvs. This configuration file will run the\n# test suite on all supported python versions. To use it, "pip install tox"\n# and then run "tox" from this directory.\n\n[tox]\nenvlist = py26, py27, py32, py33, py34, py35, pypy, jython\n\n[testenv]\ncommands = py.test\ndeps =\n    pytest\n'.lstrip()
        result = open('tox.ini').read()
        @py_assert1 = result == expected_tox_ini
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected_tox_ini)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(expected_tox_ini) if 'expected_tox_ini' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_tox_ini) else 'expected_tox_ini'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_quickstart_main_choose_individual_pythons_and_defaults(self, monkeypatch):
        monkeypatch.setattr(tox_plus._quickstart, 'term_input', self.get_mock_term_input([
         '4',
         '',
         '',
         '',
         '',
         '',
         '',
         '',
         '',
         '',
         '']))
        tox_plus._quickstart.main(argv=['tox-quickstart'])
        expected_tox_ini = '\n# Tox (http://tox.testrun.org/) is a tool for running tests\n# in multiple virtualenvs. This configuration file will run the\n# test suite on all supported python versions. To use it, "pip install tox"\n# and then run "tox" from this directory.\n\n[tox]\nenvlist = py26, py27, py32, py33, py34, py35, pypy, jython\n\n[testenv]\ncommands = {envpython} setup.py test\ndeps =\n\n'.lstrip()
        result = open('tox.ini').read()
        @py_assert1 = result == expected_tox_ini
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected_tox_ini)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(expected_tox_ini) if 'expected_tox_ini' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_tox_ini) else 'expected_tox_ini'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_quickstart_main_existing_tox_ini(self, monkeypatch):
        try:
            f = open('tox.ini', 'w')
            f.write('foo bar\n')
        finally:
            f.close()

        monkeypatch.setattr(tox_plus._quickstart, 'term_input', self.get_mock_term_input([
         '4',
         '',
         '',
         '',
         '',
         '',
         '',
         '',
         '',
         '',
         '',
         '']))
        tox_plus._quickstart.main(argv=['tox-quickstart'])
        expected_tox_ini = '\n# Tox (http://tox.testrun.org/) is a tool for running tests\n# in multiple virtualenvs. This configuration file will run the\n# test suite on all supported python versions. To use it, "pip install tox"\n# and then run "tox" from this directory.\n\n[tox]\nenvlist = py26, py27, py32, py33, py34, py35, pypy, jython\n\n[testenv]\ncommands = {envpython} setup.py test\ndeps =\n\n'.lstrip()
        result = open('tox-generated.ini').read()
        @py_assert1 = result == expected_tox_ini
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected_tox_ini)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(expected_tox_ini) if 'expected_tox_ini' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_tox_ini) else 'expected_tox_ini'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None


class TestToxQuickstart(object):

    def test_pytest(self):
        d = {'py26': True, 
         'py27': True, 
         'py32': True, 
         'py33': True, 
         'py34': True, 
         'pypy': True, 
         'commands': 'py.test', 
         'deps': 'pytest'}
        expected_tox_ini = '\n# Tox (http://tox.testrun.org/) is a tool for running tests\n# in multiple virtualenvs. This configuration file will run the\n# test suite on all supported python versions. To use it, "pip install tox"\n# and then run "tox" from this directory.\n\n[tox]\nenvlist = py26, py27, py32, py33, py34, pypy\n\n[testenv]\ncommands = py.test\ndeps =\n    pytest\n'.lstrip()
        d = tox_plus._quickstart.process_input(d)
        tox_plus._quickstart.generate(d)
        result = open('tox.ini').read()
        @py_assert1 = result == expected_tox_ini
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected_tox_ini)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(expected_tox_ini) if 'expected_tox_ini' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_tox_ini) else 'expected_tox_ini'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_setup_py_test(self):
        d = {'py26': True, 
         'py27': True, 
         'commands': 'python setup.py test', 
         'deps': ''}
        expected_tox_ini = '\n# Tox (http://tox.testrun.org/) is a tool for running tests\n# in multiple virtualenvs. This configuration file will run the\n# test suite on all supported python versions. To use it, "pip install tox"\n# and then run "tox" from this directory.\n\n[tox]\nenvlist = py26, py27\n\n[testenv]\ncommands = python setup.py test\ndeps =\n\n'.lstrip()
        d = tox_plus._quickstart.process_input(d)
        tox_plus._quickstart.generate(d)
        result = open('tox.ini').read()
        @py_assert1 = result == expected_tox_ini
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected_tox_ini)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(expected_tox_ini) if 'expected_tox_ini' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_tox_ini) else 'expected_tox_ini'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_trial(self):
        d = {'py27': True, 
         'commands': 'trial', 
         'deps': 'Twisted'}
        expected_tox_ini = '\n# Tox (http://tox.testrun.org/) is a tool for running tests\n# in multiple virtualenvs. This configuration file will run the\n# test suite on all supported python versions. To use it, "pip install tox"\n# and then run "tox" from this directory.\n\n[tox]\nenvlist = py27\n\n[testenv]\ncommands = trial\ndeps =\n    Twisted\n'.lstrip()
        d = tox_plus._quickstart.process_input(d)
        tox_plus._quickstart.generate(d)
        result = open('tox.ini').read()
        @py_assert1 = result == expected_tox_ini
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected_tox_ini)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(expected_tox_ini) if 'expected_tox_ini' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_tox_ini) else 'expected_tox_ini'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_nosetests(self):
        d = {'py27': True, 
         'py32': True, 
         'py33': True, 
         'py34': True, 
         'py35': True, 
         'pypy': True, 
         'commands': 'nosetests -v', 
         'deps': 'nose'}
        expected_tox_ini = '\n# Tox (http://tox.testrun.org/) is a tool for running tests\n# in multiple virtualenvs. This configuration file will run the\n# test suite on all supported python versions. To use it, "pip install tox"\n# and then run "tox" from this directory.\n\n[tox]\nenvlist = py27, py32, py33, py34, py35, pypy\n\n[testenv]\ncommands = nosetests -v\ndeps =\n    nose\n'.lstrip()
        d = tox_plus._quickstart.process_input(d)
        tox_plus._quickstart.generate(d)
        result = open('tox.ini').read()
        @py_assert1 = result == expected_tox_ini
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (result, expected_tox_ini)) % {'py0': @pytest_ar._saferepr(result) if 'result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(result) else 'result',  'py2': @pytest_ar._saferepr(expected_tox_ini) if 'expected_tox_ini' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_tox_ini) else 'expected_tox_ini'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None