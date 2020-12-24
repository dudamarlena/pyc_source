# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/harold/cache/langoliers.py
# Compiled at: 2006-08-02 05:57:50
import threading, time, weakref
from harold.lib import synchronized

class Langoliers(threading.Thread):
    """ Thread to remove invalid cache entries

    """
    __module__ = __name__
    caches = weakref.WeakKeyDictionary()
    snooze = 3

    def __init__(self):
        super(Langoliers, self).__init__()
        self.setDaemon(True)
        self.__lock = threading.RLock()

    def run(self):
        lock = self.__lock
        while True:
            time.sleep(self.snooze)
            lock.acquire()
            try:
                for cache in self.caches.keys():
                    for key in cache.keys():
                        try:
                            entry = cache[key]
                        except (KeyError,):
                            pass
                        else:
                            if not entry.valid():
                                cache.counter_incr('cleared', key[0])
                                del cache[key]

            finally:
                lock.release()

    @classmethod
    @synchronized
    def register(cls, cache):
        """ adds cache to mapping of caches to sweep and prune

        @param cache cache instance to prune
        @return None
        """
        cls.caches[cache] = True


langoliers = Langoliers()
langoliers.start()