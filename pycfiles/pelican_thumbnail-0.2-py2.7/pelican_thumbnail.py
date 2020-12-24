# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pelican_thumbnail.py
# Compiled at: 2014-03-17 23:01:55
from pelican import signals

def youtube_thumbnail(youtube, type):
    return 'http://i1.ytimg.com/vi/%s/%s.jpg' % (youtube, type)


def add_thumbnails(generator):
    for article in generator.articles:
        if not getattr(article, 'thumbnail', None):
            if hasattr(article, 'youtube'):
                youtube_id = article.youtube
                article.thumbnail = youtube_thumbnail(youtube_id, 'hqdefault')
                article.thumbnail_hq = youtube_thumbnail(youtube_id, 'hqdefault')
                article.thumbnail_mq = youtube_thumbnail(youtube_id, 'mqdefault')
                article.thumbnail_sq = youtube_thumbnail(youtube_id, 'sqdefault')
                article.thumbnail_maxres = youtube_thumbnail(youtube_id, 'maxresdefault')
            if hasattr(article, 'niconico'):
                article.thumbnail = 'http://tn-skr4.smilevideo.jp/smile?i=%s' % article.niconico.replace('sm', '')

    return


def register():
    signals.article_generator_finalized.connect(add_thumbnails)