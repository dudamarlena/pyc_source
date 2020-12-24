# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/cms_apps.py
# Compiled at: 2017-07-21 05:10:28
# Size of source mod 2**32: 288 bytes
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext as _

class ArticleApp(CMSApp):
    name = _('Articles')
    urls = ['cmsplugin_articles_ai.article_urls']


apphook_pool.register(ArticleApp)