# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/gateway/root_uri.py
# Compiled at: 2013-10-04 10:48:33
"""
Created on Aug 13, 2013

@package: gateway acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Processor that provides the root URI.
"""
from ally.container.ioc import injected
from ally.design.processor.attribute import defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessor

class Solicit(Context):
    """
    The solicit context.
    """
    rootURI = defines(str, doc='\n    @rtype: string\n    The root URI path to use for generated paths.\n    ')


@injected
class RootURIHandler(HandlerProcessor):
    """
    Provides the root URI items to be used for generated paths.
    """
    rootURI = str

    def __init__(self):
        assert isinstance(self.rootURI, str), 'Invalid root URI %s' % self.rootURI
        super().__init__()

    def process(self, chain, solicit: Solicit, **keyargs):
        """
        @see: HandlerProcessor.process
        
        Populate the roor URI.
        """
        assert isinstance(solicit, Solicit), 'Invalid solicit %s' % solicit
        solicit.rootURI = self.rootURI.strip('/')