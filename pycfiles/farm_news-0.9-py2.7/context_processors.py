# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/news/context_processors.py
# Compiled at: 2014-03-27 11:03:35
from django.conf import settings
from .models import Article

def latest_articles(request):
    num_latest_articles = hasattr(settings, 'NUM_LATEST_ARTICLES') and settings.NUM_LATEST_ARTICLES or 3
    objs = Article.objects.published().order_by('-publish_on')[:num_latest_articles]
    return {'latest_articles': objs}