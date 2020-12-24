# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webstring\xmlt.py
# Compiled at: 2007-01-03 20:14:57
"""XML Template engine."""
from webstring.etreet import EtreeTemplate
from webstring.lxmlt import LxmlTemplate
from webstring.wsgi import WSGIBase
__all__ = [
 'XMLTemplate', 'WSGITemplate', 'template']

def template(source, **kw):
    """Decorator for general templating."""

    def decorator(application):
        return WSGITemplate(application, source, **kw)

    return decorator


class XMLTemplate(object):
    """XML template class."""
    __module__ = __name__

    def __new__(cls, *args, **kw):
        engine = kw.get('engine', 'etree')
        if engine == 'lxml':
            return LxmlTemplate(*args, **kw)
        elif engine == 'etree':
            return EtreeTemplate(*args, **kw)


class WSGITemplate(WSGIBase):
    """WSGI middleware for using XMLTemplate to render web content."""
    __module__ = __name__
    _format, _klass = 'xml', XMLTemplate