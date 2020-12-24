# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/kitchentools.py
# Compiled at: 2006-09-21 05:27:35
import os.path
from persistent import Persistent
from zope.interface import implements, alsoProvides
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from worldcookery.interfaces import IKitchenTools, ILocalKitchenTools

class KitchenToolsFromFile(object):
    """Kitchen tools utility that reads data from a file
    """
    __module__ = __name__
    implements(IKitchenTools)

    @property
    def kitchen_tools(self):
        file_name = os.path.join(os.path.dirname(__file__), 'kitchentools.dat')
        for line in file(file_name):
            if line.strip():
                yield line.strip().decode('utf-8')


class LocalKitchenTools(Persistent):
    """Local, persistent kitchen tools utility
    """
    __module__ = __name__
    implements(ILocalKitchenTools)
    __name__ = __parent__ = None
    kitchen_tools = []


def kitchenToolVocabulary(context):
    utility = getUtility(IKitchenTools)
    return SimpleVocabulary.fromValues(utility.kitchen_tools)


alsoProvides(kitchenToolVocabulary, IVocabularyFactory)
from zope.component import adapter
from worldcookery.interfaces import INewWorldCookerySiteEvent

@adapter(INewWorldCookerySiteEvent)
def createLocalKitchenTools(event):
    kitchentools = LocalKitchenTools()
    previous = getUtility(IKitchenTools)
    kitchentools.kitchen_tools = list(previous.kitchen_tools)
    sm = event.object.getSiteManager()
    sm['kitchentools'] = kitchentools
    sm.registerUtility(kitchentools, ILocalKitchenTools)