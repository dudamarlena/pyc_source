# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ls_edac_mc.py
# Compiled at: 2020-03-25 13:10:41
from insights.parsers import ls_edac_mc
from insights.parsers.ls_edac_mc import LsEdacMC
from insights.tests import context_wrap
import doctest
LS_EDAC_MC = '\n/sys/devices/system/edac/mc:\ntotal 37592\ndrwxr-xr-x. 3 0 0 0 Jan 10 10:33 .\ndrwxr-xr-x. 3 0 0 0 Jan 10 10:33 ..\ndrwxr-xr-x. 2 0 0 0 Jan 10 10:33 power\ndrwxr-xr-x. 2 0 0 0 Jan 10 10:33 mc0\ndrwxr-xr-x. 2 0 0 0 Jan 10 10:33 mc1\ndrwxr-xr-x. 2 0 0 0 Jan 10 10:33 mc2\n'

def test_ls_edac_mc():
    ls_edac_mc = LsEdacMC(context_wrap(LS_EDAC_MC))
    assert '/sys/devices/system/edac/mc' in ls_edac_mc
    assert ls_edac_mc.dirs_of('/sys/devices/system/edac/mc') == ['.', '..', 'power', 'mc0', 'mc1', 'mc2']


def test_ls_etc_documentation():
    failed_count, tests = doctest.testmod(ls_edac_mc, globs={'ls_edac_mc': ls_edac_mc.LsEdacMC(context_wrap(LS_EDAC_MC))})
    assert failed_count == 0