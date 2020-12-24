# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/lib/NewsFeed.py
# Compiled at: 2011-12-23 04:19:50
from datetime import datetime
import uuid

class FeedEntry(object):
    Title = ''
    Link = ''
    Guid = uuid.uuid4()
    TimeUpdated = datetime.now()
    Summary = ''


class NewsFeed(object):
    Title = ''
    Subtitle = ''
    Description = ''
    FeedUrl = ''
    PageUrl = ''
    Guid = uuid.uuid4()
    TimeUpdated = datetime.now()
    Author = None
    Entries = []

    def CreateEntry(self, title, link, guid, summary):
        res = FeedEntry(Title=title, Link=link, Guid=guid, Summary=summary)
        self.Entries.append(res)
        return res