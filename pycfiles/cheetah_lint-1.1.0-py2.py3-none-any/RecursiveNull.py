# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tools/RecursiveNull.py
# Compiled at: 2019-09-22 10:12:27
__doc__ = '\nNothing, but in a friendly way.  Good for filling in for objects you want to\nhide.  If $form.f1 is a RecursiveNull object, then\n$form.f1.anything["you"].might("use") will resolve to the empty string.\n\nThis module was contributed by Ian Bicking.\n'
import sys

class RecursiveNull(object):

    def __getattr__(self, attr):
        return self

    def __getitem__(self, item):
        return self

    def __call__(self, *args, **kwargs):
        return self

    def __str__(self):
        return ''

    def __repr__(self):
        return ''

    if sys.version_info[0] >= 3:

        def __bool__(self):
            return 0

    else:

        def __nonzero__(self):
            return 0

    def __eq__(self, x):
        if x:
            return False
        return True

    def __ne__(self, x):
        return x and True or False


del sys