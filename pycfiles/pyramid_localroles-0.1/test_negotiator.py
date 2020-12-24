# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_negotiator.py
# Compiled at: 2014-05-04 12:45:31
__doc__ = 'Locale negotiator related tests.'
from pyramid_localize.negotiator import locale_negotiator

def test_negotiate_attr(locale_negotiator_request):
    """Locale_negotiator - negotiate locale from request attribute."""
    locale = locale_negotiator(locale_negotiator_request)
    assert locale == 'fr'


def test_negotiate_path(locale_negotiator_request):
    """Locale_negotiator - negotiate locale from path."""
    locale_negotiator_request._LOCALE_ = None
    locale = locale_negotiator(locale_negotiator_request)
    assert locale == 'pl'
    return


def test_negotiate_cookie(locale_negotiator_request):
    """locale_negotiator - negotiate locale from cookie."""
    locale_negotiator_request._LOCALE_ = None
    locale_negotiator_request.path = '/page'
    locale = locale_negotiator(locale_negotiator_request)
    assert locale == 'cz'
    return


def test_negotiate_headers(locale_negotiator_request):
    """
    Locale_negotiator:header.

    Negotiate locale from a header.
    """
    locale_negotiator_request._LOCALE_ = None
    locale_negotiator_request.path = '/page'
    locale_negotiator_request.cookies = {}
    locale = locale_negotiator(locale_negotiator_request)
    assert locale == 'de'
    return


def test_negotiate_default(locale_negotiator_request):
    """
    Locale_negotiator:default.

    Other ways fail, return default locale.
    """
    locale_negotiator_request.path = '/page'
    locale_negotiator_request._LOCALE_ = None
    locale_negotiator_request.cookies = {}
    locale_negotiator_request.accept_language = None
    locale = locale_negotiator(locale_negotiator_request)
    assert locale == 'en'
    return