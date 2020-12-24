# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__unit_test__/ally/core/impl/processor/method_invoker.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jun 21, 2012

@package: ally core
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Method invoker testing.
"""
import package_extender
package_extender.PACKAGE_EXTENDER.setForUnitTest(True)
from ally.container import ioc
from ally.core.http.impl.processor.method_invoker import MethodInvokerHandler
from ally.core.impl.node import NodeRoot
from ally.core.spec.resources import Invoker, Path
from ally.design.processor.attribute import defines
from ally.design.processor.context import Context, create
from ally.design.processor.execution import Chain
from ally.design.processor.spec import Resolvers
from ally.http.spec.server import HTTP_GET
import unittest

class Request(Context):
    """
    The request context.
    """
    method = defines(str)
    path = defines(Path)
    invoker = defines(Invoker, doc='\n    @rtype: Invoker\n    The invoker to be used for calling the service.\n    ')


class Response(Context):
    """
    The response context.
    """
    code = defines(str)
    status = defines(int)
    isSuccess = defines(bool)
    allows = defines(list, doc='\n    @rtype: list[string]\n    Contains the allow list for the methods.\n    ')


ctx = create(Resolvers(contexts=dict(Request=Request, Response=Response)))
Request, Response = ctx['Request'], ctx['Response']

class TestMethodInvoker(unittest.TestCase):

    def testMethodInvoker(self):
        handler = MethodInvokerHandler()
        ioc.initialize(handler)
        request, response = Request(), Response()
        node = NodeRoot()
        request.method, request.path = HTTP_GET, Path([], node)

        def callProcess(chain, **keyargs):
            handler.process(**keyargs)

        chain = Chain([callProcess])
        chain.process(request=request, response=response).doAll()
        self.assertEqual(response.allows, [])
        self.assertTrue(response.isSuccess is False)


if __name__ == '__main__':
    unittest.main()