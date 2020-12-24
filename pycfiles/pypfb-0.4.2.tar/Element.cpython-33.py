# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pf3/pdf/Element.py
# Compiled at: 2014-08-15 05:05:30
# Size of source mod 2**32: 161 bytes


class Element:
    TYPE_TEXT = 0
    TYPE_IMAGE = 1
    elementType = None

    def __init__(self, element_type):
        self.elementType = element_type