# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/70/_7dmwj6x12q099dhb0z0p7p80000gn/T/pycharm-packaging/djangorestframework/rest_framework/utils/mediatypes.py
# Compiled at: 2018-05-14 04:48:23
# Size of source mod 2**32: 2712 bytes
"""
Handling of media types, as found in HTTP Content-Type and Accept headers.

See https://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.7
"""
from __future__ import unicode_literals
from django.http.multipartparser import parse_header
from django.utils.encoding import python_2_unicode_compatible
from rest_framework import HTTP_HEADER_ENCODING

def media_type_matches(lhs, rhs):
    """
    Returns ``True`` if the media type in the first argument <= the
    media type in the second argument.  The media types are strings
    as described by the HTTP spec.

    Valid media type strings include:

    'application/json; indent=4'
    'application/json'
    'text/*'
    '*/*'
    """
    lhs = _MediaType(lhs)
    rhs = _MediaType(rhs)
    return lhs.match(rhs)


def order_by_precedence(media_type_lst):
    """
    Returns a list of sets of media type strings, ordered by precedence.
    Precedence is determined by how specific a media type is:

    3. 'type/subtype; param=val'
    2. 'type/subtype'
    1. 'type/*'
    0. '*/*'
    """
    ret = [
     set(), set(), set(), set()]
    for media_type in media_type_lst:
        precedence = _MediaType(media_type).precedence
        ret[(3 - precedence)].add(media_type)

    return [media_types for media_types in ret if media_types]


@python_2_unicode_compatible
class _MediaType(object):

    def __init__(self, media_type_str):
        self.orig = '' if media_type_str is None else media_type_str
        self.full_type, self.params = parse_header(self.orig.encode(HTTP_HEADER_ENCODING))
        self.main_type, sep, self.sub_type = self.full_type.partition('/')

    def match(self, other):
        """Return true if this MediaType satisfies the given MediaType."""
        for key in self.params:
            if key != 'q':
                if other.params.get(key, None) != self.params.get(key, None):
                    return False

        if self.sub_type != '*':
            if other.sub_type != '*':
                if other.sub_type != self.sub_type:
                    return False
        if self.main_type != '*':
            if other.main_type != '*':
                if other.main_type != self.main_type:
                    return False
        return True

    @property
    def precedence(self):
        """
        Return a precedence level from 0-3 for the media type given how specific it is.
        """
        if self.main_type == '*':
            return 0
        else:
            if self.sub_type == '*':
                return 1
            if not self.params or list(self.params) == ['q']:
                return 2
            return 3

    def __str__(self):
        ret = '%s/%s' % (self.main_type, self.sub_type)
        for key, val in self.params.items():
            ret += '; %s=%s' % (key, val.decode('ascii'))

        return ret