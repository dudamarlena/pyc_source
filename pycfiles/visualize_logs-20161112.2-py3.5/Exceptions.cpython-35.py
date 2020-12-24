# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/Visualize_Logs/objects/Exceptions.py
# Compiled at: 2016-11-11 19:53:33
# Size of source mod 2**32: 1463 bytes


class VisualizeLogsInvalidFile(Exception):
    __doc__ = '\n\n    Exception for when a file does not exist or is invalid.\n\n    '

    def __init__(self, filepath):
        Exception.__init__(self, 'Visualize_Logs: Invalid File {0}'.format(filepath))


class VisualizeLogsInvalidFileStructure(Exception):
    __doc__ = "\n\n    Exception for when a file's content is not structured correctly.\n\n    "

    def __init__(self, filepath):
        Exception.__init__(self, 'Visualize_Logs: Invalid File Content {0}'.format(filepath))


class VisualizeLogsMissingRequiredField(Exception):
    __doc__ = "\n\n    Exception for when a file's content is missing a data field.\n\n    "

    def __init__(self, filepath, field):
        Exception.__init__(self, 'Visualize_Logs: Missing Field {0} in {1}'.format(field, filepath))


class VisualizeLogsBadFunctionInput(Exception):
    __doc__ = '\n\n    Exception for when bad input is given to a function.\n\n    '

    def __init__(self, inputname):
        Exception.__init__(self, 'Visualize_Logs: Bad Function Input: {0}'.format(inputname))


class VisualizeLogsParseError(Exception):
    __doc__ = '\n\n    Exception for when data cannot be parsed correctly.\n\n    '

    def __init__(self, data):
        Exception.__init__(self, 'Visualize_Logs: Cannot parse: {0}'.format(data))