# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/theme/browser/event_format.py
# Compiled at: 2018-04-23 08:38:48
from HTMLParser import HTMLParser
from Products.Five.browser import BrowserView

class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ('').join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class EventFormat(BrowserView):

    def __call__(self, text='', wordsnumber=50):
        if not text:
            field = self.context.getField('text')
            text = field.getAccessor(self.context)()
        s = MLStripper()
        s.feed(text)
        return (' ').join(s.get_data().split()[:int(wordsnumber)]) + '...'