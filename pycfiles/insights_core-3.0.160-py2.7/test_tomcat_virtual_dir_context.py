# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_tomcat_virtual_dir_context.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.parsers.tomcat_virtual_dir_context import TomcatVirtualDirContextFallback, TomcatVirtualDirContextTargeted
from insights.tests import context_wrap
from insights.parsers import SkipException
FOUND_1 = ('\n/usr/share/tomcat/conf/server.xml:    <Resources className="org.apache.naming.resources.VirtualDirContext"\n').strip()
FOUND_2 = ('\n/usr/share/tomcat/conf/server.xml:    <Resources className="org.apache.naming.resources.VirtualDirContext"\n/usr/share/tomcat6/webapps/whatever/META-INF/context.xml:className="org.apache.naming.resources.VirtualDirContext"\n').strip()
FOUND_3 = ('\n/usr/share/tomcat/conf/server.xml:    <Resources className="org.apache.naming.resources.VirtualDirContext"\n/usr/share/tomcat/conf/server.xml:"VirtualDirContext"\n/usr/share/tomcat6/webapps/whatever/META-INF/context.xml:className="org.apache.naming.resources.VirtualDirContext"\n').strip()
NOT_FOUND = ('\n').strip()
ERRORS_2 = '\ngarbage garbage\n'

def test_tomcat_virtual_dir_context_found():
    for parser in [TomcatVirtualDirContextFallback, TomcatVirtualDirContextTargeted]:
        tomcat_virtual_dir_context = parser(context_wrap(FOUND_1))
        assert len(tomcat_virtual_dir_context.data) == 1
        assert tomcat_virtual_dir_context.data == {'/usr/share/tomcat/conf/server.xml': [
                                               '    <Resources className="org.apache.naming.resources.VirtualDirContext"']}
        tomcat_virtual_dir_context = parser(context_wrap(FOUND_2))
        assert len(tomcat_virtual_dir_context.data) == 2
        assert tomcat_virtual_dir_context.data == {'/usr/share/tomcat/conf/server.xml': [
                                               '    <Resources className="org.apache.naming.resources.VirtualDirContext"'], 
           '/usr/share/tomcat6/webapps/whatever/META-INF/context.xml': [
                                                                      'className="org.apache.naming.resources.VirtualDirContext"']}
        tomcat_virtual_dir_context = parser(context_wrap(FOUND_3))
        assert len(tomcat_virtual_dir_context.data) == 2
        assert tomcat_virtual_dir_context.data == {'/usr/share/tomcat/conf/server.xml': [
                                               '    <Resources className="org.apache.naming.resources.VirtualDirContext"',
                                               '"VirtualDirContext"'], 
           '/usr/share/tomcat6/webapps/whatever/META-INF/context.xml': [
                                                                      'className="org.apache.naming.resources.VirtualDirContext"']}


def test_tomcat_virtual_dir_context_not_found():
    for parser in [TomcatVirtualDirContextFallback, TomcatVirtualDirContextTargeted]:
        with pytest.raises(SkipException) as (excinfo):
            parser(context_wrap(NOT_FOUND))
            assert 'VirtualDirContext not used.' in str(excinfo.value)


def test_tomcat_virtual_dir_context_exceptions():
    for parser in [TomcatVirtualDirContextFallback, TomcatVirtualDirContextTargeted]:
        with pytest.raises(SkipException) as (excinfo):
            parser(context_wrap(ERRORS_2))
            assert 'VirtualDirContext not used.' in str(excinfo.value)