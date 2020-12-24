# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/django_swift/views.py
# Compiled at: 2013-06-14 05:45:24
import logging
from django.core.files.storage import default_storage
from django.http.response import StreamingHttpResponse, HttpResponse
logger = logging.getLogger()

def download(request, name):
    try:
        f = default_storage.open(name)
        headers, data = f.connection.get_object(f.container_name, f.name, resp_chunk_size=1048576)
        response = StreamingHttpResponse(data)
        for item in headers.viewitems():
            response[item[0]] = item[1]

    except BaseException as e:
        response = HttpResponse()
        if hasattr(e, 'http_status'):
            response.status_code = e.http_status
        else:
            response.status_code = 500
            logger.exception(e)

    return response