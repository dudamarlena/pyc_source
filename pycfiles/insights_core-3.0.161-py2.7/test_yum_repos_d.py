# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_yum_repos_d.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.yum_repos_d import YumReposD
from insights.tests import context_wrap
REPOINFO = '\n[rhel-source]\nname=Red Hat Enterprise Linux $releasever - $basearch - Source\nbaseurl=ftp://ftp.redhat.com/pub/redhat/linux/enterprise/$releasever/en/os/SRPMS/\nenabled=0\ngpgcheck=1\ngpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release\n file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release1\n\n[rhel-source-beta]\nname=Red Hat Enterprise Linux $releasever Beta - $basearch - Source\nbaseurl=ftp://ftp.redhat.com/pub/redhat/linux/beta/$releasever/en/os/SRPMS/,ftp://ftp2.redhat.com/pub/redhat/linux/beta/$releasever/en/os/SRPMS/\nenabled=0\ngpgcheck=1\n    0 # This should be ignored\ngpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta,file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release\n'
REPOPATH = '/etc/yum.repos.d/rhel-source.repo'

def test_yum_repos_d():
    repos_info = YumReposD(context_wrap(REPOINFO, path=REPOPATH))
    assert repos_info.get('rhel-source') == {'name': 'Red Hat Enterprise Linux $releasever - $basearch - Source', 
       'baseurl': [
                 'ftp://ftp.redhat.com/pub/redhat/linux/enterprise/$releasever/en/os/SRPMS/'], 
       'enabled': '0', 
       'gpgcheck': '1', 
       'gpgkey': [
                'file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release',
                'file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release1']}
    assert repos_info.get('rhel-source-beta') == {'name': 'Red Hat Enterprise Linux $releasever Beta - $basearch - Source', 
       'baseurl': [
                 'ftp://ftp.redhat.com/pub/redhat/linux/beta/$releasever/en/os/SRPMS/',
                 'ftp://ftp2.redhat.com/pub/redhat/linux/beta/$releasever/en/os/SRPMS/'], 
       'enabled': '0', 
       'gpgcheck': '1', 
       'gpgkey': [
                'file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta',
                'file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release']}
    assert repos_info.file_name == 'rhel-source.repo'
    assert repos_info.file_path == REPOPATH
    assert sorted(list(repos_info)) == sorted(['rhel-source', 'rhel-source-beta'])