# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/dd/acceptcriteria/client_side_criterion.py
# Compiled at: 2013-04-04 15:36:37
"""Parent class for criteria that can be completely validated on client
side."""
from muntjac.event.dd.acceptcriteria.accept_criterion import IAcceptCriterion
from muntjac.util import clsname

class ClientSideCriterion(IAcceptCriterion):
    """Parent class for criteria that can be completely validated on client
    side. All classes that provide criteria that can be completely validated
    on client side should extend this class.

    It is recommended that subclasses of ClientSideCriterion re-validate the
    condition on the server side in L{IAcceptCriterion.accept} after
    the client side validation has accepted a transfer.
    """

    def isClientSideVerifiable(self):
        return True

    def paint(self, target):
        target.startTag('-ac')
        target.addAttribute('name', self.getIdentifier())
        self.paintContent(target)
        target.endTag('-ac')

    def paintContent(self, target):
        pass

    def getIdentifier(self):
        return clsname(self.__class__)

    def paintResponse(self, target):
        pass