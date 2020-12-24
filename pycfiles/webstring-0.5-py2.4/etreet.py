# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webstring\etreet.py
# Compiled at: 2007-01-03 20:10:09
"""cElementTree-based XML template engine."""
try:
    from xml.etree import cElementTree as etree
except ImportError:
    import cElementTree as etree

try:
    from elementtidy import TidyHTMLTreeBuilder as tidy
except ImportError:
    pass

from webstring.xmlbase import *
from webstring.htmlbase import HTMLBase
__all__ = [
 'EtreeTemplate', 'EtreeHTML']
msg = 'Broken HTML requires elementtidy from http://effbot.org/downloads/'

def _copyhtml(tree):
    """Copies an HTML document while striping the tidy meta tag."""
    newdoc = _copytree(tree)
    for parent in newdoc.getiterator():
        for child in parent:
            if child.tag.endswith('meta'):
                if child.get('content').startswith('HTML Tidy'):
                    parent.remove(child)

    return newdoc


class _EtreeField(_XMLField):
    """cElementTree Field class."""
    __module__ = __name__
    _etree, _group, _klass = etree, None, _XMLOne


class _EtreeGroup(object):
    """cElementTree Group class."""
    __module__ = __name__

    def __new__(cls, *args, **kw):
        c = _XMLGroup
        c._etree, c._group, c._field = etree, _XMLGroup, _EtreeField
        return c(*args, **kw)


_EtreeField._group = _EtreeGroup

class EtreeTemplate(_XMLTemplate):
    """cElementTree-based root Template class."""
    __module__ = __name__
    _etree, _field, _group = etree, _EtreeField, _EtreeGroup
    current = property(lambda self: EtreeTemplate(_copytree(self._tree), self._auto, self._max, templates=self._templates))
    default = property(lambda self: EtreeTemplate(_copytree(self._btree), self._auto, self._max, templates=self._templates))


class EtreeHTML(HTMLBase, EtreeTemplate):
    """ElementTree HTML Template class."""
    __module__ = __name__

    def fromfile(self, path):
        """Creates an internal element from a file source.

        @param path Path to a template source
        """
        try:
            super(EtreeHTML, self).fromfile(path)
        except:
            try:
                self._setelement(_copyhtml(tidy.parse(path).getroot()))
            except NameError:
                raise ImportError(msg)

    def fromstring(self, instring):
        """Creates an internal element from a string source.

        @param path String source for an internal template
        """
        try:
            super(EtreeHTML, self).fromstring(instring)
        except:
            try:
                parser = tidy.TreeBuilder()
                parser.feed(instring)
                self._setelement(_copyhtml(parser.close()))
            except NameError:
                raise ImportError(msg)