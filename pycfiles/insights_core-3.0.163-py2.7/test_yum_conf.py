# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_yum_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.yum_conf import YumConf
from insights.tests import context_wrap
YUM_CONF = '\n[main]\ncachedir=/var/cache/yum/$basearch/$releasever\nkeepcache=0\ndebuglevel=2\nlogfile=/var/log/yum.log\nexactarch=1\nobsoletes=1\ngpgcheck=1\nplugins=1\ninstallonly_limit=3\n\n#  This is the default, if you make this bigger yum won\'t see if the metadata\n# is newer on the remote and so you\'ll "gain" the bandwidth of not having to\n# download the new metadata and "pay" for it by yum not having correct\n# information.\n#  It is esp. important, to have correct metadata, for distributions like\n# Fedora which don\'t keep old packages around. If you don\'t like this checking\n# interupting your command line usage, it\'s much better to have something\n# manually check the metadata once an hour (yum-updatesd will do this).\n# metadata_expire=90m\n\n# PUT YOUR REPOS HERE OR IN separate files named file.repo\n# in /etc/yum.repos.d\n\n[rhel-7-server-rhn-tools-beta-debug-rpms]\nmetadata_expire = 86400\nsslclientcert = /etc/pki/entitlement/1234.pem\nbaseurl = https://cdn.redhat.com/content/beta/rhel/server/7/$basearch/rhn-tools/debug\nui_repoid_vars = basearch\nsslverify = 1\nname = RHN Tools for Red Hat Enterprise Linux 7 Server Beta (Debug RPMs)\nsslclientkey = /etc/pki/entitlement/1234-key.pem\ngpgkey = file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta,file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release\nenabled = 0\nsslcacert = /etc/rhsm/ca/redhat-uep.pem\ngpgcheck = 1\n\n[bad-repo]\ngpgkey =\n'
CONF_PATH = '/etc/yum.conf'

def test_get_yum_conf():
    yum_conf = YumConf(context_wrap(YUM_CONF, path=CONF_PATH))
    assert yum_conf.items('main') == {'plugins': '1', 
       'keepcache': '0', 
       'cachedir': '/var/cache/yum/$basearch/$releasever', 
       'exactarch': '1', 
       'obsoletes': '1', 
       'installonly_limit': '3', 
       'debuglevel': '2', 
       'gpgcheck': '1', 
       'logfile': '/var/log/yum.log'}
    assert yum_conf.items('rhel-7-server-rhn-tools-beta-debug-rpms') == {'ui_repoid_vars': 'basearch', 
       'sslverify': '1', 
       'name': 'RHN Tools for Red Hat Enterprise Linux 7 Server Beta (Debug RPMs)', 
       'sslclientkey': '/etc/pki/entitlement/1234-key.pem', 
       'enabled': '0', 
       'gpgkey': [
                'file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta',
                'file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release'], 
       'sslclientcert': '/etc/pki/entitlement/1234.pem', 
       'baseurl': [
                 'https://cdn.redhat.com/content/beta/rhel/server/7/$basearch/rhn-tools/debug'], 
       'sslcacert': '/etc/rhsm/ca/redhat-uep.pem', 
       'gpgcheck': '1', 
       'metadata_expire': '86400'}
    assert yum_conf.file_name == 'yum.conf'
    assert yum_conf.file_path == '/etc/yum.conf'