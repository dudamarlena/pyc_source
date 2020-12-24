# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/rst.py
# Compiled at: 2007-01-07 21:49:07
"""Restructured Text Support Module

This module is used internally to transform docstrings and Restructured
Text documents to HTML.

"""
import sys
from docutils.core import publish_parts

def parts(file):
    """
    Parse ``file`` and return a dictionary containing transformed parts.

    This uses the ``docutils.core.publish_parts`` function internally.
    Interesting parts include the following:

    fragment
      The body without the header, title, or footer.

    title
      The document title.
    
    """
    fo = open(file, 'r')
    source = fo.read()
    fo.close()
    parts = publish_parts(source, source_path=file, writer_name='html')
    for (k, v) in parts.items():
        parts[k] = _scrub_html(v)

    return parts


def to_html(text, name=None):
    """
    Convert ``text`` to HTML and return result as a unicode string.
    """
    source = text
    parts = publish_parts(source, source_path=name, writer_name='html')
    return _scrub_html(parts['body'])


def _scrub_html(html):
    return html.replace('&nbsp;', '&#0160;')


def trim(docstring):
    """
    Trim a docstring.

    Taken from the example given in :pep:`257`.
    """
    if not docstring:
        return ''
    lines = docstring.expandtabs().splitlines()
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))

    trimmed = [
     lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())

    while trimmed and not trimmed[(-1)]:
        trimmed.pop()

    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    return ('\n').join(trimmed)


__all__ = [
 'parts', 'to_html', 'trim']
__author__ = 'Ryan Tomayko <rtomayko@gmail.com>'
__date__ = '$Date: 2007-01-07 19:08:36 -0800 (Sun, 07 Jan 2007) $'
__revision__ = '$Revision: 134 $'
__url__ = '$URL: svn://lesscode.org/pudge/trunk/pudge/rst.py $'
__copyright__ = 'Copyright 2005, Ryan Tomayko'
__license__ = 'MIT <http://www.opensource.org/licenses/mit-license.php>'