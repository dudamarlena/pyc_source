# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\E_Documents\Python_Code\smart_preprocess\smart_preprocess\smart_preprocess\dmreader\exceptions.py
# Compiled at: 2018-08-22 10:53:12
# Size of source mod 2**32: 4948 bytes


class ByteOrderError(Exception):

    def __init__(self, order=''):
        self.byte_order = order

    def __str__(self):
        return repr(self.byte_order)


class DM3FileVersionError(Exception):

    def __init__(self, value=''):
        self.dm3_version = value

    def __str__(self):
        return repr(self.dm3_version)


class DM3TagError(Exception):

    def __init__(self, value=''):
        self.dm3_tag = value

    def __str__(self):
        return repr(self.dm3_tag)


class DM3DataTypeError(Exception):

    def __init__(self, value=''):
        self.dm3_dtype = value

    def __str__(self):
        return repr(self.dm3_dtype)


class DM3TagTypeError(Exception):

    def __init__(self, value=''):
        self.dm3_tagtype = value

    def __str__(self):
        return repr(self.dm3_tagtype)


class DM3TagIDError(Exception):

    def __init__(self, value=''):
        self.dm3_tagID = value

    def __str__(self):
        return repr(self.dm3_tagID)


class ImageIDError(Exception):

    def __init__(self, value=''):
        self.image_id = value

    def __str__(self):
        return repr(self.image_id)


class ImageModeError(Exception):

    def __init__(self, value=''):
        self.mode = value

    def __str__(self):
        return repr(self.mode)


class ShapeError(Exception):

    def __init__(self, value):
        self.error = value.shape

    def __str__(self):
        return repr(self.error)


class NoInteractiveError(Exception):

    def __init__(self):
        self.error = 'HyperSpy must run in interactive mode to use this feature'

    def __str__(self):
        return repr(self.error)


class WrongObjectError(Exception):

    def __init__(self, is_str, must_be_str):
        self.error = 'A object of type %s was given, but a %s' % (
         is_str, must_be_str) + ' object is required'

    def __str__(self):
        return repr(self.error)


class MissingParametersError(Exception):

    def __init__(self, parameters):
        par_str = ''
        for par in parameters:
            par_str += '%s,' % par

        self.error = 'The following parameters are missing: %s' % par_str
        self.error = self.error[:-1]

    def __str__(self):
        return repr(self.error)


class DataDimensionError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class SignalDimensionError(Exception):

    def __init__(self, output_dimension, expected_output_dimension):
        self.output_dimension = output_dimension
        self.expected_output_dimension = expected_output_dimension
        self.msg = 'output dimension=%i, %i expected' % (
         self.output_dimension, self.expected_output_dimension)

    def __str__(self):
        return repr(self.msg)


class NavigationDimensionError(Exception):

    def __init__(self, navigation_dimension, expected_navigation_dimension):
        self.navigation_dimension = navigation_dimension
        self.expected_navigation_dimension = expected_navigation_dimension
        self.msg = 'navigation dimension=%i, %s expected' % (
         self.navigation_dimension, self.expected_navigation_dimension)

    def __str__(self):
        return repr(self.msg)


class SignalSizeError(Exception):

    def __init__(self, signal_size, expected_signal_size):
        self.signal_size = signal_size
        self.expected_signal_size = expected_signal_size
        self.msg = 'signal_size=%i, %i expected' % (
         self.signal_size, self.expected_signal_size)

    def __str__(self):
        return repr(self.msg)


class NavigationSizeError(Exception):

    def __init__(self, navigation_size, expected_navigation_size):
        self.navigation_size = navigation_size
        self.expected_navigation_size = expected_navigation_size
        self.msg = 'navigation_size =%i, %i expected' % (
         self.navigation_size, self.expected_navigation_size)


class VisibleDeprecationWarning(UserWarning):
    __doc__ = 'Visible deprecation warning.\n    By default, python will not show deprecation warnings, so this class\n    provides a visible one.\n\n    '