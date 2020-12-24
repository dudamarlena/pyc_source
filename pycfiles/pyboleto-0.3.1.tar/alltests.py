# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ecereto/src/pyboleto/tests/alltests.py
# Compiled at: 2016-04-11 02:39:08
import unittest

def suite():
    """suite that tests all banks"""

    def my_import(name):
        components = name.split('.')
        try:
            mod = __import__(name)
            for comp in components[1:]:
                mod = getattr(mod, comp)

        except ImportError:
            mod = __import__(components[1])

        return mod

    modules_to_test = [
     'tests.test_banco_banrisul',
     'tests.test_banco_bradesco',
     'tests.test_banco_caixa',
     'tests.test_banco_do_brasil',
     'tests.test_banco_hsbc',
     'tests.test_banco_hsbc_com_registro',
     'tests.test_banco_itau',
     'tests.test_banco_real',
     'tests.test_banco_santander']
    alltests = unittest.TestSuite()
    for module in [ my_import(x) for x in modules_to_test ]:
        alltests.addTest(module.suite)

    return alltests


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())