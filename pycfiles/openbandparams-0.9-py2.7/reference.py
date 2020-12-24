# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/reference.py
# Compiled at: 2015-04-09 03:16:40


class Reference(object):
    pass


class BibtexReference(Reference):

    def __init__(self, bibtex):
        self.bibtex = bibtex

    def __str__(self):
        return self.bibtex