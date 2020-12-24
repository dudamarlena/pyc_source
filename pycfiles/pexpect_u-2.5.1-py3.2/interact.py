# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pexpect/tests/interact.py
# Compiled at: 2011-10-29 16:59:39
import pexpect
p = pexpect.spawn('cat')
p.interact()