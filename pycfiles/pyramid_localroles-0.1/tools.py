# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_localize/tools.py
# Compiled at: 2014-05-04 12:45:31
__doc__ = 'methods in this module are tools, thank to which pyramid_localize works most of its magic.'
import sys, os, logging
from translationstring import _interp_regex
from pyramid.i18n import make_localizer
from pyramid.i18n import TranslationString
from pyramid.asset import resolve_asset_spec
from pyramid.path import package_path
from pyramid.interfaces import ILocalizer
from pyramid.interfaces import ITranslationDirectories
from pyramid.compat import text_type
logger = logging.getLogger(__name__)

def set_localizer(request, reset=False):
    """
    Set localizer and auto_translate methods for request.

    :param pyramid.request.Request request: request object
    :param bool reset: flag that directs resetting localizer within app
    """
    if reset:
        for locale in request.registry['config'].localize.locales.available:
            logger.debug(('Resetting {0} localizator').format(locale))
            tdirs = request.registry.queryUtility(ITranslationDirectories, default=[])
            localizer = make_localizer(locale, tdirs)
            request.registry.registerUtility(localizer, ILocalizer, name=locale)

    def auto_translate(*args, **kwargs):
        if len(args) <= 1 and 'domain' not in kwargs:
            kwargs['domain'] = request.registry['config'].localize.domain
        return request.localizer.translate(TranslationString(*args, **kwargs))

    request._ = auto_translate


def destination_path(request):
    """
    Return absolute path of the translation destination.

    :param pyramid.request.Request request: a request object

    :returns: A combined translation destination path
    :rtype: str
    """
    (package_name, filename) = resolve_asset_spec(request.registry['config'].localize.translation.destination)
    if package_name is None:
        directory = filename
    else:
        __import__(package_name)
        package = sys.modules[package_name]
        directory = os.path.join(package_path(package), filename)
    return directory


def dummy_autotranslate(msgid, domain=None, default=None, mapping=None):
    """
    Method that simulate autotranslate.

    :param str msgid: Message or message id
    :param str domain: Translation domain
    :param str default: Default message
    :param dict mapping: Mapping dictionary for message variables

    :returns: *translated* string
    :rtype: str
    """
    tstr = None
    if default:
        tstr = default
    else:
        tstr = msgid
    if mapping and tstr:

        def replace(match):
            (whole, param1, param2) = match.groups()
            return text_type(mapping.get(param1 or param2, whole))

        tstr = _interp_regex.sub(replace, tstr)
    return tstr