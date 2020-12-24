# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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