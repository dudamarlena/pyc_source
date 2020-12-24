# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/utils/downloadFile.py
# Compiled at: 2014-07-02 14:33:05
import mimetypes, os
from django.http import HttpResponse
from django.utils.http import http_date
from protoLib.utilsWeb import JsonError

def getFile(request, path):
    if not request.user.is_authenticated():
        return JsonError('readOnly User')
    fullpath = getFullPath(request, path)
    if not os.path.exists(fullpath):
        return JsonError('"%s" does not exist' % path)
    statobj = os.stat(fullpath)
    mimetype, encoding = mimetypes.guess_type(fullpath)
    mimetype = mimetype or 'application/octet-stream'
    response = HttpResponse(open(fullpath, 'rb').read(), content_type=mimetype)
    response['Last-Modified'] = http_date(statobj.st_mtime)
    response['Content-Length'] = statobj.st_size
    if encoding:
        response['Content-Encoding'] = encoding
    return response


def getFullPath(request, filename):
    from django.conf import settings
    PPATH = settings.PPATH
    return os.path.join(PPATH, 'output', request.user.username + '.' + filename)