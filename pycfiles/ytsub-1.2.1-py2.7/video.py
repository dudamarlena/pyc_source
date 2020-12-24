# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ytsub/video.py
# Compiled at: 2013-01-05 10:41:32
from functools import total_ordering
from datetime import datetime
from datetime import timedelta

@total_ordering
class Vid:

    def __init__(self, author_name, playlist_item_video):
        self.id = playlist_item_video['snippet']['resourceId']['videoId']
        self.title = playlist_item_video['snippet']['title']
        self.date = datetime.strptime(playlist_item_video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.000Z')
        self.author = author_name

    def __str__(self):
        return 'Vid{id:' + self.id + ', date:' + self.date.isoformat() + ', title:' + self.title + ', author:' + self.author + '}'

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.date < other.date

    def __hash__(self):
        return hash(self.id)