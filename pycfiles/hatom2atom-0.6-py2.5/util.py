# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hatom2atom/util.py
# Compiled at: 2008-12-18 22:31:30
"""util - utilities for the hatom2atom package

this file is part of the hatom2atom package.

created and maintained by luke arno <luke.arno@gmail.com>

copyright (c) 2006  Luke Arno  <luke.arno@gmail.com>

this program is free software; you can redistribute it and/or
modify it under the terms of the gnu general public license
as published by the free software foundation; either version 2
of the license, or (at your option) any later version.

this program is distributed in the hope that it will be useful,
but without any warranty; without even the implied warranty of
merchantability or fitness for a particular purpose.  see the
gnu general public license for more details.

you should have received a copy of the gnu general public license
along with this program; if not, write to:

the free software foundation, inc., 
51 franklin street, fifth floor, 
boston, ma  02110-1301, usa.

luke arno can be found at http://lukearno.com/
"""
import urllib2, libxml2, libxslt
libxml2.thrDefLoadExtDtdDefaultValue(1)
from hatom2atom import settings

class TransformError(Exception):
    pass


def easy_transform(transform, source, params=None):
    """Transform with a filename, a string of XML and an optional dict."""
    try:
        source_doc = libxml2.parseDoc(source)
    except:
        raise TransformError('Could not parse sourcetree.')

    try:
        style_doc = libxml2.parseFile(transform)
    except:
        source_doc.freeDoc()
        raise TransformError('Could not parse transform tree.')

    try:
        style = libxslt.parseStylesheetDoc(style_doc)
        if style is None:
            raise
    except:
        source_doc.freeDoc()
        style_doc.freeDoc()
        raise TransformError('Could not parse stylesheet.')

    try:
        result = style.applyStylesheet(source_doc, params)
    except:
        source_doc.freeDoc()
        style.freeStylesheet()
        raise TransformError('Could not run stylesheet against source tree.')

    output = style.saveResultToString(result)
    source_doc.freeDoc()
    style.freeStylesheet()
    result.freeDoc()
    return output


def url_opener(environ):
    """Return a url opener that will set some headers."""
    client_ip = environ.get('REMOTE_ADDR', 'unknown')
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', settings.agent),
     (
      'Accept', settings.accept),
     (
      'X-Forwarded-For', client_ip),
     (
      'Referer', environ.get('HTTP_REFERER'))]
    return opener