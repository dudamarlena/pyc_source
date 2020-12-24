# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/vocabularies.py
# Compiled at: 2008-06-20 09:35:26
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from easyshop.core.interfaces import IShopManagement
from Products.CMFPlone.utils import safe_unicode

def countries(context):
    """
    """
    terms = []
    for country in IShopManagement(context).getShop().getCountries():
        terms.append(SimpleTerm(country, country))

    return SimpleVocabulary(terms)