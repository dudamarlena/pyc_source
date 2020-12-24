# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dvs/Dropbox/Code/djangoql/test_project/core/views.py
# Compiled at: 2019-10-08 06:04:43
# Size of source mod 2**32: 895 bytes
import json
from django.contrib.auth.models import Group, User
from django.shortcuts import render
from django.views.decorators.http import require_GET
from djangoql.exceptions import DjangoQLError
from djangoql.queryset import apply_search
from djangoql.schema import DjangoQLSchema

class UserQLSchema(DjangoQLSchema):
    include = (
     User, Group)


@require_GET
def completion_demo(request):
    q = request.GET.get('q', '')
    error = ''
    query = User.objects.all().order_by('username')
    if q:
        try:
            query = apply_search(query, q, schema=UserQLSchema)
        except DjangoQLError as e:
            query = query.none()
            error = str(e)

    return render(request, 'completion_demo.html', context={'q':q, 
     'error':error, 
     'search_results':query, 
     'introspections':json.dumps(UserQLSchema(query.model).as_dict())})