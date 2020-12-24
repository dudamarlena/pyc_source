# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_checkin_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import checkin_conf
from insights.parsers.checkin_conf import CheckinConf
from insights.tests import context_wrap
from . import ic_testmod
CONFIG = ('\n[logging]\nconfig = /etc/splice/logging/basic.cfg\n\n# this is used only for single-spacewalk deployments\n[spacewalk]\n# Spacewalk/Satellite server to use for syncing data.\nhost=\n# Path to SSH private key used to connect to spacewalk host.\nssh_key_path=\nlogin=swreport\n\n# these are used for multi-spacewalk deployments\n# [spacewalk_one]\n# type = ssh\n# # Spacewalk/Satellite server to use for syncing data.\n# host=\n# # Path to SSH private key used to connect to spacewalk host.\n# ssh_key_path=\n# login=swreport\n#\n# [spacewalk_two]\n# type = file\n# # Path to directory containing report output\n# path = /path/to/output\n\n[katello]\nhostname=localhost\nport=443\nproto=https\napi_url=/sam\nadmin_user=admin\nadmin_pass=admin\n#autoentitle_systems = False\n#flatten_orgs = False\n').strip()

def test_checkin_conf():
    result = CheckinConf(context_wrap(CONFIG))
    assert list(result.sections()) == ['logging', 'spacewalk', 'katello']
    assert result.get('spacewalk', 'host') == ''


def test_checkin_conf_doc_examples():
    env = {'CheckinConf': CheckinConf, 
       'checkin_conf': CheckinConf(context_wrap(CONFIG))}
    failed, total = ic_testmod(checkin_conf, globs=env)
    assert failed == 0