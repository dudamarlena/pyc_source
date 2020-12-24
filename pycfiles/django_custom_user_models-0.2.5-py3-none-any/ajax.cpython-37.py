# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\decorators\ajax.py
# Compiled at: 2019-12-10 17:11:23
# Size of source mod 2**32: 422 bytes
from django.http import HttpResponseBadRequest

def ajax_required(function):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return function(request, *args, **kwargs)

    return wrap