# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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