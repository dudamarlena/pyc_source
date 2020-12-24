# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/views/static.py
# Compiled at: 2018-07-11 18:15:30
"""
Views and functions for serving static files. These are only to be used
during development, and SHOULD NOT be used in a production setting.
"""
from __future__ import unicode_literals
import mimetypes, os, stat, posixpath, re
try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote

from django.http import CompatibleStreamingHttpResponse, Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotModified
from django.template import loader, Template, Context, TemplateDoesNotExist
from django.utils.http import http_date, parse_http_date
from django.utils.translation import ugettext as _, ugettext_noop

def serve(request, path, document_root=None, show_indexes=False):
    """
    Serve static files below a given point in the directory structure.

    To use, put a URL pattern such as::

        (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root' : '/path/to/my/files/'})

    in your URLconf. You must provide the ``document_root`` param. You may
    also set ``show_indexes`` to ``True`` if you'd like to serve a basic index
    of the directory.  This index view will use the template hardcoded below,
    but if you'd like to override it, you can create a template called
    ``static/directory_index.html``.
    """
    path = posixpath.normpath(unquote(path))
    path = path.lstrip(b'/')
    newpath = b''
    for part in path.split(b'/'):
        if not part:
            continue
        drive, part = os.path.splitdrive(part)
        head, part = os.path.split(part)
        if part in (os.curdir, os.pardir):
            continue
        newpath = os.path.join(newpath, part).replace(b'\\', b'/')

    if newpath and path != newpath:
        return HttpResponseRedirect(newpath)
    fullpath = os.path.join(document_root, newpath)
    if os.path.isdir(fullpath):
        if show_indexes:
            return directory_index(newpath, fullpath)
        raise Http404(_(b'Directory indexes are not allowed here.'))
    if not os.path.exists(fullpath):
        raise Http404(_(b'"%(path)s" does not exist') % {b'path': fullpath})
    statobj = os.stat(fullpath)
    mimetype, encoding = mimetypes.guess_type(fullpath)
    mimetype = mimetype or b'application/octet-stream'
    if not was_modified_since(request.META.get(b'HTTP_IF_MODIFIED_SINCE'), statobj.st_mtime, statobj.st_size):
        return HttpResponseNotModified()
    response = CompatibleStreamingHttpResponse(open(fullpath, b'rb'), content_type=mimetype)
    response[b'Last-Modified'] = http_date(statobj.st_mtime)
    if stat.S_ISREG(statobj.st_mode):
        response[b'Content-Length'] = statobj.st_size
    if encoding:
        response[b'Content-Encoding'] = encoding
    return response


DEFAULT_DIRECTORY_INDEX_TEMPLATE = b'\n{% load i18n %}\n<!DOCTYPE html>\n<html lang="en">\n  <head>\n    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />\n    <meta http-equiv="Content-Language" content="en-us" />\n    <meta name="robots" content="NONE,NOARCHIVE" />\n    <title>{% blocktrans %}Index of {{ directory }}{% endblocktrans %}</title>\n  </head>\n  <body>\n    <h1>{% blocktrans %}Index of {{ directory }}{% endblocktrans %}</h1>\n    <ul>\n      {% ifnotequal directory "/" %}\n      <li><a href="../">../</a></li>\n      {% endifnotequal %}\n      {% for f in file_list %}\n      <li><a href="{{ f|urlencode }}">{{ f }}</a></li>\n      {% endfor %}\n    </ul>\n  </body>\n</html>\n'
template_translatable = ugettext_noop(b'Index of %(directory)s')

def directory_index(path, fullpath):
    try:
        t = loader.select_template([b'static/directory_index.html',
         b'static/directory_index'])
    except TemplateDoesNotExist:
        t = Template(DEFAULT_DIRECTORY_INDEX_TEMPLATE, name=b'Default directory index template')

    files = []
    for f in os.listdir(fullpath):
        if not f.startswith(b'.'):
            if os.path.isdir(os.path.join(fullpath, f)):
                f += b'/'
            files.append(f)

    c = Context({b'directory': path + b'/', 
       b'file_list': files})
    return HttpResponse(t.render(c))


def was_modified_since(header=None, mtime=0, size=0):
    """
    Was something modified since the user last downloaded it?

    header
      This is the value of the If-Modified-Since header.  If this is None,
      I'll just return True.

    mtime
      This is the modification time of the item we're talking about.

    size
      This is the size of the item we're talking about.
    """
    try:
        if header is None:
            raise ValueError
        matches = re.match(b'^([^;]+)(; length=([0-9]+))?$', header, re.IGNORECASE)
        header_mtime = parse_http_date(matches.group(1))
        header_len = matches.group(3)
        if header_len and int(header_len) != size:
            raise ValueError
        if int(mtime) > header_mtime:
            raise ValueError
    except (AttributeError, ValueError, OverflowError):
        return True

    return False