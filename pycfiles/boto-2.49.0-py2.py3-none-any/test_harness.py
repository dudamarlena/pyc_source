# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/test_harness.py
# Compiled at: 2012-08-16 08:18:10
__doc__ = '\nSimple test harness function\n'
import sys

def test_harness(function, test_data):
    """
    Returns the result of the test along with the test_data object updated
    """
    name = 'test.test_' + function[0] + '.test_' + function[1]
    sys.stdout.write('Testing ' + name + '()...')
    (result, test_data) = eval(name + '(test_data)')
    if result:
        sys.stdout.write('success\n')
    else:
        sys.stdout.write('failed\n')
    return (result, test_data)