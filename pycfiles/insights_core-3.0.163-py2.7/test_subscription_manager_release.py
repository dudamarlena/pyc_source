# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_subscription_manager_release.py
# Compiled at: 2020-03-25 13:10:41
from insights.parsers import SkipException, subscription_manager_release
from insights.parsers.subscription_manager_release import SubscriptionManagerReleaseShow
from insights.tests import context_wrap
import pytest, doctest
INPUT_NORMAL_1 = ('\nRelease: 7.2\n').strip()
INPUT_NORMAL_2 = ('\nRelease: 6Server\n').strip()
INPUT_NORMAL_3 = ('\nRelease: 8\n').strip()
INPUT_NOT_SET = ('\nRelease not set\n').strip()
INPUT_NG_1 = ('\nXYC\nRelease not set\n').strip()
INPUT_NG_2 = ('\nRelease: 7.x\n').strip()
INPUT_NG_3 = ('\nRelease: 7.x DUMMY\n').strip()
INPUT_NG_4 = ('\nRelease: 7x\n').strip()

def test_subscription_manager_release_show_ok():
    ret = SubscriptionManagerReleaseShow(context_wrap(INPUT_NORMAL_1))
    assert ret.set == '7.2'
    assert ret.major == 7
    assert ret.minor == 2
    ret = SubscriptionManagerReleaseShow(context_wrap(INPUT_NORMAL_2))
    assert ret.set == '6Server'
    assert ret.major == 6
    assert ret.minor is None
    ret = SubscriptionManagerReleaseShow(context_wrap(INPUT_NORMAL_3))
    assert ret.set == '8'
    assert ret.major == 8
    assert ret.minor is None
    return


def test_subscription_manager_release_show_not_set():
    ret = SubscriptionManagerReleaseShow(context_wrap(INPUT_NOT_SET))
    assert ret.set is None
    assert ret.major is None
    assert ret.minor is None
    return


def test_subscription_manager_release_show_ng():
    with pytest.raises(SkipException) as (e_info):
        SubscriptionManagerReleaseShow(context_wrap(INPUT_NG_1))
    assert 'Content takes at most 1 line (2 given).' in str(e_info.value)
    with pytest.raises(SkipException) as (e_info):
        SubscriptionManagerReleaseShow(context_wrap(INPUT_NG_2))
    assert 'Incorrect content: Release: 7.x' in str(e_info.value)
    with pytest.raises(SkipException) as (e_info):
        SubscriptionManagerReleaseShow(context_wrap(INPUT_NG_3))
    assert 'Incorrect content: Release: 7.x DUMMY' in str(e_info.value)
    with pytest.raises(SkipException) as (e_info):
        SubscriptionManagerReleaseShow(context_wrap(INPUT_NG_4))
    assert 'Incorrect content: Release: 7x' in str(e_info.value)


def test_doc_examples():
    env = {'rhsm_rel': SubscriptionManagerReleaseShow(context_wrap(INPUT_NORMAL_1))}
    failed, total = doctest.testmod(subscription_manager_release, globs=env)
    assert failed == 0