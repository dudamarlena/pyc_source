# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_redhat_release.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.redhat_release import RedhatRelease
from insights.tests import context_wrap
REDHAT_RELEASE1 = ('\nRed Hat Enterprise Linux Server release 6.7 (Santiago)\n').strip()
REDHAT_RELEASE2 = ('\nRed Hat Enterprise Linux Server release 7.2 (Maipo)\n').strip()
REDHAT_RELEASE3 = ('\nRed Hat Enterprise Linux release 7.5-0.14\n').strip()
RHVH_RHV40 = ('\nRed Hat Enterprise Linux release 7.3\n').strip()
RHEVH_RHEV35 = ('\nRed Hat Enterprise Virtualization Hypervisor release 6.7 (20160219.0.el6ev)\n').strip()
FEDORA = ('\nFedora release 23 (Twenty Three)\n').strip()

def test_rhe6():
    release = RedhatRelease(context_wrap(REDHAT_RELEASE1))
    assert release.raw == REDHAT_RELEASE1
    assert release.major == 6
    assert release.minor == 7
    assert release.version == '6.7'
    assert release.is_rhel
    assert release.product == 'Red Hat Enterprise Linux Server'


def test_rhe7():
    release = RedhatRelease(context_wrap(REDHAT_RELEASE2))
    assert release.raw == REDHAT_RELEASE2
    assert release.major == 7
    assert release.minor == 2
    assert release.version == '7.2'
    assert release.is_rhel
    assert release.product == 'Red Hat Enterprise Linux Server'


def test_rhe75_0_14():
    release = RedhatRelease(context_wrap(REDHAT_RELEASE3))
    assert release.raw == REDHAT_RELEASE3
    assert release.major == 7
    assert release.minor == 5
    assert release.version == '7.5-0.14'
    assert release.is_rhel
    assert release.product == 'Red Hat Enterprise Linux'


def test_rhevh35():
    release = RedhatRelease(context_wrap(RHEVH_RHEV35))
    assert release.raw == RHEVH_RHEV35
    assert release.major == 6
    assert release.minor == 7
    assert release.version == '6.7'
    assert not release.is_rhel
    assert release.product == 'Red Hat Enterprise Virtualization Hypervisor'


def test_rhvh40():
    release = RedhatRelease(context_wrap(RHVH_RHV40))
    assert release.raw == RHVH_RHV40
    assert release.major == 7
    assert release.minor == 3
    assert release.version == '7.3'
    assert release.is_rhel
    assert release.product == 'Red Hat Enterprise Linux'


def test_fedora23():
    release = RedhatRelease(context_wrap(FEDORA))
    assert release.raw == FEDORA
    assert release.major == 23
    assert release.minor is None
    assert release.version == '23'
    assert not release.is_rhel
    assert release.product == 'Fedora'
    return