# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nazrul/www/python/Contributions/apps/hybrid-access-control-system/hacs/forms.py
# Compiled at: 2016-07-12 14:55:33
# Size of source mod 2**32: 2565 bytes
from __future__ import unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import RoutingTable
from .models import SiteRoutingRules
from .models import ContentTypeRoutingRules
from .globals import HTTP_METHOD_LIST
__author__ = 'Md Nazrul Islam<connect2nazrul@gmail.com>'
__all__ = [str(x) for x in ('RoutingTableForm', 'RoutingTableAdminForm', 'ContentTypeRoutingRulesForm',
                            'ContentTypeRoutingRulesAdminForm', 'SiteRoutingRulesForm',
                            'SiteRoutingRulesAdminForm')]

class RoutingTableForm(forms.ModelForm):
    __doc__ = ''

    class Meta:
        model = RoutingTable
        fields = ('route_name', 'description', 'urls', 'handlers', 'is_active')


class RoutingTableAdminForm(RoutingTableForm):
    __doc__ = ''

    class Meta(RoutingTableForm.Meta):
        model = None


class SiteRoutingRulesForm(forms.ModelForm):
    __doc__ = ''
    allowed_method = forms.MultipleChoiceField(choices=[(x, x) for x in HTTP_METHOD_LIST], label=_('Allowed Method'), widget=FilteredSelectMultiple('allowed method', False))

    class Meta:
        model = SiteRoutingRules
        fields = ('route', 'site', 'allowed_method', 'is_active', 'blacklisted_uri',
                  'whitelisted_uri', 'maintenance_mode')


class SiteRoutingRulesAdminForm(SiteRoutingRulesForm):
    __doc__ = ''

    class Meta(SiteRoutingRulesForm.Meta):
        model = None


class ContentTypeRoutingRulesForm(forms.ModelForm):
    __doc__ = ''
    allowed_method = forms.MultipleChoiceField(choices=[(x, x) for x in HTTP_METHOD_LIST], label=_('Allowed Method'), widget=FilteredSelectMultiple('allowed method', False))
    content_type = forms.ModelChoiceField(queryset=ContentType.objects.filter(model__in=('user',
                                                                                         'group'), app_label__in=('auth', )))

    class Meta:
        model = ContentTypeRoutingRules
        fields = ('route', 'site', 'content_type', 'allowed_method', 'object_id', 'is_active',
                  'blacklisted_uri', 'whitelisted_uri')
        widgets = {'allowed_method': FilteredSelectMultiple('allowed method', True)}


class ContentTypeRoutingRulesAdminForm(ContentTypeRoutingRulesForm):
    __doc__ = ''

    class Meta(ContentTypeRoutingRulesForm.Meta):
        model = None