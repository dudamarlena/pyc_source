# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/projects/wholebaked-site/venv/lib/python2.7/site-packages/richtext_blog/custom_dashboard.py
# Compiled at: 2012-04-15 00:30:08
"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = '{{ project }}.{{ file }}.CustomIndexDashboard'
"""
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        self.children.append(modules.Group(_('Group: Administration & Applications'), column=1, collapsible=True, children=[
         modules.AppList(_('Administration'), column=1, collapsible=False, models=('django.contrib.*', )),
         modules.AppList(_('Applications'), column=1, css_classes=('', ), exclude=('django.contrib.*', ))]))
        self.children.append(modules.LinkList(_('Media Management'), column=2, children=[
         {'title': _('FileBrowser'), 
            'url': '/admin/filebrowser/browse/', 
            'external': False}]))
        self.children.append(modules.LinkList(_('Support'), column=2, children=[
         {'title': _('Django Documentation'), 
            'url': 'http://docs.djangoproject.com/', 
            'external': True},
         {'title': _('Grappelli Documentation'), 
            'url': 'http://packages.python.org/django-grappelli/', 
            'external': True},
         {'title': _('Grappelli Google-Code'), 
            'url': 'http://code.google.com/p/django-grappelli/', 
            'external': True}]))
        self.children.append(modules.Feed(_('Latest Django News'), column=2, feed_url='http://www.djangoproject.com/rss/weblog/', limit=5))
        self.children.append(modules.RecentActions(_('Recent Actions'), limit=5, collapsible=False, column=3))