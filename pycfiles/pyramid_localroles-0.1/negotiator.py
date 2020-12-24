# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_localize/negotiator.py
# Compiled at: 2014-05-04 12:45:31
__doc__ = 'Locale negotiator.'

def locale_negotiator(request):
    """
    Locale negotiator.

    It sets best suited locale variable for given user:

    1. Check for presence and value of **request._LOCALE_** value
    2. Then tries the address url, if the first part has locale indicator.
    3. It checks cookies, for value set here
    4. Tries to best match accepted language for browser user is visiting
        website with
    5. Defaults to **localize.locales.default** configuration setting value

    :param pyramid.request.Request request: a request object
    :returns: locale name
    :rtype: str
    """
    available_languages = request.registry['config'].localize.locales.available
    locale = request.registry['config'].localize.locales.default
    route_elements = request.path.split('/')
    if hasattr(request, '_LOCALE_') and request._LOCALE_ in available_languages:
        locale = request._LOCALE_
    elif len(route_elements[1]) == 2 and route_elements[1] in available_languages:
        locale = route_elements[1]
    elif request.cookies and '_LOCALE_' in request.cookies and request.cookies['_LOCALE_'] in available_languages:
        locale = request.cookies['_LOCALE_']
    elif request.accept_language:
        locale = request.accept_language.best_match(available_languages)
    return locale