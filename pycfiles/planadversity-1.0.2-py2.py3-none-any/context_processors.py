# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/projects/volunteer-coordination/volunteerhub/apps/volunteers/context_processors.py
# Compiled at: 2014-07-14 11:23:15
from .models import Organization

def organization_loader(request):
    current_org = request.session.get('current_organization', None)
    try:
        user_orgs = Organization.objects.filter(managers=request.user)
    except TypeError:
        user_orgs = []

    if len(user_orgs) >= 1 and current_org is None:
        current_org = user_orgs[0]
    return {'current_organization': current_org, 'user_orgs': user_orgs}