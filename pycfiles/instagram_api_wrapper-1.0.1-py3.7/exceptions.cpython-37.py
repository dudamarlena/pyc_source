# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/instagram_api_wrapper/exceptions.py
# Compiled at: 2018-08-28 06:29:52
# Size of source mod 2**32: 100 bytes


class InstagramApiError(Exception):

    def __init__(self, message):
        self.message = message