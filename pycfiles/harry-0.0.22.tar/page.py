# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zacharymunro-cape/Documents/har2jmx/har2jmx/harpy/harpy/page.py
# Compiled at: 2012-06-19 11:02:04


class Page(object):

    def __init__(self, j):
        self.raw = j
        self.started_date_time = self.raw['startedDateTime']
        self.id = self.raw['id']
        self.title = self.raw['title']
        self._timings = self.raw['pageTimings']
        if 'comment' in self.raw:
            self.comment = self.raw['comment']
        else:
            self.comment = ''

    @property
    def timings(self):
        if 'onContentLoad' in self._timings:
            on_content_load = self._timings['onContentLoad']
        else:
            on_content_load = None
        if 'onLoad' in self._timings:
            on_load = self._timings['onLoad']
        else:
            on_load = None
        if 'comment' in self._timings:
            comment = self._timings['comment']
        else:
            comment = ''
        return (on_content_load, on_load, comment)