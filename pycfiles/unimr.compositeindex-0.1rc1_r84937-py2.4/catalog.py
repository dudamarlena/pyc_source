# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/unimr/compositeindex/catalog.py
# Compiled at: 2009-04-22 12:10:04
import logging
from Acquisition import aq_parent
from Products.ZCatalog.Catalog import Catalog
from CompositeIndex import compositeSearchArgumentsMap
from wrapper import wrap_method, call
from config import PROJECTNAME
logger = logging.getLogger(PROJECTNAME)

def search(self, request, sort_index=None, reverse=0, limit=None, merge=1):
    compositeSearchArgumentsMap(self, request)
    return call(self, 'search', request, sort_index=sort_index, reverse=reverse, limit=limit, merge=merge)


def patch(scope, original, replacement):
    wrap_method(scope, original, replacement)