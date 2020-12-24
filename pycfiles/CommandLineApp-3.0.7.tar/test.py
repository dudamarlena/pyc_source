# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/commandline/test.py
# Compiled at: 2009-06-13 11:00:11
__doc__ = '\nJust a test module, using doctests. Run tests using python setup.py test\nor python test.py\n'

def doctests():
    """
    >>> import commandline
    >>> commandline.TESTMODE=1
    >>> def test1(arg1=1, arg2=2, arg3=3):
    ...     print [arg1, arg2, arg3]
    ...
    >>> commandline.run_as_main(test1, [])
    [1, 2, 3]
    >>> commandline.run_as_main(test1, ['6'])
    [6, 2, 3]
    >>> commandline.run_as_main(test1, ['--arg1=6', '--arg2=7', '--arg3=8'])
    [6, 7, 8]
    >>> commandline.run_as_main(test1, ['6', '7', '8'])
    [6, 7, 8]
    
    >>> commandline.run_as_main(test1, ['6', '7', '8', '9'], 'test.py')
    Usage: test.py [arg1 [arg2 [arg3]]] [Options]
    <BLANKLINE>
    (Please put options last, and no more args than shown.)
    Unexpected argument(s): 9
    
    >>> commandline.run_as_main(test1, ['--arg1=6', '7', '8'], 'test.py')
    Usage: test.py [arg1 [arg2 [arg3]]] [Options]
    <BLANKLINE>
    (Please put options last, and no more args than shown.)
    Unexpected argument(s): 7, 8
    
    >>> def test2(arg1=1, arg2=2, arg3=3):
    ...     return [arg1, arg2, arg3]
    ...
    >>> commandline.run_as_main(test2, ['6', '7', '8'])
    [6, 7, 8]
    
    >>> def nodefault(arg1, arg2, arg3):
    ...     return [arg1, arg2, arg3]
    >>> # If we have no default arguments, we assume you want strings:
    >>> commandline.run_as_main(nodefault, ['6', '7', '8'])
    ['6', '7', '8']
    >>> commandline.run_as_main(nodefault, [], 'test.py')
    Usage: test.py arg1 arg2 arg3 [Options]
    <BLANKLINE>
    The following compulsory arguments are missing: arg1, arg2, arg3
    """
    doctest.testmod()


import doctest, unittest
suite = unittest.TestSuite()
suite.addTest(doctest.DocTestSuite())
if __name__ == '__main__':
    doctests()