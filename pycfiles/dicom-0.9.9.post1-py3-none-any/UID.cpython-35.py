# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\UID.py
# Compiled at: 2017-01-26 21:09:38
# Size of source mod 2**32: 6980 bytes
"""Dicom Unique identifiers"""
import os, uuid, datetime
from math import fabs
from ._UID_dict import UID_dictionary

class InvalidUID(Exception):
    __doc__ = "\n    Throw when DICOM UID is invalid\n\n    Example of invalid UID::\n\n        >>> uid = '1.2.123.'\n    "

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class UID(str):
    __doc__ = "Subclass python string so have human-friendly UIDs\n\n    Use like:\n        uid = UID('1.2.840.10008.1.2.4.50')\n    then\n        uid.name, uid.type, uid.info, and uid.is_retired all return\n           values from the UID_dictionary\n\n    String representation (__str__) will be the name,\n    __repr__ will be the full 1.2.840....\n    "

    def __new__(cls, val):
        """Set up new instance of the class"""
        if isinstance(val, UID):
            return val
        if isinstance(val, str):
            return super(UID, cls).__new__(cls, val.strip())
        raise TypeError('UID must be a string')

    def __init__(self, val):
        """Initialize the UID properties

        Sets name, type, info, is_retired, and is_transfer_syntax.
        If UID is a transfer syntax, also sets is_little_endian,
            is_implicit_VR, and is_deflated boolean values.
        """
        if self in UID_dictionary:
            self.name, self.type, self.info, retired = UID_dictionary[self]
            self.is_retired = bool(retired)
        else:
            self.name = str.__str__(self)
            self.type, self.info, self.is_retired = (None, None, None)
        self.is_transfer_syntax = self.type == 'Transfer Syntax'
        if self.is_transfer_syntax:
            self.is_implicit_VR = True
            self.is_little_endian = True
            self.is_deflated = False
            if val == '1.2.840.10008.1.2':
                pass
        else:
            if val == '1.2.840.10008.1.2.1':
                self.is_implicit_VR = False
            else:
                if val == '1.2.840.10008.1.2.2':
                    self.is_implicit_VR = False
                    self.is_little_endian = False
                else:
                    if val == '1.2.840.10008.1.2.1.99':
                        self.is_deflated = True
                        self.is_implicit_VR = False
                    else:
                        self.is_implicit_VR = False

    def __str__(self):
        """Return the human-friendly name for this UID"""
        return self.name

    def __eq__(self, other):
        """Override string equality so either name or UID number match passes"""
        if str.__eq__(self, other) is True:
            return True
        if str.__eq__(self.name, other) is True:
            return True
        return False

    def __ne__(self, other):
        return not self == other

    def is_valid(self):
        """
        Raise an exception is the UID is invalid

        Usage example::

            >>> invalid_uid = dicom.UID.UID('1.2.345.')
            >>> invalid_uid.is_valid(invalid_uid)
            InvalidUID: 'Trailing dot at the end of the UID'
            >>> valid_uid = dicom.UID.UID('1.2.123')

        """
        if self[(-1)] == '.':
            raise InvalidUID('Trailing dot at the end of the UID')

    def __hash__(self):
        return super(UID, self).__hash__()


ExplicitVRLittleEndian = UID('1.2.840.10008.1.2.1')
ImplicitVRLittleEndian = UID('1.2.840.10008.1.2')
DeflatedExplicitVRLittleEndian = UID('1.2.840.10008.1.2.1.99')
ExplicitVRBigEndian = UID('1.2.840.10008.1.2.2')
NotCompressedPixelTransferSyntaxes = [
 ExplicitVRLittleEndian,
 ImplicitVRLittleEndian,
 DeflatedExplicitVRLittleEndian,
 ExplicitVRBigEndian]
pydicom_root_UID = '1.2.826.0.1.3680043.8.498.'
pydicom_UIDs = {pydicom_root_UID + '1': 'ImplementationClassUID'}

def generate_uid(prefix=pydicom_root_UID, truncate=False):
    """
    Generate a dicom unique identifier based on host id, process id and current
    time. The max lenght of the generated UID is 64 caracters.

    If the given prefix is ``None``, the UID is generated following the method
    described on `David Clunie website
    <http://www.dclunie.com/medical-image-faq/html/part2.html#UID>`_

    Usage example::

        >>> dicom.UID.generate_uid()
        1.2.826.0.1.3680043.8.498.2913212949509824014974371514
        >>> dicom.UID.generate_uid(None)
        2.25.31215762025423160614120088028604965760

    This method is inspired from the work of `DCMTK
    <http://dicom.offis.de/dcmtk.php.en>`_.

    :param prefix: The site root UID. Default to pydicom root UID.
    """
    max_uid_len = 64
    if prefix is None:
        dicom_uid = '2.25.{0}'.format(uuid.uuid1().int)
    else:
        uid_info = [
         uuid.getnode(),
         fabs(os.getpid()),
         datetime.datetime.today().second,
         datetime.datetime.today().microsecond]
        suffix = ''.join([str(int(x)) for x in uid_info])
        dicom_uid = ''.join([prefix, suffix])
    if truncate:
        dicom_uid = dicom_uid[:max_uid_len]
    dicom_uid = UID(dicom_uid)
    dicom_uid.is_valid()
    return dicom_uid