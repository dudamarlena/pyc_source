# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/static_right.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jun 7, 2013

@package: support acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Processor that adds static rights.
"""
from acl.spec import RightAcl
from ally.container.ioc import injected
from ally.design.processor.attribute import defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from collections import Iterable
import itertools

class Solicitation(Context):
    """
    The solicitation context.
    """
    rights = defines(Iterable, doc='\n    @rtype: Iterable(RightAcl)\n    The static rights for the types.\n    ')


@injected
class RegisterStaticRights(HandlerProcessorProceed):
    """
    The handler that populates static rights.
    """
    rights = list

    def __init__(self):
        assert isinstance(self.rights, list), 'Invalid static rights %s' % self.rights
        for right in self.rights:
            if not isinstance(right, RightAcl):
                raise AssertionError('Invalid right %s' % right)

        super().__init__()

    def process(self, solicitation: Solicitation, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Adds the default rights.
        """
        assert isinstance(solicitation, Solicitation), 'Invalid solicitation %s' % solicitation
        if solicitation.rights is not None:
            solicitation.rights = itertools.chain(solicitation.rights, self.rights)
        else:
            solicitation.rights = iter(self.rights)
        return