# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/virtualenv/python2.7.9/lib/python2.7/site-packages/cxmanage_api/cx_exceptions.py
# Compiled at: 2017-02-08 04:42:30
__doc__ = 'Calxeda: cx_exceptions.py'
from pyipmi import IpmiError
from tftpy.TftpShared import TftpException

class EEPROMUpdateError(Exception):
    """Raised when an error is encountered while updating the EEPROM

    >>> from cxmanage_api.cx_exceptions import TimeoutError
    >>> raise TimeoutError('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.TimeoutError: My custom exception text!

    :param msg: Exceptions message and details to return to the user.
    :type msg: string
    :raised: When an error is encountered while updating the EEPROM

    """

    def __init__(self, msg):
        """Default constructor for the EEPROMUpdateError class."""
        super(EEPROMUpdateError, self).__init__()
        self.msg = msg

    def __str__(self):
        """String representation of this Exception class."""
        return self.msg


class TimeoutError(Exception):
    """Raised when a timeout has been reached.

    >>> from cxmanage_api.cx_exceptions import TimeoutError
    >>> raise TimeoutError('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.TimeoutError: My custom exception text!

    :param msg: Exceptions message and details to return to the user.
    :type msg: string
    :raised: When a timeout has been reached.

    """

    def __init__(self, msg):
        """Default constructor for the TimoutError class."""
        super(TimeoutError, self).__init__()
        self.msg = msg

    def __str__(self):
        """String representation of this Exception class."""
        return self.msg


class NoPartitionError(Exception):
    """Raised when a partition is not found.

    >>> from cxmanage_api.cx_exceptions import NoPartitionError
    >>> raise NoPartitionError('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.NoPartitionError: My custom exception text!

    :param msg: Exceptions message and details to return to the user.
    :type msg: string
    :raised: When a partition is not found.

    """

    def __init__(self, msg):
        """Default constructor for the NoPartitionError class."""
        super(NoPartitionError, self).__init__()
        self.msg = msg

    def __str__(self):
        """String representation of this Exception class."""
        return self.msg


class NoSensorError(Exception):
    """Raised when a sensor or sensors are not found.

    >>> from cxmanage_api.cx_exceptions import NoSensorError
    >>> raise NoSensorError('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.NoSensorError: My custom exception text!

    :param msg: Exceptions message and details to return to the user.
    :type msg: string
    :raised: When a sensor or sensors are not found.

    """

    def __init__(self, msg):
        """Default constructor for the NoSensorError class."""
        super(NoSensorError, self).__init__()
        self.msg = msg

    def __str__(self):
        """String representation of this Exception class."""
        return self.msg


class SocmanVersionError(Exception):
    """Raised when there is an error with the users socman version.

    >>> from cxmanage_api.cx_exceptions import SocmanVersionError
    >>> raise SocmanVersionError('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.SocmanVersionError: My custom exception text!

    :param msg: Exceptions message and details to return to the user.
    :type msg: string
    :raised: When there is an error with the users socman version.

    """

    def __init__(self, msg):
        """Default constructor for the SocmanVersionError class."""
        super(SocmanVersionError, self).__init__()
        self.msg = msg

    def __str__(self):
        """String representation of this Exception class."""
        return self.msg


class FirmwareConfigError(Exception):
    """Raised when there are slot/firmware version inconsistencies.

    >>> from cxmanage_api.cx_exceptions import FirmwareConfigError
    >>> raise FirmwareConfigError('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.FirmwareConfigError: My custom exception text!

    :param msg: Exceptions message and details to return to the user.
    :type msg: string
    :raised: When there are slot/firmware version inconsistencies.

    """

    def __init__(self, msg):
        """Default constructor for the FirmwareConfigError class."""
        super(FirmwareConfigError, self).__init__()
        self.msg = msg

    def __str__(self):
        """String representation of this Exception class."""
        return self.msg


class PriorityIncrementError(Exception):
    """Raised when the Priority on a SIMG image cannot be altered.

    >>> from cxmanage_api.cx_exceptions import PriorityIncrementError
    >>> raise PriorityIncrementError('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.PriorityIncrementError: My custom exception text!

    :param msg: Exceptions message and details to return to the user.
    :type msg: string
    :raised: When the Priority on a SIMG image cannot be altered.

    """

    def __init__(self, msg):
        """Default constructor for the PriorityIncrementError class."""
        super(PriorityIncrementError, self).__init__()
        self.msg = msg

    def __str__(self):
        """String representation of this Exception class."""
        return self.msg


class ImageSizeError(Exception):
    """Raised when the actual size of the image is not what is expected.

    >>> from cxmanage_api.cx_exceptions import ImageSizeError
    >>> raise ImageSizeError('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.ImageSizeError: My custom exception text!

    :param msg: Exceptions message and details to return to the user.
    :type msg: string
    :raised: When the actual size of the image is not what is expected.

    """

    def __init__(self, msg):
        """Default constructor for the ImageSizeError class."""
        super(ImageSizeError, self).__init__()
        self.msg = msg

    def __str__(self):
        """String representation of this Exception class."""
        return self.msg


