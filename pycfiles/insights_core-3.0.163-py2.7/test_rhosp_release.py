# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rhosp_release.py
# Compiled at: 2019-11-14 13:57:46
import doctest
from insights.parsers import rhosp_release
from insights.tests import context_wrap
ROCKY = ('\nRed Hat OpenStack Platform release 14.0.0 RC (Rocky)\n').strip()
PIKE = ('\nRed Hat OpenStack Platform release 12.0 Beta (Pike)\n').strip()

def test_rhosp_release():
    rocky = rhosp_release.RhospRelease(context_wrap(ROCKY))
    assert rocky.product == 'Red Hat OpenStack Platform'
    assert rocky.version == '14.0.0'
    assert rocky.code_name == 'Rocky'
    pike = rhosp_release.RhospRelease(context_wrap(PIKE))
    assert pike.product == 'Red Hat OpenStack Platform'
    assert pike.version == '12.0'
    assert pike.code_name == 'Pike'


def test_documentation():
    failed_count, tests = doctest.testmod(rhosp_release, globs={'release': rhosp_release.RhospRelease(context_wrap(ROCKY))})
    assert failed_count == 0