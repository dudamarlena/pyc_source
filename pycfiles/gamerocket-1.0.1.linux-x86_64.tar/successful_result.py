# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/result/successful_result.py
# Compiled at: 2013-08-22 05:48:38
from gamerocket.attribute_getter import AttributeGetter

class SuccessfulResult(AttributeGetter):

    @property
    def is_success(self):
        return True