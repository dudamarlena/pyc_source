# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/dd/acceptcriteria/or_.py
# Compiled at: 2013-04-04 15:36:37
"""A compound criterion that accepts the drag if any of its criterion
accepts it."""
from muntjac.event.dd.acceptcriteria.client_side_criterion import ClientSideCriterion

class Or(ClientSideCriterion):
    """A compound criterion that accepts the drag if any of its criterion
    accepts it.

    @see: And
    """

    def __init__(self, *criteria):
        """@param criteria:
                   the criteria of which the Or criteria will be composed
        """
        self._criteria = criteria

    def paintContent(self, target):
        super(Or, self).paintContent(target)
        for crit in self._criteria:
            crit.paint(target)

    def accept(self, dragEvent):
        for crit in self._criteria:
            if crit.accept(dragEvent):
                return True

        return False

    def getIdentifier(self):
        return 'com.vaadin.event.dd.acceptcriteria.Or'