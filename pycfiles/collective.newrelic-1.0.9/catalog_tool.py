# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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