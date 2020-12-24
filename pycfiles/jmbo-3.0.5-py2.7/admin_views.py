# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo/admin_views.py
# Compiled at: 2016-10-27 15:23:38
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden
from jmbo.models import ModelBase

@staff_member_required
def publish_ajax(request):
    obj = ModelBase.objects.get(id=request.REQUEST['id'])
    obj.publish()
    return HttpResponse('published')


@staff_member_required
def unpublish_ajax(request):
    obj = ModelBase.objects.get(id=request.REQUEST['id'])
    obj.unpublish()
    return HttpResponse('unpublished')


@require_POST
@staff_member_required
def edit_autosave_ajax(request):
    obj = ModelBase.objects.get(id=request.POST['id']).as_leaf_class()
    model = type(obj)
    permission = model._meta.app_label + '.' + model._meta.get_change_permission()
    if not request.user.has_perm(permission):
        return HttpResponseForbidden('You are not allowed to change this object')
    changes = False
    for field in getattr(obj, 'autosave_fields', []):
        new_value = request.POST.get(field)
        old_value = getattr(obj, field)
        if new_value != old_value:
            setattr(obj, field, new_value)
            changes = True

    if changes:
        obj.save()
    return HttpResponse('1')