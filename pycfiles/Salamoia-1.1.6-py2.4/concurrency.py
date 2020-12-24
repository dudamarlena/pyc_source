# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/concurrency.py
# Compiled at: 2007-12-02 16:26:58
import threading

class ThreadLocalClass(type):
    """
    >>> from threading import Thread

    >>> class Test(object):
    ...   __metaclass__ = ThreadLocalClass
    
    >>> def threadTest(arg):
    ...   Test.classThreadLocal.test = arg

    >>> Test.classThreadLocal.test = 10
    >>> t = Thread(target=threadTest, args=(20,))
    >>> t.start()
    >>> t.join()

    >>> Test.classThreadLocal.test
    10
    """
    __module__ = __name__

    def __init__(cls, name, bases, dict):
        super(ThreadLocalClass, cls).__init__(name, bases, dict)
        cls.classThreadLocal = threading.local()