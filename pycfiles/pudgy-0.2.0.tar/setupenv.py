# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/test/setupenv.py
# Compiled at: 2006-03-14 17:35:23
from os.path import dirname, abspath, normpath, join
__all__ = [
 'test_code_dir', 'test_files', 'test_output_dir', 'build_dir', 'get_test_file', 'get_output_file']
test_code_dir = abspath(dirname(__file__))
test_files = join(test_code_dir, 'data')
build_dir = join(dirname(dirname(test_code_dir)), 'build')
test_output_dir = join(dirname(dirname(test_code_dir)), 'build/test')

def get_test_file(filename):
    return join(test_files, filename)


def get_output_file(*filenames):
    return join(test_output_dir, *filenames)