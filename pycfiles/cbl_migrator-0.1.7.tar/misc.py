# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cblog/utils/misc.py
# Compiled at: 2006-12-13 19:45:32
import cherrypy
from turbogears import url

def absolute_url(suffix='', params=None, **kw):
    """Return the absolute URL to this server, appending 'suffix' if given."""
    aurl = 'http://%s/' % cherrypy.request.headers['Host']
    if suffix:
        aurl += url(suffix, params, **kw).lstrip('/')
    return aurl


def et_textlist(el, _addtail=False):
    """Returns list of text strings contained within an ET.Element and its sub-elements.

    Helpful for extracting text from prose-oriented XML (such as XHTML or
    DocBook).

    After: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/498286
    """
    result = []
    if el.text is not None:
        result.append(el.text)
    for elem in el:
        result.extend(et_textlist(elem, True))

    if _addtail and el.tail is not None:
        result.append(el.tail)
    return result