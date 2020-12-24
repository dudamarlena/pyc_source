# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: nturl2path.pyc
# Compiled at: 2009-12-06 23:04:04
"""Convert a NT pathname to a file URL and vice versa."""

def url2pathname(url):
    """OS-specific conversion from a relative URL of the 'file' scheme
    to a file system path; not recommended for general use."""
    import string, urllib
    url = url.replace(':', '|')
    if '|' not in url:
        if url[:4] == '////':
            url = url[2:]
        components = url.split('/')
        return urllib.unquote(('\\').join(components))
    comp = url.split('|')
    if len(comp) != 2 or comp[0][(-1)] not in string.ascii_letters:
        error = 'Bad URL: ' + url
        raise IOError, error
    drive = comp[0][(-1)].upper()
    components = comp[1].split('/')
    path = drive + ':'
    for comp in components:
        if comp:
            path = path + '\\' + urllib.unquote(comp)

    return path


def pathname2url(p):
    """OS-specific conversion from a file system path to a relative URL
    of the 'file' scheme; not recommended for general use."""
    import urllib
    if ':' not in p:
        if p[:2] == '\\\\':
            p = '\\\\' + p
        components = p.split('\\')
        return urllib.quote(('/').join(components))
    comp = p.split(':')
    if len(comp) != 2 or len(comp[0]) > 1:
        error = 'Bad path: ' + p
        raise IOError, error
    drive = urllib.quote(comp[0].upper())
    components = comp[1].split('\\')
    path = '///' + drive + ':'
    for comp in components:
        if comp:
            path = path + '/' + urllib.quote(comp)

    return path