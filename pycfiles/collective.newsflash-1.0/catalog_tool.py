# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/uittenbroek/Projects/buildout-nuffic/src/collective.newrelic/collective/newrelic/patches/catalog_tool.py
# Compiled at: 2013-12-24 05:41:42
import newrelic.agent, newrelic.api
from Products.CMFPlone.CatalogTool import CatalogTool
from collective.newrelic.utils import logger
CatalogTool.original_cmfplone_catalogtool_searchResults = CatalogTool.searchResults

def newrelic_searchResults(self, REQUEST=None, **kw):
    trans = newrelic.agent.current_transaction()
    with newrelic.api.database_trace.DatabaseTrace(trans, str(kw), self):
        result = self.original_cmfplone_catalogtool_searchResults(REQUEST, **kw)
    return result


CatalogTool.searchResults = newrelic_searchResults
logger.info('Patched Products.CMFPlone.CatalogTool:CatalogTool.searchResults with instrumentation')