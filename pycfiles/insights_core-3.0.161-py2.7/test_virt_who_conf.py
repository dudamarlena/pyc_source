# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_virt_who_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.virt_who_conf import VirtWhoConf
from insights.parsers import SkipException
from insights.tests import context_wrap
import pytest
VWHO_CONF = "\n## This is a template for virt-who global configuration files. Please see\n## virt-who-config(5) manual page for detailed information.\n##\n## virt-who checks /etc/virt-who.conf for sections 'global' and 'defaults'.\n## The sections and their values are explained below.\n## NOTE: These sections retain their special meaning and function only when present in /etc/virt-who.conf\n##\n## You can uncomment and fill following template or create new file with\n## similar content.\n\n#Terse version of the general config template:\n[global]\n\ninterval=3600\n#reporter_id=\ndebug=False\noneshot=False\n#log_per_config=False\n#log_dir=\n#log_file=\n#configs=\n\n[defaults]\nowner=Satellite\nenv=Satellite\nhypervisor_id=ID1\n"

def test_virt_who_conf_empty():
    with pytest.raises(SkipException):
        assert VirtWhoConf(context_wrap('')) is None
    return


def test_virt_who_conf():
    vwho_conf = VirtWhoConf(context_wrap(VWHO_CONF))
    assert vwho_conf.has_option('global', 'debug')
    assert vwho_conf.get('global', 'oneshot') == 'False'
    assert vwho_conf.getboolean('global', 'oneshot') is False
    assert vwho_conf.get('global', 'interval') == '3600'
    assert vwho_conf.getint('global', 'interval') == 3600
    assert vwho_conf.items('defaults') == {'owner': 'Satellite', 
       'env': 'Satellite', 
       'hypervisor_id': 'ID1'}