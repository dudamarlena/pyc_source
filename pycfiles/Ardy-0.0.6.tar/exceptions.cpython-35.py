# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prometeo/projects/ardy/ardy/core/exceptions.py
# Compiled at: 2018-03-24 11:47:25
# Size of source mod 2**32: 432 bytes
from __future__ import unicode_literals, print_function

class ArdyNoFileError(Exception):
    pass


class ArdyNoDirError(Exception):
    pass


class ArdyLambdaNotExistsError(Exception):
    pass


class ArdyEnvironmentNotExistsError(Exception):
    pass


class ArdyAwsError(Exception):
    pass


class ArdyNoArtefactError(Exception):
    pass


class ArdyNotImplementError(Exception):
    pass