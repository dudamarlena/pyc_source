# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jmcarp/miniconda/envs/guardian/lib/python2.7/site-packages/guardrail/core/exceptions.py
# Compiled at: 2015-03-25 19:18:57


class GuardrailException(Exception):
    pass


class RecordNotSaved(GuardrailException):
    pass


class SchemaNotFound(GuardrailException):
    pass


class PermissionExists(GuardrailException):
    pass


class PermissionNotFound(GuardrailException):
    pass