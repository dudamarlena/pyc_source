# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/dd/acceptcriteria/accept_all.py
# Compiled at: 2013-04-04 15:36:37
"""Criterion that accepts all drops anywhere on the component."""
from muntjac.event.dd.acceptcriteria.client_side_criterion import ClientSideCriterion

class AcceptAll(ClientSideCriterion):
    """Criterion that accepts all drops anywhere on the component.

    Note! Class is singleton, use L{get} method to get the instance.
    """
    _singleton = None

    def __init__(self):
        pass

    @classmethod
    def get(cls):
        return cls._singleton

    def accept(self, dragEvent):
        return True

    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.AcceptAll'


AcceptAll._singleton = AcceptAll()