# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\ThreadLock\tests.py
# Compiled at: 2010-03-31 15:40:02
"""ThreadLock tests

>>> lock = ThreadLock.allocate_lock()

>>> twoshouldstart = threading.Event()

>>> n = 0
>>> readbytwo = None

>>> def one():
...     global n
...     lock.acquire()
...     twoshouldstart.set()
...     for i in range(10):
...         time.sleep(.001)
...         lock.acquire()
...         n += 1
... 
...     for i in range(10):
...         time.sleep(.001)
...         lock.release()
... 
...     lock.release()

>>> def two():
...     global readbytwo
...     twoshouldstart.wait()
...     lock.acquire()
...     readbytwo = n
...     lock.release()

>>> ttwo = threading.Thread(target=two)
>>> ttwo.start()
>>> time.sleep(0.001)
>>> tone = threading.Thread(target=one)
>>> tone.start()
>>> tone.join()
>>> ttwo.join()
>>> readbytwo
10

$Id: tests.py,v 1.2 2003/11/28 16:46:39 jim Exp $
"""
import ThreadLock, threading, time, unittest
from doctest import DocTestSuite

def test_suite():
    return unittest.TestSuite((
     DocTestSuite(),))


if __name__ == '__main__':
    unittest.main()