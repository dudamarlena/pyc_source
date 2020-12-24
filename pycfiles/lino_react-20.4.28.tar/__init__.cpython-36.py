# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luc/work/react/lino_react/react/__init__.py
# Compiled at: 2020-04-06 08:14:06
# Size of source mod 2**32: 3350 bytes
"""
A user interface for Lino applications that uses FaceBooks React JS framework.

.. autosummary::
   :toctree:

    views
    renderer
    models
"""
from lino.api.ad import Plugin

class Plugin(Plugin):
    ui_handle_attr_name = 'react_handle'
    needs_plugins = [
     'lino.modlib.jinja']
    url_prefix = 'react'
    media_name = 'react'

    def on_ui_init(self, kernel):
        from .renderer import Renderer
        self.renderer = Renderer(self)
        kernel.extjs_renderer = self.renderer

    def get_patterns(self):
        from django.conf.urls import url
        from django.urls import path
        from . import views
        rx = '^'
        self.renderer.build_site_cache()
        urls = [
         url(rx + '$', views.App.as_view()),
         url(rx + 'user/settings', views.UserSettings.as_view()),
         url(rx + 'auth$', views.Authenticate.as_view()),
         url(rx + 'null/', views.Null.as_view()),
         url(rx + 'api/main_html$', views.MainHtml.as_view()),
         path('dashboard/<int:index>', views.DashboardItem.as_view()),
         url(rx + 'restful/(?P<app_label>\\w+)/(?P<actor>\\w+)$', views.ApiList.as_view()),
         url(rx + 'restful/(?P<app_label>\\w+)/(?P<actor>\\w+)/(?P<pk>.+)$', views.ApiElement.as_view()),
         url(rx + 'api/(?P<app_label>\\w+)/(?P<actor>\\w+)$', views.ApiList.as_view()),
         url(rx + 'api/(?P<app_label>\\w+)/(?P<actor>\\w+)/(?P<pk>[^/]+)$', views.ApiElement.as_view()),
         url(rx + 'api/(?P<app_label>\\w+)/(?P<actor>\\w+)/(?P<pk>[^/]+)/(?P<field>\\w+)/suggestions$', views.Suggestions.as_view()),
         url(rx + 'choices/(?P<app_label>\\w+)/(?P<rptname>\\w+)$', views.Choices.as_view()),
         url(rx + 'choices/(?P<app_label>\\w+)/(?P<rptname>\\w+)/(?P<fldname>\\w+)$', views.Choices.as_view()),
         url(rx + 'apchoices/(?P<app_label>\\w+)/(?P<actor>\\w+)/(?P<an>\\w+)/(?P<field>\\w+)$', views.ActionParamChoices.as_view()),
         url(rx + 'choicelists/', views.ChoiceListModel.as_view())]
        return urls

    def get_detail_url(self, ar, actor, pk, *args, **kw):
        return (self.build_plain_url)(
 '#',
 'api',
 actor.actor_id.replace('.', '/'),
 str(pk), *args, **kw)

    def get_used_libs(self, html=False):
        if html is not None:
            yield ('React', '16.6', 'https://reactjs.org/')