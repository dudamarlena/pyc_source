# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/djweed/views.py
# Compiled at: 2018-03-12 01:56:47
# Size of source mod 2**32: 826 bytes
from mimetypes import guess_type
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse

def get_file(request, content_type_id, object_id, field_name, file_name):
    try:
        ct = ContentType.objects.get_for_id(content_type_id)
        obj = ct.get_object_for_this_type(id=object_id)
        field = getattr(obj, field_name)
    except (ObjectDoesNotExist, AttributeError):
        raise Http404

    if getattr(settings, 'ALLOW_NGINX_X_ACCEL_REDIRECT'):
        response = HttpResponse()
        response['X-Accel-Redirect'] = field.storage_url
    else:
        response = HttpResponse((field.content), content_type=(guess_type(field.verbose_name)[0]))
    return response