# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/plone-py2.6/collective/behavior.localregistry/src/collective/behavior/localregistry/interfaces.py
# Compiled at: 2013-04-14 13:39:36
from zope.interface import Interface

class ILocalRegistryCreatedEvent(Interface):
    """An event that is fired after a local registry is created
    """