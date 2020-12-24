# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/integration.py
# Compiled at: 2019-11-14 13:57:46
from itertools import islice
from insights import tests
from insights.core.dr import get_name, load_components

def test_integration(component, compare_func, input_data, expected):
    actual = tests.run_test(component, input_data)
    compare_func(actual, expected)


def pytest_generate_tests(metafunc):
    pattern = metafunc.config.getoption('-k')
    generate_tests(metafunc, test_integration, 'insights/tests', pattern=pattern)


def generate_tests(metafunc, test_func, package_names, pattern=None):
    """
    This function hooks in to pytest's test collection framework and provides a
    test for every (input_data, expected) tuple that is generated from all
    @archive_provider-decorated functions.
    """
    if metafunc.function is test_func:
        if type(package_names) not in (list, tuple):
            package_names = [
             package_names]
        for package_name in package_names:
            load_components(package_name, include=pattern or '.*', exclude=None)

        args = []
        ids = []
        slow_mode = metafunc.config.getoption('--runslow')
        fast_mode = metafunc.config.getoption('--smokey')
        for f in tests.ARCHIVE_GENERATORS:
            ts = f(stride=1 if slow_mode else f.stride)
            if fast_mode:
                ts = islice(ts, 0, 1)
            for t in ts:
                args.append(t)
                input_data_name = (isinstance(t[2], list) or t[2]).name if 1 else 'multi-node'
                ids.append(('#').join([get_name(f), input_data_name]))

        metafunc.parametrize('component,compare_func,input_data,expected', args, ids=ids)
    return