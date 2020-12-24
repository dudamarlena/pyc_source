# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devel/thasso/git/github/gemtools/python/test/cpu_info_tests.py
# Compiled at: 2013-04-17 04:25:01
import subprocess, gem
from testfiles import testfiles

def test_i3_compliance():
    file = testfiles['cpuinfo_i3.txt']
    of = open(file, 'r')
    assert gem._is_i3_compliant(of) == True
    of.close()


def test_core2_compliance():
    file = testfiles['cpuinfo_core2.txt']
    of = open(file, 'r')
    assert gem._is_i3_compliant(of) == False
    of.close()