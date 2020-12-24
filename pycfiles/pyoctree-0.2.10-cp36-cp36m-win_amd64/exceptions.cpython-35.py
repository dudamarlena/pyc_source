# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyoctopart/exceptions.py
# Compiled at: 2016-03-05 13:07:37
# Size of source mod 2**32: 4637 bytes
__doc__ = '\npyoctopart: A simple Python client library to the Octopart public REST API.\n\nauthor: Bernard `Guyzmo` Pratz <octopart@m0g.net>\nauthor: Joe Baker <jbaker@alum.wpi.edu>\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n  http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'

class OctopartException(Exception):
    """OctopartException"""
    __slots__ = [
     'arguments', 'arg_types', 'arg_ranges', 'code']

    def __init__(self, args, arg_types, arg_ranges, error_message):
        self.arguments = args
        self.arg_types = arg_types
        self.arg_ranges = arg_ranges
        self.message = error_message

    def __str__(self):
        args = ' '.join(('\nPassed arguments:', str(self.arguments)))
        argt = ' '.join(('\nArgument types:', str(self.arg_types)))
        argr = ' '.join(('\nArgument ranges:', str(self.arg_ranges)))
        string = self.message + args + argt + argr
        return string


class OctopartInvalidApiKeyError(OctopartException):

    def __init__(self, apikey):
        OctopartException.__init__(self, [], [], [], '')
        self.apikey = apikey

    def __str__(self):
        return "Api key '{}' is invalid! Please set it up!".format(self.apikey)


class OctopartArgumentMissingError(OctopartException):

    def __init__(self, args, arg_types, arg_ranges):
        OctopartException.__init__(self, args, arg_types, arg_ranges, 'Required argument missing from method call.')


class OctopartArgumentInvalidError(OctopartException):

    def __init__(self, args, arg_types, arg_ranges):
        OctopartException.__init__(self, args, arg_types, arg_ranges, 'Passed an invalid argument for this method.')


class OctopartTypeArgumentError(OctopartException):

    def __init__(self, args, arg_types, arg_ranges):
        OctopartException.__init__(self, args, arg_types, arg_ranges, 'Argument type mismatch.')


class OctopartRangeArgumentError(OctopartException):

    def __init__(self, args, arg_types, arg_ranges):
        OctopartException.__init__(self, args, arg_types, arg_ranges, 'Numeric argument value out of valid range.')


class OctopartStringLengthError(OctopartException):

    def __init__(self, args, arg_types, arg_ranges):
        OctopartException.__init__(self, args, arg_types, arg_ranges, 'String argument outside of allowed length.')


class OctopartLimitExceededError(OctopartException):

    def __init__(self, args, arg_types, arg_ranges):
        OctopartException.__init__(self, args, arg_types, arg_ranges, 'Value of (start+limit) in a bom/match line argument exceeds 100.')


class Octopart404Error(OctopartException):

    def __init__(self, args, arg_types, arg_ranges):
        OctopartException.__init__(self, args, arg_types, arg_ranges, 'Unexpected HTTP Error 404.')


class Octopart503Error(OctopartException):

    def __init__(self, args, arg_types, arg_ranges):
        OctopartException.__init__(self, args, arg_types, arg_ranges, 'Unexpected HTTP Error 503.')


class OctopartNonJsonArgumentError(OctopartException):

    def __init__(self, args, arg_types, arg_ranges):
        OctopartException.__init__(self, args, arg_types, arg_ranges, 'Argument is not a JSON-encoded list of pairs.')


class OctopartInvalidSortError(OctopartException):

    def __init__(self, args, arg_types, arg_ranges):
        OctopartException.__init__(self, args, arg_types, arg_ranges, 'Invalid sort order. Valid sort order strings are "asc" and "desc".')


class OctopartTooLongListError(OctopartException):

    def __init__(self, args, arg_types, arg_ranges):
        OctopartException.__init__(self, args, arg_types, arg_ranges, 'List argument outside of allowed length.')