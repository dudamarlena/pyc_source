# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/inqbus/ocf/generic/test.py
# Compiled at: 2011-10-30 15:28:20
from os import kill
from mock import Mock, sentinel, patch
mock = Mock(return_value=2)

@patch('kill', mock)
def test():
    return kill(1084, 0)


ret = test()
mock.assert_called_with(1084, 0)
assert ret == 3, 'incorrect return value'
print ret