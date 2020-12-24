# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dtopt/tests.py
# Compiled at: 2007-08-10 14:24:37
__test__ = {'test this': "\nEllisis in particular are tested here.  First, an\nerror:\n\n    >>> o = object()\n    >>> o # Expect a doctest error here!\n    ...   # really, it's okay\n    <object object at ...>\n\nSee, you got an error!  Next:\n\n    >>> from dtopt import ELLIPSIS\n    >>> o\n    <object object at ...>\n"}
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print 'Expect *one* error.  Zero is bad, two is bad.'
    print 'One error is good'