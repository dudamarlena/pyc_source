# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/richcomments/views.py
# Compiled at: 2011-09-15 07:14:57
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.template import Template, RequestContext

def list(request, content_type, id):
    """
    Wrapper exposing comment's render_comment_list tag as a view.
    """
    (app_label, model) = content_type.split('-')
    ctype = ContentType.objects.get(app_label=app_label, model=model)
    obj = ctype.get_object_for_this_type(id=id)
    t = Template('{% load comments %}{% render_comment_list for object %}')
    context = RequestContext(request)
    context.update({'object': obj})
    result = t.render(context)
    return HttpResponse(result)