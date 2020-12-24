# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/static_right.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jun 7, 2013\n\n@package: support acl\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProcessor that adds static rights.\n'
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