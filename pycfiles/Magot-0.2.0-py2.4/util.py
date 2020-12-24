# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/magot/util.py
# Compiled at: 2006-10-29 10:20:51
from itertools import chain
from peak.model import features
from peak.binding import attributes

def flatten(listOfLists):
    return list(chain(*listOfLists))


class NewAttribute(object):
    """ Attribute metadata that generates a new attribute whose name is '<attrName>suffix'. """
    __module__ = __name__

    def __init__(self, suffix):
        self.suffix = suffix


@attributes.declareAttribute.when(NewAttribute)
def _declareNewAttribute(classobj, attrname, metadata):

    class newAttr(features.Attribute):
        __module__ = __name__

    newAttrName = attrname + metadata.suffix
    newAttr.attrName = newAttr.__name__ = newAttrName
    newAttr.activateInClass(classobj, newAttrName)


class DerivedAndCached(features.Attribute):
    """ Attribute whose value is computed only if it's not already set. """
    __module__ = __name__

    def get(feature, element):
        try:
            return element.__dict__[feature.attrName]
        except KeyError:
            value = feature.compute(element)
            feature.set(element, value)
            return value

    def compute(feature, element):
        raise NotImplementedError


class Proxy(object):
    """ A Proxy class that delegates to an original object for all untouched attributes
        and stores overridden attributes. 
    """
    __module__ = __name__

    def __init__(self, obj):
        """The initializer."""
        super(Proxy, self).__init__(obj)
        self._obj = obj

    def __getattr__(self, attr):
        try:
            return self.__dict__[attr]
        except KeyError:
            return getattr(self._obj, attr)

    def getModifiedAttr(self, attr):
        modified = self.__dict__.get(attr, None)
        try:
            if modified != getattr(self._obj, attr):
                return modified
            else:
                return
        except AttributeError:
            return modified

        return

    def getOriginalObject(self):
        return self._obj


def pprintHierarchy(root):

    def printAccount(account, depth):
        if account.balance.amount != 0:
            print '\t' * depth + str(account).ljust(20) + str(account.balance).rjust(40 - 4 * depth)

    root.traverseHierarchy(printAccount, False)
    print '============================================================'