# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rpm_v_packages.py
# Compiled at: 2020-04-16 14:56:28
import doctest
from insights.parsers import rpm_v_packages
from insights.parsers.rpm_v_packages import RpmVPackages
from insights.tests import context_wrap
TEST_RPM = '\npackage procps is not installed\n..?......  c /etc/sudoers\n..?......    /usr/bin/sudo\n..?......    /usr/bin/sudoreplay\nmissing     /var/db/sudo/lectured (Permission denied)\n'

def test_rpm_empty():
    rpm_pkgs = RpmVPackages(context_wrap([]))
    assert rpm_pkgs.packages_list == []


def test_rpm():
    line_1 = {'attributes': None, 'file': None, 'line': 'package procps is not installed', 
       'mark': None}
    line_2 = {'attributes': '..?......', 'file': '/etc/sudoers', 'line': '..?......  c /etc/sudoers', 
       'mark': 'c'}
    line_3 = {'attributes': '..?......', 'file': '/usr/bin/sudo', 'line': '..?......    /usr/bin/sudo', 
       'mark': None}
    line_4 = {'attributes': '..?......', 'file': '/usr/bin/sudoreplay', 'line': '..?......    /usr/bin/sudoreplay', 
       'mark': None}
    line_5 = {'attributes': None, 'file': None, 'line': 'missing     /var/db/sudo/lectured (Permission denied)', 
       'mark': None}
    rpm_pkgs = RpmVPackages(context_wrap(TEST_RPM))
    assert rpm_pkgs.packages_list[0] == line_1
    assert rpm_pkgs.packages_list[1] == line_2
    assert rpm_pkgs.packages_list[2] == line_3
    assert rpm_pkgs.packages_list[3] == line_4
    assert rpm_pkgs.packages_list[4] == line_5
    return


def test_doc_examples():
    env = {'rpm_v_packages': RpmVPackages(context_wrap(TEST_RPM))}
    failed, total = doctest.testmod(rpm_v_packages, globs=env)
    assert failed == 0