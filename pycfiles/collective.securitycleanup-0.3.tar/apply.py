# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/sectionsubskin/apply.py
# Compiled at: 2008-07-18 06:49:04
from zope.interface import alsoProvides
try:
    from zope.interface import noLongerProvides
except ImportError:
    from Products.Five.utilities.marker import erase as noLongerProvides

from zope.component import getAllUtilitiesRegisteredFor
from collective.sectionsubskin.interfaces import ISubskinDefinition

def applyinterface(obj, event):
    """Mark the request with the correct subskin.
    """
    oldroot = event.request.get('subskin_root', None)
    if oldroot is not None:
        event.request.set('subskin_root', None)
        for layer in getAllUtilitiesRegisteredFor(ISubskinDefinition):
            layer = layer.type_interface
            if layer.providedBy(oldroot):
                noLongerProvides(event.request, layer)

    for layer in getAllUtilitiesRegisteredFor(ISubskinDefinition):
        layer = layer.type_interface
        if layer.providedBy(obj):
            alsoProvides(event.request, layer)
            try:
                event.request.set('subskin_root', obj)
            except TypeError:
                raise

    return