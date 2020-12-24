# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/show/urls.py
# Compiled at: 2013-09-27 03:40:37
from django.conf.urls.defaults import patterns, url
from show.view_modifiers import RadioShowDefaultViewModifier
urlpatterns = patterns('', url('^schedule/$', 'show.views.schedule', {}, name='show-schedule'), url('^current/radio/$', 'show.views.current_radio', {}, name='show-current-radio'), url('^radio/(?P<slug>[\\w-]+)/$', 'jmbo.views.object_detail', {'template_name': 'show/show_detail.html', 'view_modifier': RadioShowDefaultViewModifier}, name='radioshow_object_detail'), url('^radio/(?P<slug>[\\w-]+)/about/$', 'jmbo.views.object_detail', {'view_modifier': RadioShowDefaultViewModifier, 
   'extra_context': {'is_about': True}}, name='radio-show-about'), url('^radio/(?P<slug>[\\w-]+)/polls/$', 'jmbo.views.object_detail', {'view_modifier': RadioShowDefaultViewModifier, 
   'extra_context': {'is_polls': True}}, name='radio-show-polls'), url('^radio/(?P<slug>[\\w-]+)/galleries/$', 'jmbo.views.object_detail', {'view_modifier': RadioShowDefaultViewModifier, 
   'extra_context': {'is_galleries': True}}, name='radio-show-galleries'), url('^contributor/(?P<slug>[\\w-]+)/$', 'jmbo.views.object_detail', {}, name='contributor_object_detail'))