# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/ims_lti_py/utils.py
# Compiled at: 2013-02-01 11:28:56
from uuid import uuid1

def generate_identifier():
    return uuid1().__str__()


class InvalidLTIConfigError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidLTIRequestError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)