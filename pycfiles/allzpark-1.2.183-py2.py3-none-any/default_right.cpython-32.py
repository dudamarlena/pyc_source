# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/default_right.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 21, 2013\n\n@package: support acl\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProcessor that adds default rights from the ACL types.\n'
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