# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_jboss_version.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.jboss_version import JbossVersion
from insights.tests import context_wrap
import doctest
from insights.parsers import jboss_version
JBOSS_6 = ('\nRed Hat JBoss Enterprise Application Platform - Version 6.4.3.GA\n').strip()
JBOSS_7 = ('\nRed Hat JBoss Enterprise Application Platform - Version 7.1.0.Beta1\n').strip()

def test_jboss6():
    release6 = JbossVersion(context_wrap(JBOSS_6, path='/home/test/jboss/jboss-eap-6.4/version.txt'))
    assert release6.file_path == '/home/test/jboss/jboss-eap-6.4/version.txt'
    assert release6.raw == JBOSS_6
    assert release6.major == 6
    assert release6.minor == 4
    assert release6.version == '6.4.3'
    assert release6.code_name == 'GA'
    assert release6.release == 3


def test_jboss7():
    release7 = JbossVersion(context_wrap(JBOSS_7, path='/home/test/jboss/jboss-eap-7.1/version.txt'))
    assert release7.file_path == '/home/test/jboss/jboss-eap-7.1/version.txt'
    assert release7.raw == JBOSS_7
    assert release7.major == 7
    assert release7.minor == 1
    assert release7.version == '7.1.0'
    assert release7.code_name == 'Beta1'
    assert release7.release == 0


def test_jboss_version_doc_examples():
    env = {'JbossVersion': JbossVersion, 
       'jboss_version': JbossVersion(context_wrap(JBOSS_6, path='/home/test/jboss/jboss-eap-6.4/version.txt'))}
    failed, total = doctest.testmod(jboss_version, globs=env)
    assert failed == 0