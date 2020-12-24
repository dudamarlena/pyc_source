# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/feed2twitter/readrss.py
# Compiled at: 2009-01-05 09:21:56
import feedparser, pickle, time, os.path
from os import mkdir
import md5

class parse(object):
    __module__ = __name__

    def __init__(self, feed_url):
        self.feed_url = feed_url
        self.feed = feedparser.parse(feed_url)

    def getStampFileName(self):
        self.md5name = md5.md5(self.feed_url).hexdigest()
        self.directory = os.path.expanduser('~/.feed2twitter/')
        self.filename = self.directory + self.md5name

    def updateLastRead(self, item=None):
        self.getStampFileName()
        if not os.path.exists(self.directory):
            mkdir(self.directory)
        output = open(self.filename, 'wb')
        key = 'updated_parsed'
        if not item:
            if 'published_parsed' in self.feed['items'][0]:
                key = 'published_parsed'
            pickle.dump(self.feed['items'][0][key], output)
        else:
            if 'published_parsed' in item:
                key = 'published_parsed'
            else:
                key = 'updated_parsed'
            pickle.dump(item[key], output)
        output.close()

    def getlastRead(self):
        self.getStampFileName()
        try:
            pick = open(self.filename, 'rb')
        except IOError:
            return False

        try:
            last_read = pickle.load(pick)
        except EOFError:
            return False

        return last_read