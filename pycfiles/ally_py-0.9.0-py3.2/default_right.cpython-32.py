# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/default_right.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Feb 21, 2013

@package: support acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Processor that adds default rights from the ACL types.
"""
from acl.spec import TypeAcl
from ally.container.ioc import injected
from ally.container.support import setup
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed, Handler
from collections import Iterable
import itertools

class Solicitation(Context):
    """
    The solicitation context.
    """
    types = requires(Iterable, doc='\n    @rtype: Iterable(TypeAcl)\n    The ACL types to add the default rights for.\n    ')
    rights = defines(Iterable, doc='\n    @rtype: Iterable(RightAcl)\n    The default rights for the types.\n    ')


@injected
@setup(Handler, name='registerDefaultRights')
class RegisterDefaultRights(HandlerProcessorProceed):
    """
    Provides the handler that populates the default rights for ACL types.
    """

    def process(self, solicitation: Solicitation, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Adds the default rights.
        """
        assert isinstance(solicitation, Solicitation), 'Invalid solicitation %s' % solicitation
        if solicitation.types is None:
            return
        else:
            rights = []
            for typeAcl in solicitation.types:
                assert isinstance(typeAcl, TypeAcl), 'Invalid ACL type %s' % typeAcl
                rights.extend(typeAcl.defaults)

            if solicitation.rights is not None:
                solicitation.rights = itertools.chain(solicitation.rights, rights)
            else:
                solicitation.rights = rights
            return