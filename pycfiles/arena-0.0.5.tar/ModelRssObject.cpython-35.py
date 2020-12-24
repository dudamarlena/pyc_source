# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/ModelRssObject.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 1100 bytes
__doc__ = '\nCreated on Nov 11, 2010\n\n@author: Mark V Systems Limited\n(c) Copyright 2010 Mark V Systems Limited, All rights reserved.\n'
import os
from arelle import XmlUtil
from arelle.ModelDocument import ModelDocument, Type

class ModelRssObject(ModelDocument):
    """ModelRssObject"""

    def __init__(self, modelXbrl, type=Type.RSSFEED, uri=None, filepath=None, xmlDocument=None):
        super(ModelRssObject, self).__init__(modelXbrl, type, uri, filepath, xmlDocument)
        self.rssItems = []

    def rssFeedDiscover(self, rootElement):
        """Initiates discovery of RSS feed
        """
        self.xmlRootElement = rootElement
        for itemElt in XmlUtil.descendants(rootElement, None, 'item'):
            self.rssItems.append(itemElt)