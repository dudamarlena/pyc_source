# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/ModelRssObject.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 1100 bytes
"""
Created on Nov 11, 2010

@author: Mark V Systems Limited
(c) Copyright 2010 Mark V Systems Limited, All rights reserved.
"""
import os
from arelle import XmlUtil
from arelle.ModelDocument import ModelDocument, Type

class ModelRssObject(ModelDocument):
    __doc__ = '\n    .. class:: ModelRssObject(type=ModelDocument.Type.RSSFEED, uri=None, filepath=None, xmlDocument=None)\n    \n    ModelRssObject is a specialization of ModelDocument for RSS Feeds.\n    \n    (for parameters and inherited attributes, please see ModelDocument)\n    '

    def __init__(self, modelXbrl, type=Type.RSSFEED, uri=None, filepath=None, xmlDocument=None):
        super(ModelRssObject, self).__init__(modelXbrl, type, uri, filepath, xmlDocument)
        self.rssItems = []

    def rssFeedDiscover(self, rootElement):
        """Initiates discovery of RSS feed
        """
        self.xmlRootElement = rootElement
        for itemElt in XmlUtil.descendants(rootElement, None, 'item'):
            self.rssItems.append(itemElt)