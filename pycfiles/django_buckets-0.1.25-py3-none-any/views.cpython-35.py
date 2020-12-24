# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-buckets/buckets/views.py
# Compiled at: 2017-01-02 04:04:27
# Size of source mod 2**32: 923 bytes
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils.translation import ugettext as _
from django.core.files.storage import default_storage
from buckets.exceptions import InvalidPayload

def validate_payload(payload):
    errors = {}
    key = payload.get('key', None)
    if not key:
        errors['key'] = _("'key' is required")
    if errors:
        raise InvalidPayload(errors=errors)


@require_POST
def signed_url(request):
    if not hasattr(default_storage, 'get_signed_url'):
        response = {'error': 'Not found'}
        status = 404
    else:
        try:
            validate_payload(request.POST)
            response = default_storage.get_signed_url(key=request.POST['key'])
            status = 200
        except InvalidPayload as e:
            response = e.errors
            status = 400

    return JsonResponse(response, status=status)