# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\lib\history.py
# Compiled at: 2019-05-23 14:26:37
# Size of source mod 2**32: 1153 bytes
from collections import UserDict, namedtuple
History = namedtuple('History', ['url', 'previous', 'name'])

class HistoryDict(UserDict):

    def set_history(self, url, previous, name=None, warning=True):
        if url in self:
            if warning:
                print('warning: {} has already exist in history'.format(url))
        self[url] = History(url, previous, name)

    def get_tracer(self, url):
        tracer = []
        previous = url
        while previous:
            try:
                p = self[previous]
                previous = p.previous
            except:
                return tracer
            else:
                if p.previous:
                    tracer.insert(0, p)

        return tracer

    def get_previous(self, url, name=None):
        history = self.get(url)
        if not history:
            return
        if name is None:
            return history.previous
        for history in self.get_tracer(url):
            if history.name == name:
                return history.url

    def get_histories(self, name):
        return [h.url for h in self.values() if h.name == name]