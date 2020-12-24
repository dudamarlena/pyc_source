# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authopenid_middleware/parseurl.py
# Compiled at: 2009-10-29 02:02:05
import re, cgi, urllib

def parse_url(name):
    pattern = re.compile('\n            (?P<drivername>\\w+)://\n            (?:\n                (?P<user>[^:/]*)\n                (?::(?P<passwd>[^/]*))?\n            @)?\n            (?:\n                (?P<host>[^/:]*)\n                (?::(?P<port>[^/]*))?\n            )?\n            (?:/(?P<db>.*))?\n            ', re.X)
    m = pattern.match(name)
    if m is not None:
        components = m.groupdict()
        if components['db'] is not None:
            tokens = components['db'].split('?', 2)
            components['db'] = tokens[0]
            query = len(tokens) > 1 and dict(cgi.parse_qsl(tokens[1])) or None
            if query is not None:
                query = dict(((k.encode('ascii'), query[k]) for k in query))
        else:
            query = None
        components['query'] = query
        if components['passwd'] is not None:
            components['passwd'] = urllib.unquote_plus(components['passwd'])
        return components
    else:
        raise Exception("Could not parse rfc1738 URL from string '%s'" % name)
    return