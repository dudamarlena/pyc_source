# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/plone-py2.6/collective/behavior.localregistry/src/collective/behavior/localregistry/behavior.py
# Compiled at: 2013-04-14 13:40:18
from zope.interface import Interface

class ILocalRegistry(Interface):
    """Dexterity behavior to add a local plone.app.registry for content types,
    it adds a local component with a layered proxy registry.
    """
    pass