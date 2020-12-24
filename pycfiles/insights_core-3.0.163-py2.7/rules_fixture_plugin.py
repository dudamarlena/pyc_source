# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/plugins/rules_fixture_plugin.py
# Compiled at: 2019-05-23 13:36:34
from insights.core.plugins import rule, make_fail, make_pass
from insights.parsers import installed_rpms, uname as uname_mod

@rule(optional=[installed_rpms.InstalledRpms, uname_mod.Uname])
def report(rpms, uname):
    if rpms is not None:
        bash_ver = rpms.get_max('bash')
        if uname is not None:
            return make_pass('PASS', bash_ver=bash_ver.nvr, uname_ver=uname.version)
        return make_fail('FAIL', bash_ver=bash_ver.nvr, path=rpms.file_path)
    return