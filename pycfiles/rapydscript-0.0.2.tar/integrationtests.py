# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/host/inst/rapydscript/tests/integrationtests.py
# Compiled at: 2013-02-27 23:08:11
import unittest
from os import listdir, path, remove, getcwd
from subprocess import Popen
from filecmp import cmp
DATA_DIR = './tests/testdata'

def get_test_file_list():
    file_dict = {}
    for filename in listdir(DATA_DIR):
        test_name = ''
        file_type = ''
        if filename.endswith('.pyj'):
            test_name = filename[:-4]
            file_type = '.pyj'
        elif filename.endswith('.ref'):
            test_name, file_type = path.splitext(filename[:-4])
            if file_type not in ('.js', ):
                file_type = ''
        if test_name and file_type:
            if test_name not in file_dict:
                file_dict[test_name] = []
            file_dict[test_name].append(file_type)

    test_list = []
    for test_name, test_file_list in file_dict.iteritems():
        if len(test_file_list) == 2:
            test_list.append(test_name)
        else:
            print '%s has unexpected files %s' % (test_name, test_file_list)

    return test_list


def delete_test_output(test_name):
    for check_ext in ('js', ):
        try:
            check_file = '%s/%s.%s' % (DATA_DIR, test_name, check_ext)
            remove(check_file)
        except:
            pass


def test_generator(test_name):

    def test_function(self):
        delete_test_output(test_name)
        p = Popen(['./bin/rapydscript', '%s/%s.pyj' % (DATA_DIR, test_name)])
        p.communicate()
        for check_ext, test in (('js', 'Javascript'), ):
            check_file = '%s/%s.%s' % (DATA_DIR, test_name, check_ext)
            self.assertTrue(cmp(check_file, '%s.ref' % check_file), 'Unexpected %s output for %s' % (check_file, test))

        delete_test_output(test_name)

    return test_function


class SuiteGenerator(type):
    """
    Metaclass for generating test methods in RapydTest
    """

    def __new__(self, cls, parents, cls_dict):
        test_list = get_test_file_list()
        for test_name in test_list:
            test_fun_name = 'test_%s' % test_name
            if test_fun_name in cls_dict:
                raise Exception('Tests not compatible')
            cls_dict[test_fun_name] = test_generator(test_name)

        return super(SuiteGenerator, self).__new__(self, cls, parents, cls_dict)


class RapydTest(unittest.TestCase):
    __metaclass__ = SuiteGenerator

    def test_run(self):
        """
        Just a test to make sure this class is generated properly then run
        """
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()