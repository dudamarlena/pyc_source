# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pf3/pdf/Element.py
# Compiled at: 2014-08-15 05:05:30
# Size of source mod 2**32: 161 bytes


class Element:
    TYPE_TEXT = 0
    TYPE_IMAGE = 1
    elementType = None

    def __init__(self, element_type):
        self.elementType = element_type