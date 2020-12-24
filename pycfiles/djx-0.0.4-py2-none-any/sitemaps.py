# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/flatpages/sitemaps.py
# Compiled at: 2019-02-14 00:35:16
from django.apps import apps as django_apps
from django.contrib.sitemaps import Sitemap
from django.core.exceptions import ImproperlyConfigured

class FlatPageSitemap(Sitemap):

    def items(self):
        if not django_apps.is_installed('django.contrib.sites'):
            raise ImproperlyConfigured("FlatPageSitemap requires django.contrib.sites, which isn't installed.")
        Site = django_apps.get_model('sites.Site')
        current_site = Site.objects.get_current()
        return current_site.flatpage_set.filter(registration_required=False)