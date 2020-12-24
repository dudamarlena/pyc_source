# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/tests/test.py
# Compiled at: 2007-12-02 16:26:54
"""
Manually run specified tests
"""
import unittest, doctest, sys

def main():
    modules = []
    docFiles = []
    docTestModules = []
    verb = 0
    for file in sys.argv[1:]:
        if file == '-v':
            verb = verb + 2
        elif file[-4:] == '.txt':
            docFiles.append(file)
        elif file[-3:] == '.py':
            name = file[:-3].replace('/', '.')
            dest = docTestModules
            if '/tests/' in file:
                dest = modules
            dest.append(name)
        else:
            modules.append(file)

    suite = unittest.TestLoader().loadTestsFromNames(modules)
    suite.addTests([ doctest.DocFileSuite(file, module_relative=False) for file in docFiles ])
    for module in docTestModules:
        try:
            suite.addTest(doctest.DocTestSuite(module))
        except ValueError, msg:
            if msg[1] != 'has no tests':
                raise

    unittest.TextTestRunner(verbosity=verb).run(suite)


if __name__ == '__main__':
    main()