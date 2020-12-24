# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/pytest/_pytest/nose.py
# Compiled at: 2019-07-30 18:47:09
# Size of source mod 2**32: 2517 bytes
""" run test suites written for nose. """
import sys, py, pytest
from _pytest import unittest

def get_skip_exceptions():
    skip_classes = set()
    for module_name in ('unittest', 'unittest2', 'nose'):
        mod = sys.modules.get(module_name)
        if hasattr(mod, 'SkipTest'):
            skip_classes.add(mod.SkipTest)

    return tuple(skip_classes)


def pytest_runtest_makereport(item, call):
    if call.excinfo:
        if call.excinfo.errisinstance(get_skip_exceptions()):
            call2 = call.__class__(lambda : pytest.skip(str(call.excinfo.value)), call.when)
            call.excinfo = call2.excinfo


@pytest.mark.trylast
def pytest_runtest_setup(item):
    if is_potential_nosetest(item):
        if isinstance(item.parent, pytest.Generator):
            gen = item.parent
            if not hasattr(gen, '_nosegensetup'):
                call_optional(gen.obj, 'setup')
                if isinstance(gen.parent, pytest.Instance):
                    call_optional(gen.parent.obj, 'setup')
                gen._nosegensetup = True
        if not call_optional(item.obj, 'setup'):
            call_optional(item.parent.obj, 'setup')
        item.session._setupstate.addfinalizer(lambda : teardown_nose(item), item)


def teardown_nose(item):
    if is_potential_nosetest(item):
        if not call_optional(item.obj, 'teardown'):
            call_optional(item.parent.obj, 'teardown')


def pytest_make_collect_report(collector):
    if isinstance(collector, pytest.Generator):
        call_optional(collector.obj, 'setup')


def is_potential_nosetest(item):
    return isinstance(item, pytest.Function) and not isinstance(item, unittest.TestCaseFunction)


def call_optional(obj, name):
    method = getattr(obj, name, None)
    isfixture = hasattr(method, '_pytestfixturefunction')
    if method is not None:
        if not isfixture:
            if py.builtin.callable(method):
                method()
                return True