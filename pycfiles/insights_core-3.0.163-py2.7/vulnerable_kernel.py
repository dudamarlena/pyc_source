# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/plugins/vulnerable_kernel.py
# Compiled at: 2019-05-16 13:41:33
from insights import make_fail, rule
from insights.parsers.uname import Uname

@rule(Uname)
def report(uname):
    if uname.fixed_by('2.6.32-431.11.2.el6', introduced_in='2.6.32-431.el6'):
        return make_fail('VULNERABLE_KERNEL', kernel=uname.kernel)