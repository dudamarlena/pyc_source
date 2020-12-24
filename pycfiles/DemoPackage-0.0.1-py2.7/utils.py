# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/DemoPackage/utils.py
# Compiled at: 2013-04-29 13:17:22
""" Utility functions."""

def print_string():
    """This function prints a string.
    
    :returns: None.
    :output: print an string.
    :rtype: None.
    """
    print 'This is a sample string.'
    print 'Author : Sourabh Bajaj'


def print_integer(i=100):
    """This function prints the integer i.
    
    :param i: The integer to be printed.
    :returns: None.
    :rtype: None.
    :output: print an integer
    """
    print 'This is a sample integer.', i


def main():
    """
    This is the main function
    """
    print 'This is the main function'


if __name__ == '__main__':
    main()