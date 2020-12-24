# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_package_provides_httpd.py
# Compiled at: 2019-05-16 13:41:33
import pytest, doctest
from insights.parsers import package_provides_httpd
from insights.parsers.package_provides_httpd import PackageProvidesHttpd
from insights.tests import context_wrap
from ...parsers import SkipException
PACKAGE_COMMAND_MATCH = '\n/opt/rh/httpd24/root/usr/sbin/httpd httpd24-httpd-2.4.34-7.el7.x86_64\n'
PACKAGE_COMMAND_ERROR = '\n'
PACKAGE_COMMAND_NOT_MATCH = '\nbin/httpd file /root/bin/httpd is not owned by any package\n'

def test_package_provides_httpd_match():
    package = PackageProvidesHttpd(context_wrap(PACKAGE_COMMAND_MATCH))
    assert package.command == '/opt/rh/httpd24/root/usr/sbin/httpd'
    assert package.package == 'httpd24-httpd-2.4.34-7.el7.x86_64'


def test_package_provides_httpd_err():
    with pytest.raises(SkipException) as (pe):
        PackageProvidesHttpd(context_wrap(PACKAGE_COMMAND_ERROR))
        assert 'there is not httpd application running' in str(pe)


def test_package_provides_httpd_not_match():
    with pytest.raises(SkipException) as (pe):
        PackageProvidesHttpd(context_wrap(PACKAGE_COMMAND_NOT_MATCH))
        assert 'current running httpd command is not provided by package installed through yum or rpm' in str(pe)


def test_doc_examples():
    env = {'package': package_provides_httpd.PackageProvidesHttpd(context_wrap(PACKAGE_COMMAND_MATCH))}
    failed, _ = doctest.testmod(package_provides_httpd, globs=env)
    assert failed == 0