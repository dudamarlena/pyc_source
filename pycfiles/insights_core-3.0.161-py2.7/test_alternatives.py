# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_alternatives.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.tests import context_wrap
from insights.parsers.alternatives import AlternativesOutput, JavaAlternatives
from insights.core import ParseException
ALT_MTA = "\nmta - status is auto.\n link currently points to /usr/sbin/sendmail.postfix\n/usr/sbin/sendmail.postfix - priority 30\n slave mta-mailq: /usr/bin/mailq.postfix\n slave mta-newaliases: /usr/bin/newaliases.postfix\nCurrent `best' version is /usr/sbin/sendmail.postfix.\n"
DUPLICATED_STATUS_LINE = '\nmta - status is auto.\nNonsense line that should be ignored\nmta - status is auto.\n'
MISSING_STATUS_LINE = "\n link currently points to /usr/sbin/sendmail.postfix\n/usr/sbin/sendmail.postfix - priority 30\n slave mta-mailq: /usr/bin/mailq.postfix\n slave mta-newaliases: /usr/bin/newaliases.postfix\nCurrent `best' version is /usr/sbin/sendmail.postfix.\n"

def test_mta_alternatives():
    mtas = AlternativesOutput(context_wrap(ALT_MTA))
    assert hasattr(mtas, 'program')
    assert mtas.program == 'mta'
    assert hasattr(mtas, 'status')
    assert mtas.status == 'auto'
    assert hasattr(mtas, 'link')
    assert mtas.link == '/usr/sbin/sendmail.postfix'
    assert hasattr(mtas, 'best')
    assert mtas.best == '/usr/sbin/sendmail.postfix'
    assert hasattr(mtas, 'paths')
    assert isinstance(mtas.paths, list)
    assert len(mtas.paths) == 1
    for i in ('path', 'priority', 'slave'):
        assert i in mtas.paths[0]


def test_failure_modes():
    with pytest.raises(ParseException, match='Program line for mta'):
        alts = AlternativesOutput(context_wrap(DUPLICATED_STATUS_LINE))
        assert alts.program is None
    alts = AlternativesOutput(context_wrap(MISSING_STATUS_LINE))
    for i in (alts.program, alts.status, alts.link, alts.best):
        assert i is None

    assert alts.paths == []
    return


alter_java = ("\njava - status is auto.\n link currently points to /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java\n/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java - priority 16091\n slave ControlPanel: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/ControlPanel\n slave keytool: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/keytool\n slave policytool: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/policytool\n slave rmid: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/rmid\n slave rmiregistry: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/rmiregistry\n slave tnameserv: /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/tnameserv\n slave jre_exports: /usr/lib/jvm-exports/jre-1.6.0-ibm.x86_64\n slave jre: /usr/lib/jvm/jre-1.6.0-ibm.x86_64\n/usr/lib/jvm/jre-1.4.2-gcj/bin/java - priority 1420\n slave ControlPanel: (null)\n slave keytool: /usr/lib/jvm/jre-1.4.2-gcj/bin/keytool\n slave policytool: (null)\n slave rmid: (null)\n slave rmiregistry: /usr/lib/jvm/jre-1.4.2-gcj/bin/rmiregistry\n slave tnameserv: (null)\n slave jre_exports: /usr/lib/jvm-exports/jre-1.4.2-gcj\n slave jre: /usr/lib/jvm/jre-1.4.2-gcj\nCurrent `best' version is /usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java.\n").strip()
alter_no_java = ("\n/usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/java - priority 170079\n slave ControlPanel: (null)\n slave keytool: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/keytool\n slave orbd: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/orbd\n slave pack200: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/pack200\n slave policytool: (null)\n slave rmid: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/rmid\n slave rmiregistry: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/rmiregistry\n slave servertool: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/servertool\n slave tnameserv: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/tnameserv\n slave unpack200: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/unpack200\n slave jre_exports: /usr/lib/jvm-exports/jre-1.7.0-openjdk.x86_64\n slave jre: /usr/lib/jvm/jre-1.7.0-openjdk.x86_64\n slave java.1.gz: /usr/share/man/man1/java-java-1.7.0-openjdk.1.gz\n slave keytool.1.gz: /usr/share/man/man1/keytool-java-1.7.0-openjdk.1.gz\n slave orbd.1.gz: /usr/share/man/man1/orbd-java-1.7.0-openjdk.1.gz\n slave pack200.1.gz: /usr/share/man/man1/pack200-java-1.7.0-openjdk.1.gz\n slave rmid.1.gz: /usr/share/man/man1/rmid-java-1.7.0-openjdk.1.gz\n slave rmiregistry.1.gz: /usr/share/man/man1/rmiregistry-java-1.7.0-openjdk.1.gz\n slave servertool.1.gz: /usr/share/man/man1/servertool-java-1.7.0-openjdk.1.gz\n slave tnameserv.1.gz: /usr/share/man/man1/tnameserv-java-1.7.0-openjdk.1.gz\n slave unpack200.1.gz: /usr/share/man/man1/unpack200-java-1.7.0-openjdk.1.gz\nCurrent `best' version is /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/java.\n").strip()

def test_class_no_java():
    java = JavaAlternatives(context_wrap(alter_no_java))
    for i in (java.program, java.status, java.link, java.best):
        assert i is None

    assert java.paths == []
    return


def test_class_has_java():
    java = JavaAlternatives(context_wrap(alter_java))
    assert java.program == 'java'
    assert java.status == 'auto'
    assert java.link == '/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java'
    assert java.best == '/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java'
    assert isinstance(java.paths, list)
    assert len(java.paths) == 2
    for i in ('path', 'priority', 'slave'):
        assert i in java.paths[0]

    assert java.paths[0]['path'] == '/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/java'
    assert java.paths[0]['priority'] == 16091
    assert isinstance(java.paths[0]['slave'], dict)
    assert sorted(java.paths[0]['slave'].keys()) == sorted([
     'ControlPanel', 'keytool', 'policytool', 'rmid', 'rmiregistry',
     'tnameserv', 'jre_exports', 'jre'])
    assert java.paths[0]['slave']['ControlPanel'] == '/usr/lib/jvm/jre-1.6.0-ibm.x86_64/bin/ControlPanel'
    for i in ('path', 'priority', 'slave'):
        assert i in java.paths[1]

    assert java.paths[1]['path'] == '/usr/lib/jvm/jre-1.4.2-gcj/bin/java'
    assert java.paths[1]['priority'] == 1420
    assert isinstance(java.paths[1]['slave'], dict)
    assert sorted(java.paths[1]['slave'].keys()) == sorted([
     'ControlPanel', 'keytool', 'policytool', 'rmid', 'rmiregistry',
     'tnameserv', 'jre_exports', 'jre'])
    assert java.paths[1]['slave']['ControlPanel'] == '(null)'