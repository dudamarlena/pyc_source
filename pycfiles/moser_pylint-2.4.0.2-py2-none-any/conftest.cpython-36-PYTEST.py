# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/conftest.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 1040 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, pytest
from pylint import checkers
from pylint.lint import PyLinter
from pylint.testutils import MinimalTestReporter

@pytest.fixture
def linter(checker, register, enable, disable, reporter):
    _linter = PyLinter()
    _linter.set_reporter(reporter())
    checkers.initialize(_linter)
    if register:
        register(_linter)
    if checker:
        _linter.register_checker(checker(_linter))
    if disable:
        for msg in disable:
            _linter.disable(msg)

    if enable:
        for msg in enable:
            _linter.enable(msg)

    os.environ.pop('PYLINTRC', None)
    return _linter


@pytest.fixture(scope='module')
def checker():
    pass


@pytest.fixture(scope='module')
def register():
    pass


@pytest.fixture(scope='module')
def enable():
    pass


@pytest.fixture(scope='module')
def disable():
    pass


@pytest.fixture(scope='module')
def reporter():
    return MinimalTestReporter