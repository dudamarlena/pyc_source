# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/clsexceptions.py
# Compiled at: 2010-12-12 22:28:56


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class DuplicateXMLDocumentError(Exception):

    def __init__(self, *args):
        message = 'Error %s: \nIndicates: %s\nIn Location: %s' % (args[0], args[1], args[2])
        print message
        self.message = message


class UndefinedXMLWriter(Exception):

    def __init__(self, *args):
        print 'Error %s: \nIndicates: %s\nIn Location: %s' % (args[0], args[1], args[2])


class DatabaseAuthenticationError(Exception):

    def __init__(self, *args):
        print 'Error %s: \nIndicates: %s\nIn Location: %s' % (args[0], args[1], args[2])


class SoftwareCompatibilityError(Exception):

    def __init__(self, *args):
        print 'Error %s: \nIndicates: %s\nIn Location: %s' % (args[1], args[0], args[2])


class XSDError(Exception):

    def __init__(self, *args):
        print 'Error %s: \nIndicates: %s\nIn Location: %s' % (args[1], args[0], args[2])


class dbLayerNotFoundError(Exception):

    def __init__(self, *args):
        print 'Error %s: \nIndicates: %s\nIn Location: %s' % (args[1], args[0], args[2])


class VPNFailure(Error):

    def __init__(self, *args):
        print 'Error %s: \nIndicates: %s\nIn Location: %s' % (args[1], args[0], args[2])


class FTPUploadFailureError(Error):

    def __init__(self, *args):
        print 'Error %s: \nIndicates: %s\nIn Location: %s' % (args[1], args[0], args[2])


class KeyboardInterrupt(Error):

    def __init__(self, *args):
        print 'Intercepted Keyboard Interupt'


class fileNotFoundError(Error):

    def __init__(self, *args):
        print 'Error %s: \nIndicates: %s\nIn Location: %s' % (args[1], args[0], args[2])


class dataFormatError(Error):

    def __init__(self, *args):
        print 'Error %s: \nIndicates: %s\nIn Location: %s' % (args[1], args[0], args[2])


class InvalidSSNError(Error):

    def __init__(self, *args):
        print 'Error %s: \nIndicates: %s\nIn Location: %s' % (args[1], args[0], args[2])


class ethnicityPickNotFound(Error):

    def __init__(self, *args):
        print 'Error %s: \nIndicates: %s\nIn Location: %s' % (args[1], args[0], args[2])


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message