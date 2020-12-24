# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.microblog/plonesocial/microblog/migration.py
# Compiled at: 2014-03-11 12:09:55
from zope.component import queryUtility
from plonesocial.microblog.interfaces import IMicroblogTool
from BTrees import OOBTree
import logging
logger = logging.getLogger('plonesocial.microblog.migration')
from transaction import commit

def setup_uuid_mapping(context):
    """0.5 adds a new index"""
    tool = queryUtility(IMicroblogTool)
    if not hasattr(tool, '_uuid_mapping'):
        logger.info('Adding missing UUID mapping to %s' % repr(tool))
        tool._uuid_mapping = OOBTree.OOBTree()
        commit()