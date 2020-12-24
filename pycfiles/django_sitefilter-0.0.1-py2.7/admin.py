# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sitefilter/admin.py
# Compiled at: 2012-11-20 08:29:49
from django.core.exceptions import FieldError
from sitefilter.models import get_current_site_filter

class SiteFilterMixin(object):

    def queryset(self, request):
        queryset = super(SiteFilterMixin, self).queryset(request)
        sites = get_current_site_filter(request).sites.all()
        if sites:
            try:
                return queryset.filter(site__in=sites).distinct()
            except FieldError:
                return queryset.filter(sites__in=sites).distinct()

        return queryset