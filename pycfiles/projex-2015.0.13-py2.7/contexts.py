# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/contexts.py
# Compiled at: 2016-07-03 23:28:12


class MultiContext(object):
    """ Support entering and exiting of multiple python contexts """

    def __init__(self, *contexts):
        self._contexts = contexts

    def __enter__(self):
        for context in self._contexts:
            context.__enter__()

    def __exit__(self, *args):
        for context in self._contexts:
            context.__exit__(*args)