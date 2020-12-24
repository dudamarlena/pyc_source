# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-api/vkontakte_api/exceptions.py
# Compiled at: 2015-01-25 02:59:11


class VkontakteDeniedAccessError(Exception):
    pass


class VkontakteContentError(Exception):
    pass


class VkontakteParseError(Exception):
    pass


class WrongResponseType(Exception):
    pass