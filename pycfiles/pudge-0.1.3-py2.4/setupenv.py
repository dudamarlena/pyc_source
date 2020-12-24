# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/test/setupenv.py
# Compiled at: 2006-03-14 16:35:23
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