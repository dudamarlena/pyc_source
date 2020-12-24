# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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