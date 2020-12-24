# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/django_includes/utils.py
# Compiled at: 2020-01-02 03:06:44
# Size of source mod 2**32: 358 bytes


def patch_http_development_server():
    """
    HACK: without HTTP/1.1, Chrome ignores certain cache headers during development!
     see http://stackoverflow.com/a/28033770/179583 for a bit more discussion.

    You can include this in your wsgi.py file.

    """
    from wsgiref import simple_server
    simple_server.ServerHandler.http_version = '1.1'