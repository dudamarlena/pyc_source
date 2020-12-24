# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_nsswitch_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.nsswitch_conf import NSSwitchConf
from insights.tests import context_wrap
NSSWITCH = '\n# To use db, put the "db" in front of "files" for entries you want to be\n# looked up first in the databases\n#\n# Example:\n#passwd:    db files nisplus nis\n#shadow:    db files nisplus nis\n#group:     db files nisplus nis\n\npasswd:     files sss\nshadow:     files sss\ngroup:      files sss\n#initgroups: files\n\n#hosts:     db files nisplus nis dns\nhosts:      files dns myhostname\n\n# Example - obey only what nisplus tells us...\n#services:   nisplus [NOTFOUND=return] files\n#networks:   nisplus [NOTFOUND=return] files\n#protocols:  nisplus [NOTFOUND=return] files\n#rpc:        nisplus [NOTFOUND=return] files\n#ethers:     nisplus [NOTFOUND=return] files\n#netmasks:   nisplus [NOTFOUND=return] files\n\nbootparams: nisplus [NOTFOUND=return] files\n\n'
NSSWITCH_ERROR = '\npasswd      files sss DNS\nGROUP:      Files SSS\n'

def test_nsswitch_conf():
    nss = NSSwitchConf(context_wrap(NSSWITCH, path='/etc/nsswitch.conf'))
    assert hasattr(nss, 'data')
    assert hasattr(nss, 'errors')
    assert hasattr(nss, 'sources')
    assert sorted(nss.data.keys()) == sorted([
     'passwd', 'shadow', 'group', 'hosts', 'bootparams'])
    assert nss.errors == []
    assert nss.sources == set([
     'files', 'sss', 'dns', 'myhostname', 'nisplus', '[notfound=return]'])
    assert 'passwd' in nss
    assert 'initgroups' not in nss
    assert nss['passwd'] == 'files sss'
    assert nss['bootparams'] == 'nisplus [notfound=return] files'


def test_nsswitch_errors():
    nss = NSSwitchConf(context_wrap(NSSWITCH_ERROR, path='/etc/nsswitch.conf'))
    assert hasattr(nss, 'data')
    assert hasattr(nss, 'errors')
    assert hasattr(nss, 'sources')
    assert nss.data == {'group': 'files sss'}
    assert nss.errors == [
     'passwd      files sss DNS']
    assert nss.sources == set(['files', 'sss'])