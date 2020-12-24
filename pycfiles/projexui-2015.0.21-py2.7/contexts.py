# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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