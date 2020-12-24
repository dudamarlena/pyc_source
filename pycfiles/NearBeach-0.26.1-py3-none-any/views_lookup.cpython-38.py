# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled/NearBeach/views_lookup.py
# Compiled at: 2020-05-03 01:13:24
# Size of source mod 2**32: 1339 bytes
from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from .misc_functions import *
import simplejson

@login_required(login_url='login', redirect_field_name='')
def lookup_product(request, product_id):
    product_results = product_and_service.objects.filter(product_id=product_id)
    data = serializers.serialize('json', product_results)
    return HttpResponse(data, content_type='application/json')


@login_required(login_url='login', redirect_field_name='')
def lookup_user_permissions(request):
    """
    This lookup is designed so that the user can do either:
    1.) Refresh their permissions without having to log in and out
    2.) For bots, who require to go through the admin login
    3.) System Engineer to extract information from the system to help the user
    """
    data = serializers.serialize('json',
      user_group.objects.filter(username=(request.user),
      is_deleted='FALSE'),
      use_natural_foreign_keys=True,
      use_natural_primary_keys=True)
    request.session['NearBeach_Permissions'] = data
    request.session['is_superuser'] = request.user.is_superuser
    return HttpResponse(data, content_type='application/json')