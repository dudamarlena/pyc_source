# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/generations/evolve3.py
# Compiled at: 2013-11-19 07:06:50
import logging
logger = logging.getLogger('ztfy.thesaurus')
from transaction.interfaces import ITransactionManager
from zope.component.interfaces import ISite
from zope.intid.interfaces import IIntIds
from ztfy.thesaurus.interfaces.thesaurus import IThesaurus
from zope.app.publication.zopepublication import ZopePublication
from zope.component import getUtility, getUtilitiesFor
from zope.site import hooks
from ztfy.utils.catalog import indexObject

def evolve(context):
    """this useless update has been removed - see evolve4"""
    pass