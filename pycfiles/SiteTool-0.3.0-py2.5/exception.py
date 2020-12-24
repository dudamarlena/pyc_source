# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sitetool/exception.py
# Compiled at: 2009-04-26 08:24:53


class TemplateError(Exception):
    """Raised when a general Error in the templates.py module occurs
    Attributes:
        message -- explanation of what the specific error is.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class PluginError(Exception):
    pass