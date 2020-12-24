# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webstring\htmlbase.py
# Compiled at: 2007-01-03 20:09:19
"""HTML template base."""
from xmlbase import _copytree
__all__ = [
 'HTMLBase']
_xheader = '<?xml version="1.0" encoding="%s"?>'
_xss = '<?xml-stylesheet href="%s" type="text/css" ?>'
_html4 = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">'
_xhtmlns = '{http://www.w3.org/1999/xhtml}'
_xhtml10 = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
_xhtml11 = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'

class HTMLBase(object):
    """Base class for HTML Templates."""
    __module__ = __name__

    def pipe(self, info=None, format='html', encoding='utf-8'):
        """Returns a string version of the internal element's parent and
        resets this Template.

        @param info Data to substitute into a document (default: None)
        @param format Format of document (default: 'html')
        @param encoding Encoding type for return string (default: 'utf-8')
        """
        return super(HTMLBase, self).pipe(info, format, encoding)

    def render(self, info=None, format='html', encoding='utf-8'):
        """Returns an HTML version of the internal element's parent.

        @param info Data to substitute into a document (default: None)
        @param format HTML format to use for string (default: 'html')        
        @param encoding Encoding type for return string (default: 'utf-8')
        """
        if info is not None:
            self.__imod__(info)
        tree = _copytree(self._tree)
        for elem in tree.getiterator():
            if elem.tag.startswith(_xhtmlns):
                elem.tag = elem.tag[len(_xhtmlns):]

        doc = self._etree.tostring(tree, encoding)
        if format == 'html':
            doc = ('\n').join([_html4, doc])
            doc = doc.replace('/>', '>').replace(' >', '>')
            doc = doc.replace(' xmlns:html="http://www.w3.org/1999/xhtml"', '')
        elif format.startswith('xhtml1'):
            header, stylesheets = [
             _xheader % encoding], list()
            for tag in tree.getiterator('link'):
                if tag.get('type') == 'text/css':
                    stylesheets.append(_xss % tag.get('href'))

            if format == 'xhtml10':
                stylesheets.append(_xhtml10)
            elif format == 'xhtml11':
                stylesheets.append(_xhtml11)
            doc = ('\n').join([('\n').join(header), ('\n').join(stylesheets), doc])
        return doc

    def write(self, path, info=None, format='html', encoding='utf-8'):
        """Writes the string of an internal element to a file.

        @param path Path of destination file
        @param info Data to substitute into a document (default: None)
        @param format Format of document (default: 'html')
        @param encoding Encoding type for return string (default: 'utf-8')
        """
        super(HTMLBase, self).write(path, info, format, encoding)