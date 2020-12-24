# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/community/context_processors.py
# Compiled at: 2012-03-17 12:42:14
from django.conf import settings
from sphene.community.models import Navigation
from sphene.community.permissionutils import has_permission_flag
from sphene.community.sphutils import SphSettings
from sphene.community.middleware import get_current_group, get_current_sphdata, get_current_user

class PermissionFlagLookup(object):

    def __getitem__(self, flag_name):
        return has_permission_flag(get_current_user(), flag_name)


def navigation(request):
    if hasattr(request, 'attributes') and 'group' in request.attributes:
        group = request.attributes['group']
    else:
        group = get_current_group()
    sphdata = get_current_sphdata()
    sph_settings = getattr(settings, 'SPH_SETTINGS', None)
    sphdata['installed_apps'] = settings.INSTALLED_APPS
    sphdata['current_url'] = request.path
    querystring = request.META.get('QUERY_STRING', None)
    if querystring:
        sphdata['current_url'] += '?' + querystring
    urlPrefix = ''
    if hasattr(request, 'attributes'):
        urlPrefix = request.attributes.get('urlPrefix', '')
    if group:
        return {'navigation_left': Navigation.objects.filter(group=group, navigationType=0), 
           'navigation_top': Navigation.objects.filter(group=group, navigationType=1), 
           'urlPrefix': urlPrefix, 
           'group': group, 
           'sph': sphdata, 
           'sph_settings': SphSettings(), 
           'sph_perms': PermissionFlagLookup()}
    else:
        return {'sph': sphdata, 'sph_settings': SphSettings(), 
           'sph_perms': PermissionFlagLookup()}