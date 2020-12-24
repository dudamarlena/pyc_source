# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webstring\lxmlt.py
# Compiled at: 2007-01-03 20:10:09
"""lxml-based XML template engine."""
try:
    import lxml.etree as etree
except ImportError:
    raise ImportError('LxmlTemplate needs the lxml library')

from webstring.xmlbase import *
from webstring.htmlbase import HTMLBase
__all__ = ['LxmlTemplate']

class _LxmlBase(object):
    """lxml specific methods."""
    __module__ = __name__
    _xslt = None

    def _setxslt(self, stylesheet):
        """Sets the XSLT stylesheet for a template."""
        self._xslt = self._etree.XSLT(self._etree.XML(stylesheet))

    def transform(self, stylesheet=None, **kw):
        """Transforms a template based on an XSLT stylesheet.

        @param stylesheet XSLT document (default: None)
        @param kw Keyword arguments
        """
        if stylesheet is not None:
            self._setxslt(stylesheet)
        return str(self._xslt(self._tree, **kw))

    def xinclude(self):
        """Processes any xinclude statements in the internal template."""
        eobj = self._etree.ElementTree(self._tree)
        eobj.xinclude()

    xslt = property(lambda self: self._xslt, _setxslt)


class _LxmlOne(_XMLOne, _LxmlBase):
    """lxml-based Field base class."""
    __module__ = __name__
    _etree = etree

    def __init__(self, *arg, **kw):
        super(_LxmlOne, self).__init__(*arg, **kw)


class _LxmlField(_XMLField):
    """lxml-based Field dispatcher."""
    __module__ = __name__
    _etree, _group, _klass = etree, None, _LxmlOne


class _LxmlGroup(object):
    """lxml-based Group class."""
    __module__ = __name__

    def __new__(cls, *args, **kw):
        _XMLGroup._etree, _XMLGroup._field, _XMLGroup._group = etree, _LxmlField, cls
        return type('_LxmlGroup', (_XMLGroup, _LxmlBase), {})(*args, **kw)


_LxmlField._group = _LxmlGroup

class LxmlTemplate(_XMLTemplate, _LxmlBase):
    """lxml-based root Template class."""
    __module__ = __name__
    _etree, _field, _group = etree, _LxmlField, _LxmlGroup
    current = property(lambda self: LxmlTemplate(_copytree(self._tree), self._auto, self._max, templates=self._templates))
    default = property(lambda self: LxmlTemplate(_copytree(self._btree), self._auto, self._max, templates=self._templates))


class LxmlHTML(HTMLBase, LxmlTemplate):
    """Template class for HTML documents."""
    __module__ = __name__

    def fromfile(self, path):
        """Creates an internal element from a file source.

        @param path Path to a template source
        """
        try:
            super(LxmlHTML, self).fromfile(path)
        except:
            parser = self._etree.HTMLParser()
            self._setelement(self._etree.parse(path), parser)

    def fromstring(self, instring):
        """Creates an internal element from a string source.

        @param path String source for an internal template
        """
        try:
            super(LxmlHTML, self).fromstring(instring)
        except:
            self._setelement(self._etree.HTML(instring))