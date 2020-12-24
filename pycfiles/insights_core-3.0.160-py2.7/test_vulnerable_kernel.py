# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_vulnerable_kernel.py
# Compiled at: 2019-05-16 13:41:33
from __future__ import print_function
from insights.parsers.uname import Uname
from insights.core.plugins import make_fail
from insights.tests import context_wrap, InputData, run_test
from insights.specs import Specs
from insights.plugins import vulnerable_kernel
ERROR_KEY = 'VULNERABLE_KERNEL'
UNAME_TEMPLATE = 'Linux testhost1 %s #1 SMP Tue Jan 29 11:47:41 EST 2013 x86_64 x86_64 x86_64 GNU/Linux'
NOT_VULNERABLE = [
 '2.4.32-100.el6.x86_64',
 '2.6.32-430.el6.x86_64',
 '2.6.32-431.11.2.el6.x86_64',
 '2.6.32-431.11.3.el6.x86_64',
 '2.6.32-432.el6.x86_64',
 '2.7.12-200.el6.x86_64']
VULNERABLE = [
 '2.6.32-431.el6.x86_64',
 '2.6.32-431.10.1.el6.x86_64',
 '2.6.32-431.11.1.el6.x86_64']

def test_vulnerable_kernel():
    for kernel in NOT_VULNERABLE:
        uname_line = UNAME_TEMPLATE % kernel
        result = vulnerable_kernel.report(Uname(context_wrap(uname_line)))
        expected = None
        result == expected or print(result)
        print(expected)
        assert result == expected
        assert False

    for kernel in VULNERABLE:
        uname_line = UNAME_TEMPLATE % kernel
        result = vulnerable_kernel.report(Uname(context_wrap(uname_line)))
        expected = make_fail(ERROR_KEY, kernel=kernel)
        result == expected or print(result)
        print(expected)
        assert result == expected
        assert False

    return


def generate_inputs(things):
    for kernel in things:
        uname_line = UNAME_TEMPLATE % kernel
        i = InputData()
        i.add(Specs.uname, uname_line)
        yield (kernel, i)


def test_vulnerable_kernel_integration():
    comp = vulnerable_kernel.report
    for kernel, i in generate_inputs(VULNERABLE):
        expected = make_fail(ERROR_KEY, kernel=kernel)
        run_test(comp, i, expected)

    for _, i in generate_inputs(NOT_VULNERABLE):
        run_test(comp, i, None)

    return