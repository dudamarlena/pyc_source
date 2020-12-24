# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/secobj/exceptions.py
# Compiled at: 2012-08-13 09:47:32


class SecurityError(Exception):
    pass


class AccessDeniedError(SecurityError):
    pass


class NoMatchingRuleError(SecurityError):
    pass


class UnknownActionError(SecurityError):
    pass


class UnknownPrincipalError(SecurityError):
    pass