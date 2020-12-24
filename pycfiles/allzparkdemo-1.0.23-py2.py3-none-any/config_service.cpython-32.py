# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__unit_test__/ally/api/config/config_service.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Mar 20, 2012\n\n@package: ally api\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides unit testing for the decorated services.\n'
import package_extender
package_extender.PACKAGE_EXTENDER.setForUnitTest(True)
from .config_models import Entity, APIModel
from ally.api.config import service, call, GET
from ally.api.type import Integer, Number, String
import unittest

@service
class IServiceEntity:

    @call(Number, Entity.X, method=GET)
    def multipy(self, x=None):
        """
        """
        pass


@service((Entity, APIModel))
class IService(IServiceEntity):

    @call(None, Number, method=GET)
    def doNothing(self, x):
        """
        """
        pass

    @call(method=GET)
    def intToStr(self, x: Integer) -> String:
        """
        """
        pass


class ServiceImpl(IService):

    def multipy(self, x=None):
        if x is None:
            return 100000
        else:
            return x + x

    def intToStr(self, x):
        return str(x)

    def doNothing(self, x):
        pass

    def implCustom(self):
        """
        """
        pass


class TestConfigure(unittest.TestCase):

    def testSuccesServiceCalls(self):
        s = ServiceImpl()
        self.assertTrue(s.multipy() == 100000)
        self.assertTrue(s.multipy(23) == 46)
        self.assertTrue(s.multipy(15.5) == 31)
        self.assertTrue(s.intToStr(23) == '23')
        self.assertTrue(s.intToStr(11) == '11')
        self.assertTrue(s.doNothing(11) == None)
        return

    def testFailedServiceCalls(self):

        class ServiceImpl(IService):

            def multipy(self, x=None):
                if x is None:
                    return 100000
                else:
                    return x + x

            def intToStr(self, x):
                return str(x)

        self.assertRaises(TypeError, ServiceImpl)


if __name__ == '__main__':
    unittest.main()