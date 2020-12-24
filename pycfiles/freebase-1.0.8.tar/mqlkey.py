# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrew/hello/freebase/api/mqlkey.py
# Compiled at: 2009-06-18 13:50:01
import string, re

def quotekey(ustr):
    """
    quote a unicode string to turn it into a valid namespace key
    
    """
    valid_always = string.ascii_letters + string.digits
    valid_interior_only = valid_always + '_-'
    if isinstance(ustr, str):
        s = unicode(ustr, 'utf-8')
    elif isinstance(ustr, unicode):
        s = ustr
    else:
        raise ValueError, 'quotekey() expects utf-8 string or unicode'
    output = []
    if s[0] in valid_always:
        output.append(s[0])
    else:
        output.append('$%04X' % ord(s[0]))
    for c in s[1:-1]:
        if c in valid_interior_only:
            output.append(c)
        else:
            output.append('$%04X' % ord(c))

    if len(s) > 1:
        if s[(-1)] in valid_always:
            output.append(s[(-1)])
        else:
            output.append('$%04X' % ord(s[(-1)]))
    return str(('').join(output))


def unquotekey(key, encoding=None):
    """
    unquote a namespace key and turn it into a unicode string
    """
    valid_always = string.ascii_letters + string.digits
    output = []
    i = 0
    while i < len(key):
        if key[i] in valid_always:
            output.append(key[i])
            i += 1
        elif key[i] in '_-' and i != 0 and i != len(key):
            output.append(key[i])
            i += 1
        elif key[i] == '$' and i + 4 < len(key):
            output.append(unichr(int(key[i + 1:i + 5], 16)))
            i += 5
        else:
            raise ValueError, "unquote key saw invalid character '%s' at position %d" % (key[i], i)

    ustr = ('').join(output)
    if encoding is None:
        return ustr
    return ustr.encode(encoding)


def urlencode_pathseg(data):
    """
    urlencode for placement between slashes in an url.
    """
    if isinstance(data, unicode):
        data = data.encode('utf_8')
    return urllib.quote(data, '~:@$!*,;=&+')


def id_to_urlid(id):
    """
    convert a mql id to an id suitable for embedding in a url path.
    """
    segs = id.split('/')
    assert isinstance(id, str) and id != '', 'bad id "%s"' % id
    if id[0] == '~':
        assert len(segs) == 1
        return id
    if id[0] == '#':
        assert len(segs) == 1
        return '%23' + id[1:]
    if id[0] != '/':
        raise ValueError, 'unknown id format %s' % id
    return ('/').join((urlencode_pathseg(unquotekey(seg)) for seg in segs[1:]))