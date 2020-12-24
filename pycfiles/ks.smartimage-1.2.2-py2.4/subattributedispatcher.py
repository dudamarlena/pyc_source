# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/smartimage/subattributedispatcher/subattributedispatcher.py
# Compiled at: 2008-12-23 17:55:56
"""The subattributeeventdispatcher

$Id: subattributedispatcher.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Andrey Orlov'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__credits__ = 'Andrey Orlov, for idea and common control'
import zope.component
from zope.app.container.interfaces import IContained
from ks.smartimage.interfaces import ISmartImage
import logging
logger = logging.getLogger('ks.smartimage')

def dispatchToSubattributes(object, event):
    for (key, value) in object.__dict__.items():
        if key[0] != '_':
            logger.debug('SMARTIMAGE KEY: %s', key)
            if ISmartImage.providedBy(value):
                logger.debug('Ok')
                for ignored in zope.component.subscribers((value, event), None):
                    pass

    return