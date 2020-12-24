# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/parse/headers.py
# Compiled at: 2015-11-05 10:40:17
__doc__ = "Parsers for HTTP and Email headers.\n\n.. py:module:: bridgedb.parse.headers\n    :synopsis: Parsers for HTTP and Email headers.\n\nbridgedb.parse.headers\n=======================\n::\n\n parseAcceptLanguage - Parse the contents of a client 'Accept-Language' header\n..\n"

def parseAcceptLanguage(header):
    """Parse the contents of a client 'Accept-Language' header.

    Parse the header in the following manner:

    1. If ``header`` is None or an empty string, return an empty list.
    2. Split the ``header`` string on any commas.
    3. Chop of the RFC2616 quality/level suffix. We ignore these, and just
       use the order of the list as the preference order, without any
       parsing of quality/level assignments.
    4. Add a fallback language of the same type if it is missing. For
       example, if we only got ['es-ES', 'de-DE'], add 'es' after 'es-ES'
       and add 'de' after 'de-DE'.
    5. Change all hyphens to underscores.

    :param string header: The contents of an 'Accept-Language' header, i.e. as
        if taken from :api:`twisted.web.server.Request.getHeader`.
    :rtype: list
    :returns: A list of language codes (with and without locales), in order of
        preference.
    """
    langs = []
    if not header:
        return langs
    langHeader = header.split(',')
    for lang in langHeader:
        if lang.find(';') != -1:
            code, _ = lang.split(';')
            langs.append(code)
        else:
            langs.append(lang)

    langsWithLocales = filter(lambda x: '-' in x, langs)
    langsOnly = map(lambda x: x.split('-')[0], langsWithLocales)
    for only in langsOnly:
        if only not in langs:
            insertAfter = filter(lambda x: x.startswith(only), [ x for x in langs ])
            if insertAfter:
                placement = langs.index(insertAfter[0]) + 1
                langs.insert(placement, only)
                continue
            langs.append(only)

    langs = map(lambda x: x.replace('-', '_'), [ x for x in langs ])
    return langs