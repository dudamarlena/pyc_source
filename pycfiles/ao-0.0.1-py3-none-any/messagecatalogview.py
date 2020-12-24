# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/anz/dashboard/browser/messagecatalogview.py
# Compiled at: 2010-09-26 21:53:54
import cjson
from Products.Five import BrowserView
from zope.interface import implements
from zope.component import queryUtility, getUtility
from zope.i18n.interfaces import ITranslationDomain
from zope.i18n.interfaces import IFallbackTranslationDomainFactory
from zope.i18n.interfaces import INegotiator
from anz.dashboard import MSG_FACTORY as _
from anz.dashboard.interfaces import IMessageCatalogView

class MessageCatalogView(BrowserView):
    """ Provide functions to return message catalog. """
    __module__ = __name__
    implements(IMessageCatalogView)

    def catalogMapping(self, domain, retJson=True):
        """ Return message catalog as a mapping.
        
        @param domain
        domain of the message catalog
        
        @param retJson
        format return value to json format or not( default True )
        
        @return
        a dict with the following format:
        {
            'success': True,
            'msg': 'Get message catalog mapping success.',
            'mapping': {
                u'text1': u'translated text1',
                u'text2': u'translated text2',
                ...
            }
        }
        
        """
        context = self.context
        request = self.request
        ret = {}
        try:
            texts = {}
            util = queryUtility(ITranslationDomain, domain)
            if util is None:
                util = queryUtility(IFallbackTranslationDomainFactory)
                if util is not None:
                    util = util(domain)
            if util is not None:
                langs = util._catalogs.keys()
                negotiator = getUtility(INegotiator)
                target_language = negotiator.getLanguage(langs, request)
                catalog_names = util._catalogs.get(target_language)
                if catalog_names:
                    if len(catalog_names) == 1:
                        if util._data[catalog_names[0]]._catalog is None:
                            util._data[catalog_names[0]].reload()
                        texts = util._data[catalog_names[0]]._catalog._catalog
                    else:
                        for name in catalog_names:
                            catalog = util._data[name]
                            if catalog._catalog is None:
                                catalog.reload()
                            texts = catalog._catalog._catalog
                            if texts:
                                break

            if texts:
                texts.update({'': 'META'})
                ret['success'] = True
                ret['msg'] = _('Get message catalog mapping success.')
            else:
                ret['success'] = False
                ret['msg'] = _('Get message catalog mapping failure.')
            ret['texts'] = texts
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)

        return retJson and cjson.encode(ret) or ret