# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bfschott/Source/cmsplugin-newsplus/cmsplugin_newsplus/cms_plugins.py
# Compiled at: 2017-12-04 14:10:18
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cmsplugin_newsplus.models import LatestNewsPlugin, News
from cmsplugin_newsplus import settings

class CMSLatestNewsPlugin(CMSPluginBase):
    """
        Plugin class for the latest news
    """
    model = LatestNewsPlugin
    name = _('Latest news')
    render_template = 'cmsplugin_newsplus/latest_news.html'

    def render(self, context, instance, placeholder):
        """
            Render the latest news
        """
        latest = News.published.all()[:instance.limit]
        context.update({'instance': instance, 
           'latest': latest, 
           'placeholder': placeholder})
        return context


if not settings.DISABLE_LATEST_NEWS_PLUGIN:
    plugin_pool.register_plugin(CMSLatestNewsPlugin)