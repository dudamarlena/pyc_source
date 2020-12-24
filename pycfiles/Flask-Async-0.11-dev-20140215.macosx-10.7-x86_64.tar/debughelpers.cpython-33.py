# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/flask/debughelpers.py
# Compiled at: 2014-02-15 13:00:30
# Size of source mod 2**32: 3503 bytes
"""
    flask.debughelpers
    ~~~~~~~~~~~~~~~~~~

    Various helpers to make the development experience better.

    :copyright: (c) 2014 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
from ._compat import implements_to_string

class UnexpectedUnicodeError(AssertionError, UnicodeError):
    __doc__ = 'Raised in places where we want some better error reporting for\n    unexpected unicode or binary data.\n    '


@implements_to_string
class DebugFilesKeyError(KeyError, AssertionError):
    __doc__ = 'Raised from request.files during debugging.  The idea is that it can\n    provide a better error message than just a generic KeyError/BadRequest.\n    '

    def __init__(self, request, key):
        form_matches = request.form.getlist(key)
        buf = [
         'You tried to access the file "%s" in the request.files dictionary but it does not exist.  The mimetype for the request is "%s" instead of "multipart/form-data" which means that no file contents were transmitted.  To fix this error you should provide enctype="multipart/form-data" in your form.' % (
          key, request.mimetype)]
        if form_matches:
            buf.append('\n\nThe browser instead transmitted some file names. This was submitted: %s' % ', '.join('"%s"' % x for x in form_matches))
        self.msg = ''.join(buf)

    def __str__(self):
        return self.msg


class FormDataRoutingRedirect(AssertionError):
    __doc__ = 'This exception is raised by Flask in debug mode if it detects a\n    redirect caused by the routing system when the request method is not\n    GET, HEAD or OPTIONS.  Reasoning: form data will be dropped.\n    '

    def __init__(self, request):
        exc = request.routing_exception
        buf = [
         'A request was sent to this URL (%s) but a redirect was issued automatically by the routing system to "%s".' % (
          request.url, exc.new_url)]
        if request.base_url + '/' == exc.new_url.split('?')[0]:
            buf.append('  The URL was defined with a trailing slash so Flask will automatically redirect to the URL with the trailing slash if it was accessed without one.')
        buf.append("  Make sure to directly send your %s-request to this URL since we can't make browsers or HTTP clients redirect with form data reliably or without user interaction." % request.method)
        buf.append('\n\nNote: this exception is only raised in debug mode')
        AssertionError.__init__(self, ''.join(buf).encode('utf-8'))


def attach_enctype_error_multidict(request):
    """Since Flask 0.8 we're monkeypatching the files object in case a
    request is detected that does not use multipart form data but the files
    object is accessed.
    """
    oldcls = request.files.__class__

    class newcls(oldcls):

        def __getitem__(self, key):
            try:
                return oldcls.__getitem__(self, key)
            except KeyError:
                if key not in request.form:
                    raise
                raise DebugFilesKeyError(request, key)

    newcls.__name__ = oldcls.__name__
    newcls.__module__ = oldcls.__module__
    request.files.__class__ = newcls