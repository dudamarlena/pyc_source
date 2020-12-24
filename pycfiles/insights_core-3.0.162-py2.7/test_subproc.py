# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_subproc.py
# Compiled at: 2019-05-16 13:41:33
import sys, pytest, shlex
from insights.util import subproc

def test_call():
    result = subproc.call('echo -n hello')
    assert result == 'hello'


def test_call_list_of_lists():
    cmd = "echo -n ' hello '"
    cmd = shlex.split(cmd)
    result = subproc.call([cmd, ['grep', '-F', 'hello']])
    assert 'hello' in result


def test_call_timeout():
    if sys.platform != 'darwin':
        with pytest.raises(subproc.CalledProcessError):
            subproc.call('sleep 3', timeout=1)