# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/pluggablecatalog/setuphandlers.py
# Compiled at: 2008-07-23 17:53:25
import Acquisition
from Products.CMFCore.utils import getToolByName
from Products.pluggablecatalog import tool
import logging
logger = logging.getLogger(__name__)

def replaceCatalog(context):
    if context.readDataFile('pluggablecatalog-default.txt') is None:
        return
    site = context.getSite()
    catalog = getToolByName(site, 'portal_catalog')
    if not isinstance(Acquisition.aq_base(catalog), tool.CatalogTool):
        catalog.__class__ = tool.CatalogTool
    return