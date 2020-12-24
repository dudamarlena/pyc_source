# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\utils\uri.py
# Compiled at: 2020-02-23 02:01:40
"""
"""
try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote

from .. import SUBTREE, BASE, LEVEL

def parse_uri(uri):
    """
    Decode LDAP URI as specified in RFC 4516 relaxing specifications
    permitting 'ldaps' as scheme for ssl-ldap
    """
    uri_components = dict()
    parts = unquote(uri).split('?')
    (scheme, sep, remain) = parts[0].partition('://')
    if sep != '://' or scheme not in ('ldap', 'ldaps'):
        return
    else:
        (address, _, uri_components['base']) = remain.partition('/')
        uri_components['ssl'] = True if scheme == 'ldaps' else False
        (uri_components['host'], sep, uri_components['port']) = address.partition(':')
        if sep != ':':
            if uri_components['ssl']:
                uri_components['port'] = 636
            else:
                uri_components['port'] = None
        else:
            if not uri_components['port'].isdigit() or not 0 < int(uri_components['port']) < 65536:
                return
            uri_components['port'] = int(uri_components['port'])
        uri_components['attributes'] = parts[1].split(',') if len(parts) > 1 else None
        uri_components['scope'] = parts[2] if len(parts) > 2 else None
        if uri_components['scope'] == 'base':
            uri_components['scope'] = BASE
        elif uri_components['scope'] == 'sub':
            uri_components['scope'] = SUBTREE
        elif uri_components['scope'] == 'one':
            uri_components['scope'] = LEVEL
        elif uri_components['scope']:
            return
        uri_components['filter'] = parts[3] if len(parts) > 3 else None
        uri_components['extensions'] = parts[4].split(',') if len(parts) > 4 else None
        return uri_components