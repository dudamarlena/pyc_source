# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_rhsm_release.py
# Compiled at: 2020-03-25 13:10:41
import doctest, insights.combiners.rhsm_release as rhsm_release_module
from insights.combiners.rhsm_release import RhsmRelease
from insights.parsers.rhsm_releasever import RhsmReleaseVer
from insights.parsers.subscription_manager_release import SubscriptionManagerReleaseShow
from insights.tests import context_wrap
RHSM_RELEASE = ('\n{"releaseVer": "7.6"}\n').strip()
SUBSCRIPTION_MANAGER_RELEASE = ('\nRelease: 7.2\n').strip()
SM_PARSER = SubscriptionManagerReleaseShow(context_wrap(SUBSCRIPTION_MANAGER_RELEASE))
RHSM_PARSER = RhsmReleaseVer(context_wrap(RHSM_RELEASE))

def test_with_rhsm():
    rhsm_release = RhsmRelease(RHSM_PARSER, None)
    assert rhsm_release.set == '7.6'
    assert rhsm_release.major == 7
    assert rhsm_release.minor == 6
    return


def test_with_sub_mgr():
    rhsm_release = RhsmRelease(None, SM_PARSER)
    assert rhsm_release.set == '7.2'
    assert rhsm_release.major == 7
    assert rhsm_release.minor == 2
    return


def test_with_both():
    rhsm_release = RhsmRelease(RHSM_PARSER, SM_PARSER)
    assert rhsm_release.set == '7.6'
    assert rhsm_release.major == 7
    assert rhsm_release.minor == 6


def test_doc_examples():
    env = {'rhsm_release': RhsmRelease(RHSM_PARSER, None)}
    failed, total = doctest.testmod(rhsm_release_module, globs=env)
    assert failed == 0
    return