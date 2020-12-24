# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/plone-py2.6/collective/behavior.localregistry/src/collective/behavior/localregistry/interfaces.py
# Compiled at: 2013-04-14 13:39:36
from zope.interface import Interface

class ILocalRegistryCreatedEvent(Interface):
    """An event that is fired after a local registry is created
    """
    pass