# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/id3frameadaptor.py
# Compiled at: 2009-05-11 19:02:40
"""
Given a set of key-val pairs provided by the textparser this class will transform it into a new 
mapping in which the keys are all ID3V2 frame names.
"""

class id3frameadaptor:

    @classmethod
    def adapt(cls, inputmapping):
        return inputmapping