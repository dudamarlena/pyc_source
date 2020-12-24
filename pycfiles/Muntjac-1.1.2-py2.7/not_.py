# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/dd/acceptcriteria/not_.py
# Compiled at: 2013-04-04 15:36:37
"""Criterion that wraps another criterion and inverts its return value."""
from muntjac.event.dd.acceptcriteria.client_side_criterion import ClientSideCriterion

class Not(ClientSideCriterion):
    """Criterion that wraps another criterion and inverts its return value.
    """

    def __init__(self, acceptCriterion):
        self._acceptCriterion = acceptCriterion

    def paintContent(self, target):
        super(Not, self).paintContent(target)
        self._acceptCriterion.paint(target)

    def accept(self, dragEvent):
        return not self._acceptCriterion.accept(dragEvent)

    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.Not'