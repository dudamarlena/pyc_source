# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_plugins/test_plugin.py
# Compiled at: 2019-05-16 13:41:33
from insights.core.plugins import rule
from insights.parsers import installed_rpms, uname

@rule(optional=[installed_rpms.InstalledRpms, uname.Uname])
def report(rpms, un):
    pass