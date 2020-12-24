# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nazrul/www/python/Contributions/apps/hybrid-access-control-system/hacs/admin.py
# Compiled at: 2016-06-19 13:04:59
# Size of source mod 2**32: 2318 bytes
from django.conf import settings
from django.contrib import admin
from .models import RoutingTable
from .models import SiteRoutingRules
from .models import ContentTypeRoutingRules
from .defaults import HACS_DEVELOPMENT_MODE
from .forms import RoutingTableAdminForm
from .forms import SiteRoutingRulesAdminForm
from .forms import ContentTypeRoutingRulesAdminForm
__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'

@admin.register(RoutingTable)
class RoutingTableAdmin(admin.ModelAdmin):
    __doc__ = ''
    form = RoutingTableAdminForm

    class Media:
        css = {}
        if getattr(settings, 'HACS_DEVELOPMENT_MODE', HACS_DEVELOPMENT_MODE):
            css['all'] = ('hacs_assets/css/jquery-ui.css', 'hacs_assets/css/jqueryui-editable.css',
                          'hacs_assets/css/hacs.css')
            js = ('hacs_assets/js/lodash.4.13.1.js', 'hacs_assets/js/jquery-2.2.4.js',
                  'hacs_assets/js/jquery-ui.js', 'hacs_assets/js/jqueryui-editable.js',
                  'hacs_assets/js/hacs.js')
        else:
            css['all'] = ('admin/hacs/css/hacs.min.css', )
            js = ('admin/hacs/js/hacs.min.js', )


@admin.register(SiteRoutingRules)
class SiteRoutingRulesAdmin(admin.ModelAdmin):
    form = SiteRoutingRulesAdminForm


@admin.register(ContentTypeRoutingRules)
class ContentTypeRoutingRulesAdmin(admin.ModelAdmin):
    __doc__ = ''
    form = ContentTypeRoutingRulesAdminForm

    class Media:
        css = {}
        if getattr(settings, 'HACS_DEVELOPMENT_MODE', HACS_DEVELOPMENT_MODE):
            css['all'] = ('hacs_assets/css/select2.css', 'hacs_assets/css/hacs.css')
            js = ('hacs_assets/js/lodash.4.13.1.js', 'hacs_assets/js/jquery-2.2.4.js',
                  'hacs_assets/js/select2.full.js', 'hacs_assets/js/hacs.js')
        else:
            css['all'] = ('admin/hacs/css/hacs.min.css', )
            js = ('admin/hacs/js/hacs.min.js', )