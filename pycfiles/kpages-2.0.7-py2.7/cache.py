# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/kpages/cache.py
# Compiled at: 2019-01-22 20:15:58
import time, threading
HB = 10

class Cache(object):
    m = {}

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Cache, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
            t = threading.Thread(target=cls._instance.timer)
            t.setDaemon(True)
            t.start()
        return cls._instance

    def setex(self, k, v, ex=None):
        """
            k, v, ex = expire
        """
        if ex:
            ex = time.time() + ex
        self.m[k] = (
         v, ex)

    def get(self, k):
        if self.m.has_key(k):
            return self.m.get(k)[0]
        else:
            return

    def timer(self):
        while True:
            now = time.time()
            for k, v in self.m.items():
                if v[1] and now > v[1]:
                    self.m.pop(k, None)

            time.sleep(HB)

        return


if __name__ == '__main__':
    Cache().setex(1, 2, 6)
    for i in range(10):
        print Cache().get(1)
        time.sleep(1)

    import tornado.ioloop
    tornado.ioloop.IOLoop.instance().start()