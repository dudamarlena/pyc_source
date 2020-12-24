# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/plonepatches/pts.py
# Compiled at: 2008-07-07 05:03:02
import os, logging
from Products.PlacelessTranslationService.memoize import memoize_second
from zope.i18n.negotiator import Negotiator
Negotiator.getLanguage = memoize_second(Negotiator.getLanguage)
from Products.PlacelessTranslationService.load import PTS_LANGUAGES
if PTS_LANGUAGES is not None:
    from zope.i18n import gettextmessagecatalog
    from Products.PlacelessTranslationService.lazycatalog import LazyGettextMessageCatalog
    gettextmessagecatalog.GettextMessageCatalog = LazyGettextMessageCatalog
from Products.PlacelessTranslationService.load import _compile_locales_dir
from zope.i18n.gettextmessagecatalog import GettextMessageCatalog
from zope.i18n.testmessagecatalog import TestMessageCatalog
from zope.i18n.translationdomain import TranslationDomain
from zope.i18n.interfaces import ITranslationDomain
from zope.component import queryUtility
from zope.component import getGlobalSiteManager
from Products.PlacelessTranslationService.interfaces import IPTSTranslationDomain
from Products.PlacelessTranslationService.PlacelessTranslationService import PlacelessTranslationService as PTS
from Products.PlacelessTranslationService.GettextMessageCatalog import BrokenMessageCatalog, _moCache

def addCatalogDecorator(func):

    def z3_addCatalog(self, catalog):
        func(self, catalog)
        if isinstance(catalog, BrokenMessageCatalog):
            return
        _moCache.cachedPoFile(catalog)
        domains = {catalog.getDomain(): {catalog.getLanguage(): _moCache.getPath(catalog)}}
        doRegisterTranslations(domains)

    return z3_addCatalog


PTS.addCatalog = addCatalogDecorator(PTS.addCatalog)
PTS.reloadCatalog = addCatalogDecorator(PTS.reloadCatalog)

def patched_registerTranslations(_context, directory):
    _compile_locales_dir(directory)
    path = os.path.normpath(directory)
    domains = {}
    for language in os.listdir(path):
        lc_messages_path = os.path.join(path, language, 'LC_MESSAGES')
        if os.path.isdir(lc_messages_path):
            for domain_file in os.listdir(lc_messages_path):
                if domain_file.endswith('.mo'):
                    domain_path = os.path.join(lc_messages_path, domain_file)
                    domain = domain_file[:-3]
                    if domain not in domains:
                        domains[domain] = {}
                    domains[domain][language] = domain_path

    if domains != {}:
        _context.action(('i18n', directory), doRegisterTranslations, args=(domains,))


def doRegisterTranslations(domains):
    for (name, langs) in domains.items():
        domain = queryUtility(ITranslationDomain, name)
        if domain is None or IPTSTranslationDomain.providedBy(domain):
            domain = TranslationDomain(name)
            domain.addCatalog(TestMessageCatalog(name))
            gsm = getGlobalSiteManager()
            gsm.registerUtility(domain, name=name)
        for (lang, file_path) in langs.items():
            domain.addCatalog(GettextMessageCatalog(lang, name, file_path))

    return


LOG = logging.getLogger(__name__)
LOG.info('Patching zope.i18n.zcml.registerTranslations via our configure.zcml')