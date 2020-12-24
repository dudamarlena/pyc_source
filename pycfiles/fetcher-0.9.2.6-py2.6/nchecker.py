# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\nchecker\nchecker.py
# Compiled at: 2011-06-04 10:23:36
from fetcher import Fetcher, FetcherUtil
engine = Fetcher(timeout=1)
from config import patterns
import htmllib, formatter, shelve

class Store(object):

    def __init__(self):
        self.store = shelve.open('nx.db')

    def chk_new_and_save(self, key, v):
        if self.store.has_key(key):
            return False
        self.store[key] = v
        return True

    def close(self):
        self.store.close()


store = Store()

class Parser(htmllib.HTMLParser):

    def __init__(self, kw):
        htmllib.HTMLParser.__init__(self, formatter.NullFormatter())
        self.kw = kw

    def anchor_bgn(self, h, n, t):
        self.href = h

    def handle_data(self, data):
        if kw in data:
            if store.chk_new_and_save(data, self.href):
                print self.href, data


def fetch(u, kwp):
    r = engine.fetch(u)
    if r.code == 200:
        print 'fetched', u
        c = FetcherUtil.decode(r.content).lower()
        for kw in kwp:
            if kw.lower() in c:
                print u, 'matched', kw
                p = Parser(kw.lower())
                p.feed(c)
                p.close()

    else:
        print 'fetch error', r.msg


def get_stack(f):
    c = inspect.currentframe().f_back
    st = []
    while c:
        print c.f_code.co_filename
        st.append(c)
        c = c.f_back

    x = map(lambda x: x.f_code.co_name, st[:-1])
    v = st[(-1)].f_code.co_filename.rsplit(os.path.sep, 1)
    x.append(v[1])
    return ('-').join(x)


import os, inspect

def __(fun):

    def xv(*arg, **kw):
        return fun()

    return xv


@__
def test():
    print get_stack()


class x:

    def y(self):
        test()


x().y()
store.close()