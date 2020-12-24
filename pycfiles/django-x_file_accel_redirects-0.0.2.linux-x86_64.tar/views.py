# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/imposeren/kava/42-kavyarnya/.env/lib/python2.7/site-packages/x_file_accel_redirects/views.py
# Compiled at: 2014-03-28 04:50:51
from django.views.static import serve
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from x_file_accel_redirects.models import AccelRedirect
from x_file_accel_redirects.conf import settings

def accel_view(request, prefix, filepath=''):
    try:
        redirect_config = AccelRedirect.objects.get(prefix=prefix)
    except AccelRedirect.DoesNotExist:
        return HttpResponseNotFound()

    redirect_config.process(filepath)
    if redirect_config.login_required and not request.user.is_authenticated():
        return HttpResponseForbidden()
    if settings.X_FILE_ACCEL:
        response = HttpResponse()
        if redirect_config.disposition_header:
            response['Content-Disposition'] = redirect_config.disposition_header
        response['X-Accel-Redirect'] = redirect_config.accel_path
    else:
        response = serve(request, filepath, redirect_config.serve_document_root, show_indexes=False)
    return response