class TransferFailure(Exception):
    """Raised when the transfer of a file has failed.

    >>> from cxmanage_api.cx_exceptions import TransferFailure
    >>> raise TransferFailure('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.TransferFailure: My custom exception text!

    :param msg: Exceptions message and details to return to the user.
    :type msg: string
    :raised: When the transfer of a file has failed.

    """

    def __init__(self, msg):
        """Default constructor for the TransferFailure class."""
        super(TransferFailure, self).__init__()
        self.msg = msg

    def __str__(self):
        """String representation of this Exception class."""
        return self.msg


class InvalidImageError(Exception):
    """Raised when an image is not valid. (i.e. fails verification).

    >>> from cxmanage_api.cx_exceptions import InvalidImageError
    >>> raise InvalidImageError('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.InvalidImageError: My custom exception text!

    :param msg: Exceptions message and details to return to the user.
    :type msg: string
    :raised: When an image is not valid. (i.e. fails verification).

    """

    def __init__(self, msg):
        """Default constructor for the InvalidImageError class."""
        super(InvalidImageError, self).__init__()
        self.msg = msg

    def __str__(self):
        """String representation of this Exception class."""
        return self.msg


class NodeMismatchError(Exception):
    """Raised when a node that is supposed to be an updated version of the
    current node is not.

    >>> from cxmanage_api.cx_exceptions import NodeMismatchError
    >>> raise InvalidImageError('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.InvalidImageError: My custom exception text!

    :param msg: Exceptions message and details to return to the user.
    :type msg: string
    :raised: When a node passed in to refresh() another node does not match.

    """

    def __init__(self, msg):
        """Default constructor for the NodeMismatchError class."""
        super(NodeMismatchError, self).__init__()
        self.msg = msg

    def __str__(self):
        """String representation of this Exception class."""
        return self.msg


class UbootenvError(Exception):
    """Raised when the UbootEnv class fails to interpret the ubootenv
    environment variables.

    >>> from cxmanage_api.cx_exceptions import UbootenvError
    >>> raise UbootenvError('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.UbootenvError: My custom exception text!

    :param msg: Exceptions message and details to return to the user.
    :type msg: string
    :raised: When ubootenv settings are unrecognizable.

    """

    def __init__(self, msg):
        """Default constructor for the UbootenvError class."""
        super(UbootenvError, self).__init__()
        self.msg = msg

    def __str__(self):
        """String representation of this Exception class."""
        return self.msg


class CommandFailedError(Exception):
    """Raised when a command has failed.

    >>> from cxmanage_api.cx_exceptions import CommandFailedError
    >>> raise CommandFailedError('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.CommandFailedError: My custom exception text!

    :param results: Command results. (map of nodes->results)
    :type results: dictionary
    :param errors: Command errors. (map of nodes->errors)
    :type errors: dictionary
    :raised: When a command has failed.

    """

    def __init__(self, results, errors):
        """Default constructor for the CommandFailedError class."""
        super(CommandFailedError, self).__init__()
        self.results = results
        self.errors = errors

    def __repr__(self):
        return 'Results: %s Errors: %s' % (self.results, self.errors)

    def __str__(self):
        return str(dict((x, str(y)) for x, y in self.errors.iteritems()))


class PartitionInUseError(Exception):
    """Raised when trying to upload to a CDB/BOOT_LOG partition that's in use.

    >>> from cxmanage_api.cx_exceptions import PartitionInUseError
    >>> raise PartitionInUseError('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.PartitionInUseError: My custom exception text!

    :param msg: Exceptions message and details to return to the user.
    :type msg: string
    :raised: When trying to upload to a CDB/BOOT_LOG partition that's in use.

    """

    def __init__(self, msg):
        """Default constructor for the PartitionInUseError class."""
        super(PartitionInUseError, self).__init__()
        self.msg = msg

    def __str__(self):
        """String representation of this Exception class."""
        return self.msg


class IPDiscoveryError(Exception):
    """Raised when server IP discovery fails for any reason.

    >>> from cxmanage_api.cx_exceptions import IPDiscoveryError
    >>> raise IPDiscoveryError('My custom exception text!')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    cxmanage_api.cx_exceptions.IPDiscoveryError: My custom exception text!

    :param msg: Exceptions message and details to return to the user.
    :type msg: string
    :raised: When IP discovery fails for any reason.

    """

    def __init__(self, msg):
        """Default constructor for the IPDsicoveryError class."""
        super(IPDiscoveryError, self).__init__()
        self.msg = msg

    def __str__(self):
        """String representation of this Exception class."""
        return self.msg


class ParseError(Exception):
    """Raised when there's an error parsing some output"""