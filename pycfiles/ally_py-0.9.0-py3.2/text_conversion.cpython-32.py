# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__unit_test__/ally/core/impl/processor/text_conversion.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jun 21, 2012

@package: ally core
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Text conversion testing.
"""
import package_extender
package_extender.PACKAGE_EXTENDER.setForUnitTest(True)
from ally.container import ioc
from ally.core.impl.processor.text_conversion import ConversionSetHandler
from ally.core.spec.resources import Normalizer, Converter
from ally.design.processor.attribute import defines
from ally.design.processor.context import Context, create
from ally.design.processor.execution import Chain
from ally.design.processor.spec import Resolvers
import unittest

class Content(Context):
    normalizer = defines(Normalizer)
    converter = defines(Converter)


ctx = create(Resolvers(contexts=dict(Content=Content)))
Content = ctx['Content']

class TestTextConversion(unittest.TestCase):

    def testTextConversion(self):
        handler = ConversionSetHandler()
        handler.normalizer = Normalizer()
        handler.converter = Converter()
        ioc.initialize(handler)
        requestCnt, response = Content(), Content()

        def callProcess(chain, **keyargs):
            handler.process(**keyargs)

        chain = Chain([callProcess])
        chain.process(requestCnt=requestCnt, response=response).doAll()
        self.assertEqual(handler.normalizer, requestCnt.normalizer)
        self.assertEqual(handler.normalizer, response.normalizer)
        self.assertEqual(handler.converter, response.converter)
        self.assertEqual(handler.converter, response.converter)


if __name__ == '__main__':
    unittest.main()