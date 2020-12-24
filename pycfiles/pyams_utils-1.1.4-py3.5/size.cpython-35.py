# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/size.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 2381 bytes
"""PyAMS_utils.size module

This module provides a small function which can be used to convert
a "size" value, given in bytes, to it's "human" representation.
"""
from babel import UnknownLocaleError
from babel.core import Locale
from babel.numbers import format_decimal
from pyams_utils.request import check_request
__docformat__ = 'restructuredtext'
from pyams_utils import _

def get_human_size(value, request=None):
    """Convert given bytes value in human readable format

    >>> from pyramid.testing import DummyRequest
    >>> request = DummyRequest(params={'_LOCALE_': 'en'})
    >>> request.locale_name
    'en'
    >>> from pyams_utils.size import get_human_size
    >>> get_human_size(256, request)
    '256 bytes'
    >>> get_human_size(3678, request)
    '3.6 Kb'
    >>> get_human_size(6785342, request)
    '6.47 Mb'
    >>> get_human_size(3674815342, request)
    '3.422 Gb'
    >>> request = DummyRequest(params={'_LOCALE_': 'fr'})
    >>> request.locale_name
    'fr'
    >>> get_human_size(256, request)
    '256 bytes'
    >>> get_human_size(3678, request)
    '3,6 Kb'
    >>> get_human_size(6785342, request)
    '6,47 Mb'
    >>> get_human_size(3674815342, request)
    '3,422 Gb'
    """
    if request is None:
        request = check_request()
    translate = request.localizer.translate
    try:
        locale = Locale(request.locale_name)
    except UnknownLocaleError:
        locale = Locale(request.registry.settings.get('pyramid.default_locale_name', 'en'))

    if value < 1024:
        return format_decimal(value, translate(_('0 bytes')), locale)
    value /= 1024
    if value < 1024:
        return format_decimal(value, translate(_('0.# Kb')), locale)
    value /= 1024
    if value < 1024:
        return format_decimal(value, translate(_('0.0# Mb')), locale)
    value /= 1024
    return format_decimal(value, translate(_('0.0## Gb')), locale)