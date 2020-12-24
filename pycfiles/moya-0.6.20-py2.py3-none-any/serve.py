# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/serve.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import unicode_literals
from __future__ import print_function
from datetime import datetime
import mimetypes, tempfile
from fs.path import basename
from fs.errors import FSError
from fs.tools import copy_file_data
from .response import MoyaResponse
from .compat import PY2, py2bytes
from . import http
from .tools import md5_hexdigest
from . import logic
from . import __version__
SERVER_NAME = (b'Moya/{}.{}').format(*__version__.split(b'.')[:2])

def file_chunker(file, size=65536):
    """An iterator that reads a file in chunks."""
    read = file.read
    try:
        chunk = read(size)
        while chunk:
            yield chunk
            chunk = read(size)

    finally:
        file.close()


def serve_file(req, fs, path, filename=None, copy=False):
    """Serve a static file"""
    res = MoyaResponse()
    mime_type, encoding = mimetypes.guess_type(basename(path))
    if mime_type is None:
        mime_type = b'application/octet-stream' if PY2 else b'application/octet-stream'
    if not path or not fs.isfile(path):
        raise logic.EndLogic(http.RespondNotFound())
    serve_file = None
    try:
        info = fs.getdetails(path)
        serve_file = fs.open(path, b'rb')
    except FSError:
        if serve_file is not None:
            serve_file.close()
        raise logic.EndLogic(http.RespondNotFound())

    if copy:
        new_serve_file = tempfile.TemporaryFile(prefix=b'moyaserve')
        copy_file_data(serve_file, new_serve_file)
        new_serve_file.seek(0)
        serve_file = new_serve_file
    file_size = info.size
    mtime = info.modified or datetime.utcnow()
    res.date = datetime.utcnow()
    res.content_type = py2bytes(mime_type)
    res.last_modified = mtime
    res.etag = (b'{}-{}-{}').format(mtime, file_size, md5_hexdigest(path))
    res.server = SERVER_NAME
    if filename is not None:
        res.content_disposition = (b'attachment; filename="{}"').format(filename)
    status304 = False
    if req.if_none_match and res.etag:
        status304 = res.etag in req.if_none_match
    elif req.if_modified_since and res.last_modified:
        status304 = res.last_modified <= req.if_modified_since
    if status304:
        res.status = 304
        serve_file.close()
    elif b'wsgi.file_wrapper' in req.environ:
        res.app_iter = req.environ[b'wsgi.file_wrapper'](serve_file)
    else:
        res.app_iter = file_chunker(serve_file)
    if not status304:
        res.content_length = file_size
    raise logic.EndLogic(res)
    return