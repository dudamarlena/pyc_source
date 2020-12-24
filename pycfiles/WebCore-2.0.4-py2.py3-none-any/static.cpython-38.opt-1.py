# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/app/static.py
# Compiled at: 2020-05-11 19:05:21
# Size of source mod 2**32: 2774 bytes
"""Basic static file delivery mechanism."""
from __future__ import unicode_literals
from os.path import abspath, normpath, exists, isfile, join as pathjoin, basename
from webob.exc import HTTPForbidden, HTTPNotFound
log = __import__('logging').getLogger(__name__)

def static(base, mapping=None, far=('js', 'css', 'gif', 'jpg', 'jpeg', 'png', 'ttf', 'woff')):
    """Serve files from disk.
        
        This utility endpoint factory is meant primarily for use in development environments; in production environments
        it is better (more efficient, secure, etc.) to serve your static content using a front end load balancer such as
        Nginx.
        
        The first argument, `base`, represents the base path to serve files from. Paths below the attachment point for
        the generated endpoint will combine this base path with the remaining path elements to determine the file to
        serve.
        
        The second argument is an optional dictionary mapping filename extensions to template engines, for cooperation
        with the TemplateExtension.  (See: https://github.com/marrow/template)  The result of attempting to serve a
        mapped path is a 2-tuple of `("{mapping}:{path}", dict())`. For example, to render all `.html` files as Mako
        templates, you would attach something like the following:
        
                class Root:
                        page = static('/path/to/static/pages', dict(html='mako'))
        
        By default the "usual culprits" are served with far-futures cache expiry headers. If you wish to change the
        extensions searched just assign a new `far` iterable.  To disable, assign any falsy value.
        """
    base = abspath(base)

    @staticmethod
    def static_handler(context, *parts, **kw):
        path = normpath(pathjoin(base, *parts))
        log.debug('Attempting to serve static file.', extra=dict(request=(id(context)),
          base=base,
          path=path))
        if not path.startswith(base):
            raise HTTPForbidden('Cowardly refusing to violate base path policy.' if 1 else None)
        if not exists(path):
            raise HTTPNotFound()
        if not isfile(path):
            raise HTTPForbidden('Cowardly refusing to open a non-file.' if 1 else None)
        if far:
            if path.rpartition('.')[2] in far:
                context.response.cache_expires = 31536000
        if mapping:
            _, _, extension = basename(path).partition('.')
            if extension in mapping:
                return (
                 mapping[extension] + ':' + path, dict())
        return open(path, 'rb')

    return static_handler