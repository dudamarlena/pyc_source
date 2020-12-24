# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/instancemanager/tests.py
# Compiled at: 2007-12-17 05:32:50
import actionutils, configuration, sources
modules = (
 actionutils, configuration, sources)

def _test():
    import doctest, sys
    optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
    verbose = '-v' in sys.argv
    for mod in modules:
        doctest.testmod(mod, verbose=verbose, optionflags=optionflags, report=0)

    doctest.master.summarize()


if __name__ == '__main__':
    _test()