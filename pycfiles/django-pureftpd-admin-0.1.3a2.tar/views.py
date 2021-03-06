# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ivan/pycharm-workplace/test_ftp/pureftpd_admin/localdir/views.py
# Compiled at: 2013-08-15 10:05:22
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
import os, posixpath
try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote

def directory_index(path, fullpath):
    show_hidden = False
    nodes = (node for node in os.listdir(fullpath))
    if not show_hidden:
        nodes = filter(lambda x: not x.startswith('.'), nodes)
    files = sorted(filter(lambda f: os.path.isfile(os.path.join(fullpath, f)), nodes), key=lambda x: x.lower())
    dirs = map(lambda d: d + '/', sorted(filter(lambda d: d not in files and os.access(os.path.join(fullpath, d), os.R_OK), nodes), key=lambda x: x.lower()))
    context = {'directory': path + '/', 
       'dirs': dirs, 
       'files': files, 
       'fullpath': '' if fullpath == os.sep else fullpath, 
       'STATIC_URL': settings.STATIC_URL}
    return render_to_response('localdir/directory_index.html', context)


def serve(request, path, document_root=None):
    path = posixpath.normpath(unquote(path))
    path = path.lstrip('/')
    newpath = ''
    for part in path.split('/'):
        if not part:
            continue
        drive, part = os.path.splitdrive(part)
        head, part = os.path.split(part)
        if part in (os.curdir, os.pardir):
            continue
        newpath = os.path.join(newpath, part).replace('\\', '/')

    if newpath and path != newpath:
        return HttpResponseRedirect(newpath)
    fullpath = newpath and os.path.join(document_root, newpath) or os.path.normpath(document_root)
    if os.path.isdir(fullpath):
        return directory_index(newpath, fullpath)
    return HttpResponseRedirect('../?' + request.GET.urlencode())