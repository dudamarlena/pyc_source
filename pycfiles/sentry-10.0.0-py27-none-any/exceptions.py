# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/tagstore/exceptions.py
# Compiled at: 2019-08-16 12:27:43
from __future__ import absolute_import

class TagKeyNotFound(Exception):
    pass


class TagValueNotFound(Exception):
    pass


class GroupTagKeyNotFound(Exception):
    pass


class GroupTagValueNotFound(Exception):
    pass