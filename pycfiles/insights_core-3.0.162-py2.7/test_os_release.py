# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_os_release.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.os_release import OsRelease
from insights.tests import context_wrap
REHL_OS_RELEASE = ('\nNAME="Red Hat Enterprise Linux Server"\nVERSION="7.2 (Maipo)"\nID="rhel"\nID_LIKE="fedora"\nVERSION_ID="7.2"\nPRETTY_NAME="Employee SKU"\nANSI_COLOR="0;31"\nCPE_NAME="cpe:/o:redhat:enterprise_linux:7.2:GA:server"\nHOME_URL="https://www.redhat.com/"\nBUG_REPORT_URL="https://bugzilla.redhat.com/"\n\nREDHAT_BUGZILLA_PRODUCT="Red Hat Enterprise Linux 7"\nREDHAT_BUGZILLA_PRODUCT_VERSION=7.2\nREDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux"\nREDHAT_SUPPORT_PRODUCT_VERSION="7.2"\n').strip()
RHEVH_RHV40_OS_RELEASE = ('\nNAME="Red Hat Enterprise Linux"\nVERSION="7.3"\nVERSION_ID="7.3"\nID="rhel"\nID_LIKE="fedora"\nVARIANT="Red Hat Virtualization Host"\nVARIANT_ID="ovirt-node"\nPRETTY_NAME="Red Hat Virtualization Host 4.0 (el7.3)"\nANSI_COLOR="0;31"\nCPE_NAME="cpe:/o:redhat:enterprise_linux:7.3:GA:hypervisor"\nHOME_URL="https://www.redhat.com/"\nBUG_REPORT_URL="https://bugzilla.redhat.com/"\n\n# FIXME\n# REDHAT_BUGZILLA_PRODUCT="Red Hat Virtualization"\n# REDHAT_BUGZILLA_PRODUCT_VERSION=7.3\n# REDHAT_SUPPORT_PRODUCT="Red Hat Virtualization"\n# REDHAT_SUPPORT_PRODUCT_VERSION=7.3\n').strip()
FEDORA_OS_RELEASE = ('\nNAME=Fedora\nVERSION="24 (Server Edition)"\nID=fedora\nVERSION_ID=24\nPRETTY_NAME="Fedora 24 (Server Edition)"\nANSI_COLOR="0;34"\nCPE_NAME="cpe:/o:fedoraproject:fedora:24"\nHOME_URL="https://fedoraproject.org/"\nBUG_REPORT_URL="https://bugzilla.redhat.com/"\nREDHAT_BUGZILLA_PRODUCT="Fedora"\nREDHAT_BUGZILLA_PRODUCT_VERSION=24\nREDHAT_SUPPORT_PRODUCT="Fedora"\nREDHAT_SUPPORT_PRODUCT_VERSION=24\nPRIVACY_POLICY_URL=https://fedoraproject.org/wiki/Legal:PrivacyPolicy\nVARIANT="Server Edition"\nVARIANT_ID=server\n').strip()

def test_rhel():
    rls = OsRelease(context_wrap(REHL_OS_RELEASE))
    data = rls.data
    assert data.get('VARIANT_ID') is None
    assert data.get('VERSION') == '7.2 (Maipo)'
    return


def test_rhevh():
    rls = OsRelease(context_wrap(RHEVH_RHV40_OS_RELEASE))
    data = rls.data
    assert data.get('VARIANT_ID') == 'ovirt-node'
    assert data.get('VERSION') == '7.3'
    assert data.get('PRETTY_NAME') == 'Red Hat Virtualization Host 4.0 (el7.3)'


def test_fedora24():
    rls = OsRelease(context_wrap(FEDORA_OS_RELEASE))
    data = rls.data
    assert data.get('VARIANT_ID') == 'server'
    assert data.get('VERSION') == '24 (Server Edition)'
    assert data.get('PRETTY_NAME') == 'Fedora 24 (Server Edition)'