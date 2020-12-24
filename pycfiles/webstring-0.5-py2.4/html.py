# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webstring\html.py
# Compiled at: 2007-01-03 20:09:13
"""HTML Template engine."""
from webstring.etreet import EtreeHTML
from webstring.lxmlt import LxmlHTML
from webstring.wsgi import WSGIBase
__all__ = [
 'HTMLTemplate', 'WSGIHTMLTemplate', 'htmltemplate']

def htmltemplate(source, **kw):
    """Decorator for HTML templating for WSGI."""

    def decorator(application):
        return WSGIHTMLTemplate(application, source, **kw)

    return decorator


class HTMLTemplate(object):
    """HTML template class."""
    __module__ = __name__

    def __new__(cls, *args, **kw):
        engine = kw.get('engine', 'etree')
        if engine == 'lxml':
            return LxmlHTML(*args, **kw)
        elif engine == 'etree':
            return EtreeHTML(*args, **kw)


class WSGIHTMLTemplate(WSGIBase):
    """WSGI middleware for using HTMLTemplate to render web content."""
    __module__ = __name__
    _format, _klass = 'html', HTMLTemplate