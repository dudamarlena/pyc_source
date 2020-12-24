# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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