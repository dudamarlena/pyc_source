# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/translations.py
# Compiled at: 2015-11-05 10:40:17
import gettext, logging, os, re
from bridgedb import _langs
from bridgedb import safelog
from bridgedb.parse import headers
TRANSLATIONS_DIR = os.path.join(os.path.dirname(__file__), 'i18n')

def getFirstSupportedLang(langs):
    """Return the first language in **langs** that we support.

    :param list langs: All requested languages
    :rtype: str
    :returns: A country code for the client's preferred language.
    """
    lang = 'en-US'
    supported = _langs.get_langs()
    for l in langs:
        if l in supported:
            lang = l
            break

    return lang


def getLocaleFromHTTPRequest(request):
    """Retrieve the languages from an HTTP ``Accept-Language:`` header.

    Parse the languages from the header, use them to install a
    ``gettext.translation`` chain via :func:`installTranslations`, and lastly
    return the requested languages.

    :type request: :api:`twisted.web.server.Request`
    :param request: An incoming request from a client.
    :rtype: list
    :returns: All requested languages.
    """
    header = request.getHeader('accept-language')
    if header is None:
        logging.debug("Client sent no 'Accept-Language' header. Using fallback.")
        header = 'en,en-US'
    langs = headers.parseAcceptLanguage(header)
    if not safelog.safe_logging:
        logging.debug('Client Accept-Language (top 5): %s' % langs[:5])
    chosenLang = request.args.get('lang', [None])[0]
    if chosenLang:
        logging.debug('Client requested language: %r' % chosenLang)
        langs.insert(0, chosenLang)
    installTranslations(langs)
    return langs


def getLocaleFromPlusAddr(address):
    """See whether the user sent his email to a 'plus' address, for instance to
    bridges+fa@bridges.torproject.org. Plus addresses are the current
    mechanism to set the reply language.
    """
    replyLocale = 'en'
    r = '.*(<)?(\\w+\\+(\\w+)@\\w+(?:\\.\\w+)+)(?(1)>)'
    match = re.match(r, address)
    if match:
        replyLocale = match.group(3)
    return replyLocale


def installTranslations(langs):
    """Create a ``gettext.translation`` chain for all **langs**.

    Attempt to install the first language in the **langs** list. If that
    fails, we receive a ``gettext.NullTranslation`` object, and if it worked
    then we have a ``gettext.GNUTranslation`` object. Whichever one we end up
    with, get the other languages and add them as fallbacks to the
    first. Lastly, install this chain of translations.

    :param list langs: A list of language codes.
    :returns: A ``gettext.NullTranslation`` or ``gettext.GNUTranslation`` with
        fallback languages set.
    """
    try:
        language = gettext.translation('bridgedb', localedir=TRANSLATIONS_DIR, languages=langs, fallback=True)
        for lang in langs:
            language.add_fallback(gettext.translation('bridgedb', localedir=TRANSLATIONS_DIR, languages=langs, fallback=True))

    except IOError as error:
        logging.error(error.message)

    language.install(unicode=True)
    return language


def usingRTLLang(langs):
    """Check if we should translate the text into a RTL language.

    Choose the first language from the **langs** list that we support and
    return True if it is a RTL language, else return False.

    :param list langs: An incoming request.
    :rtype: bool
    :returns: ``True`` if the preferred language is right-to-left; ``False``
        otherwise.
    """
    lang = getFirstSupportedLang(langs)
    if lang in _langs.RTL_LANGS:
        return True
    return False