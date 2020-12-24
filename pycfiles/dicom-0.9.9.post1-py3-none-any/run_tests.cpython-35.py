# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\test\run_tests.py
# Compiled at: 2017-01-26 21:08:30
# Size of source mod 2**32: 2041 bytes
"""Call all the unit test files in the test directory starting with 'test'"""
import os, os.path, sys, unittest
from pkg_resources import Requirement, resource_filename
test_dir = resource_filename(Requirement.parse('dicom'), 'dicom/test')

class MyTestLoader(object):

    def loadTestsFromNames(self, *args):
        save_dir = os.getcwd()
        if test_dir:
            os.chdir(test_dir)
        filenames = os.listdir('.')
        module_names = [f[:-3] for f in filenames if f.startswith('test') and f.endswith('.py')]
        suite = unittest.TestSuite()
        for module_name in module_names:
            module_dotted_name = 'dicom.test.' + module_name
            test = unittest.defaultTestLoader.loadTestsFromName(module_dotted_name)
            suite.addTest(test)

        os.chdir(save_dir)
        return suite


if __name__ == '__main__':
    suite = MyTestLoader().loadTestsFromNames()
    verbosity = 1
    args = sys.argv
    if len(args) > 1 and (args[1] == '-v' or args[1] == '--verbose'):
        verbosity = 2
    runner = unittest.TextTestRunner(verbosity=verbosity)
    save_dir = os.getcwd()
    testfiles_dir = resource_filename(Requirement.parse('dicom'), 'dicom/testfiles')
    os.chdir(testfiles_dir)
    runner.run(suite)
    os.chdir(save_dir)