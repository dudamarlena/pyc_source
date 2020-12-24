# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/urllib3/urllib3/packages/rfc3986/normalizers.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 5259 bytes
"""Module with functions to normalize components."""
import re
from . import compat
from . import misc

def normalize_scheme(scheme):
    """Normalize the scheme component."""
    return scheme.lower()


def normalize_authority(authority):
    """Normalize an authority tuple to a string."""
    userinfo, host, port = authority
    result = ''
    if userinfo:
        result += normalize_percent_characters(userinfo) + '@'
    if host:
        result += normalize_host(host)
    if port:
        result += ':' + port
    return result


def normalize_username(username):
    """Normalize a username to make it safe to include in userinfo."""
    return compat.urlquote(username)


def normalize_password(password):
    """Normalize a password to make safe for userinfo."""
    return compat.urlquote(password)


def normalize_host(host):
    """Normalize a host string."""
    if misc.IPv6_MATCHER.match(host):
        percent = host.find('%')
        if percent != -1:
            percent_25 = host.find('%25')
            if percent_25 == -1 or percent < percent_25 or percent == percent_25 and percent_25 == len(host) - 4:
                host = host.replace('%', '%25', 1)
            return host[:percent].lower() + host[percent:]
    return host.lower()


def normalize_path(path):
    """Normalize the path string."""
    if not path:
        return path
    else:
        path = normalize_percent_characters(path)
        return remove_dot_segments(path)


def normalize_query(query):
    """Normalize the query string."""
    if not query:
        return query
    else:
        return normalize_percent_characters(query)


def normalize_fragment(fragment):
    """Normalize the fragment string."""
    if not fragment:
        return fragment
    else:
        return normalize_percent_characters(fragment)


PERCENT_MATCHER = re.compile('%[A-Fa-f0-9]{2}')

def normalize_percent_characters(s):
    """All percent characters should be upper-cased.

    For example, ``"%3afoo%DF%ab"`` should be turned into ``"%3Afoo%DF%AB"``.
    """
    matches = set(PERCENT_MATCHER.findall(s))
    for m in matches:
        if not m.isupper():
            s = s.replace(m, m.upper())

    return s


def remove_dot_segments(s):
    """Remove dot segments from the string.

    See also Section 5.2.4 of :rfc:`3986`.
    """
    segments = s.split('/')
    output = []
    for segment in segments:
        if segment == '.':
            continue
        else:
            if segment != '..':
                output.append(segment)
            else:
                if output:
                    output.pop()

    if s.startswith('/'):
        if not output or output[0]:
            output.insert(0, '')
    if s.endswith(('/.', '/..')):
        output.append('')
    return '/'.join(output)


def encode_component(uri_component, encoding):
    """Encode the specific component in the provided encoding."""
    if uri_component is None:
        return uri_component
    else:
        percent_encodings = len(PERCENT_MATCHER.findall(compat.to_str(uri_component, encoding)))
        uri_bytes = compat.to_bytes(uri_component, encoding)
        is_percent_encoded = percent_encodings == uri_bytes.count(b'%')
        encoded_uri = bytearray()
        for i in range(0, len(uri_bytes)):
            byte = uri_bytes[i:i + 1]
            byte_ord = ord(byte)
            if is_percent_encoded and byte == b'%' or byte_ord < 128 and byte.decode() in misc.NON_PCT_ENCODED:
                encoded_uri.extend(byte)
            else:
                encoded_uri.extend('%{0:02x}'.format(byte_ord).encode().upper())

        return encoded_uri.decode(encoding)