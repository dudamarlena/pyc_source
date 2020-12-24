# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_qpidd_conf.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import qpidd_conf
from insights.parsers.qpidd_conf import QpiddConf
from insights.tests import context_wrap
QPIDD_CONF = '\n# Configuration file for qpidd. Entries are of the form:\n# name=value\n#\n# (Note: no spaces on either side of \'=\'). Using default settings:\n# "qpidd --help" or "man qpidd" for more details.\n#cluster-mechanism=ANONYMOUS\nlog-enable=error+\nlog-to-syslog=yes\nauth=no\nrequire-encryption=yes\nssl-require-client-authentication=yes\nssl-port=5671\nssl-cert-db=/etc/pki/katello/nssdb\nssl-cert-password-file=/etc/pki/katello/nssdb/nss_db_password-file\nssl-cert-name=broker\n\ninterface=lo\n'

def test_qpidd_conf():
    qpidd_conf = QpiddConf(context_wrap(QPIDD_CONF))
    assert qpidd_conf['auth'] == 'no'
    assert ('require-encryption' in qpidd_conf) is True


def test_qpidd_conf_doc_examples():
    env = {'qpidd_conf': QpiddConf(context_wrap(QPIDD_CONF))}
    failed, total = doctest.testmod(qpidd_conf, globs=env)
    assert failed == 0