# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/common/threads/rw_lock.py
# Compiled at: 2011-09-28 13:50:09
import threading
__author__ = 'Mateusz Kobos'

class RWLock:
    """Synchronization object used in a solution of so-called second 
        readers-writers problem. In this problem, many readers can simultaneously 
        access a share, and a writer has an exclusive access to this share.
        Additionally, the following constraints should be met: 
                - no reader should be kept waiting if the share is currently opened for 
                        reading unless a writer is also waiting for the share, 
                - no writer should be kept waiting for the share longer than absolutely 
                        necessary. 
        
        The implementation is based on [1, secs. 4.2.2, 4.2.6, 4.2.7] 
        with a modification -- adding an additional lock (C{self.__readers_queue})
        -- in accordance with [2].
                
        Sources:
                1. A.B. Downey: "The little book of semaphores", Version 2.1.5, 2008
                2. P.J. Courtois, F. Heymans, D.L. Parnas:
                        "Concurrent Control with 'Readers' and 'Writers'", 
                        Communications of the ACM, 1971 (via [3])
                3. http://en.wikipedia.org/wiki/Readers-writers_problem
        """

    def __init__(self):
        self.__read_switch = _LightSwitch()
        self.__write_switch = _LightSwitch()
        self.__no_readers = threading.Lock()
        self.__no_writers = threading.Lock()
        self.__readers_queue = threading.Lock()

    def reader_acquire(self):
        self.__readers_queue.acquire()
        self.__no_readers.acquire()
        self.__read_switch.acquire(self.__no_writers)
        self.__no_readers.release()
        self.__readers_queue.release()

    def reader_release(self):
        self.__read_switch.release(self.__no_writers)

    def writer_acquire(self):
        self.__write_switch.acquire(self.__no_readers)
        self.__no_writers.acquire()

    def writer_release(self):
        self.__no_writers.release()
        self.__write_switch.release(self.__no_readers)


class _LightSwitch:
    """An auxiliary "light switch"-like object. The first thread turns on the 
        "switch", the last one turns it off (see [1, sec. 4.2.2] for details)."""

    def __init__(self):
        self.__counter = 0
        self.__mutex = threading.Lock()

    def acquire(self, lock):
        self.__mutex.acquire()
        self.__counter += 1
        if self.__counter == 1:
            lock.acquire()
        self.__mutex.release()

    def release(self, lock):
        self.__mutex.acquire()
        self.__counter -= 1
        if self.__counter == 0:
            lock.release()
        self.__mutex.release()