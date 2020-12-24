# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pexpect/tests/adhoc.py
# Compiled at: 2011-11-02 15:34:09
import pexpect, time
p = pexpect.spawn('./a.out')
print(p.exitstatus)
p.expect(pexpect.EOF)
print(p.before)
time.sleep(1)
print('exitstatus:', p.exitstatus)
print('isalive', p.isalive())
print('exitstatus', p.exitstatus)
print('isalive', p.isalive())
print('exitstatus', p.exitstatus)