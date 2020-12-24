# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mark/devel/grandma/tests/test_jenny.py
# Compiled at: 2011-09-30 08:52:36
from grandma import jenny_wrapper
from nose.tools import assert_equals

def test_jenny():
    """Test that the interface of the jenny_wrapper works as expected."""
    dims = {'os': [
            'win32', 'linux', 'solaris'], 
       'cmd': [
             'ls', 'rm', 'cp', 'del', 'pwd'], 
       'prot': [
              'telnet', 'ssh', 'local-machine']}
    incompats = [
     {'os': [
             'win32'], 
        'cmd': [
              'ls', 'rm', 'cp']}]
    reqs = [
     [
      'del', 'win32']]
    tests = jenny_wrapper.create_test_cases(dims, 2, incompats=incompats, reqs=reqs)
    assert_equals(len(list(tests)), 16)