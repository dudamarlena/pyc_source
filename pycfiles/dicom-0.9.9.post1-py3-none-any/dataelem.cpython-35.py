# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\dataelem.py
# Compiled at: 2017-01-26 21:09:36
# Size of source mod 2**32: 12612 bytes
"""Define the DataElement class - elements within a dataset.

DataElements have a DICOM value representation VR, a value multiplicity VM,
and a value.
"""
import logging
logger = logging.getLogger('pydicom')
from dicom.datadict import dictionary_has_tag, dictionary_description
from dicom.datadict import private_dictionary_description, dictionaryVR
from dicom.tag import Tag
from dicom.UID import UID
import dicom.valuerep
from dicom import in_py3
if in_py3:
    from dicom.valuerep import PersonName3 as PersonNameUnicode
    PersonName = PersonNameUnicode
from collections import namedtuple

def isMultiValue(value):
    """Helper function: return True if 'value' is 'list-like'."""
    if isString(value) or isinstance(value, bytes):
        return False
        try:
            iter(value)
        except TypeError:
            return False

        return True


def isString(val):
    """Helper function: return True if val is a string."""
    return isinstance(val, str)


def isStringOrStringList(val):
    """Return true if val consists only of strings. val may be a list/tuple."""
    if isMultiValue(val):
        for item in val:
            if not isString(item):
                return False

        return True
    else:
        return isString(val)


_backslash = '\\'

class DataElement(object):
    __doc__ = 'Contain and manipulate a Dicom data element, having a tag, VR, VM and value.\n\n    Most user code will not create data elements using this class directly,\n    but rather through DICOM keywords in Dataset objects.\n    See the Dataset class for a description of how Datasets, Sequences,\n    and DataElements work.\n\n    Class Data\n    ----------\n    For string display (via __str__), the following are used:\n\n    descripWidth -- maximum width of description field (default 35).\n    maxBytesToDisplay -- longer data will display "array of # bytes" (default 16).\n    showVR -- True (default) to include the dicom VR just before the value.\n    '
    descripWidth = 35
    maxBytesToDisplay = 16
    showVR = 1

    def __init__(self, tag, VR, value, file_value_tell=None, is_undefined_length=False, already_converted=False):
        """Create a data element instance.

        Most user code should instead use DICOM keywords
        to create data_elements, for which only the value is supplied,
        and the VR and tag are determined from the dicom dictionary.

        tag -- dicom (group, element) tag in any form accepted by Tag().
        VR -- dicom value representation (see DICOM standard part 6)
        value -- the value of the data element. One of the following:
            - a single string value
            - a number
            - a list or tuple with all strings or all numbers
            - a multi-value string with backslash separator
        file_value_tell -- used internally by Dataset, to store the write
            position for ReplaceDataElementValue method
        is_undefined_length -- used internally to store whether the length
            field in this data element was 0xFFFFFFFFL, i.e. "undefined length"

        """
        self.tag = Tag(tag)
        self.VR = VR
        if already_converted:
            self._value = value
        else:
            self.value = value
        self.file_tell = file_value_tell
        self.is_undefined_length = is_undefined_length

    @property
    def value(self):
        """The value (possibly multiple values) of this data_element"""
        return self._value

    @value.setter
    def value(self, val):
        """Set method for 'value' property"""
        if isString(val) and self.VR not in ('UT', 'ST', 'LT', 'FL', 'FD', 'AT', 'OB',
                                             'OW', 'OF', 'SL', 'SQ', 'SS', 'UL',
                                             'OB/OW', 'OW/OB', 'OB or OW', 'OW or OB',
                                             'UN') and 'US' not in self.VR and _backslash in val:
            val = val.split(_backslash)
        self._value = self._convert_value(val)

    @property
    def VM(self):
        """The number of values in the data_element's 'value'"""
        if isMultiValue(self.value):
            return len(self.value)
        else:
            return 1

    def _convert_value(self, val):
        """Convert Dicom string values if possible to e.g. numbers. Handle the case
        of multiple value data_elements"""
        if self.VR == 'SQ':
            from dicom.sequence import Sequence
            if isinstance(val, Sequence):
                return val
            else:
                return Sequence(val)
            try:
                val.append
            except AttributeError:
                return self._convert(val)
            else:
                returnvalue = []
                for subval in val:
                    returnvalue.append(self._convert(subval))

                return returnvalue

    def _convert(self, val):
        """Take the value and convert to number, etc if possible"""
        if self.VR == 'IS':
            return dicom.valuerep.IS(val)
        else:
            if self.VR == 'DS':
                return dicom.valuerep.DS(val)
            if self.VR == 'UI':
                return UID(val)
            if in_py3 and self.VR == 'PN':
                return PersonName(val)
            return val

    def __str__(self):
        """Return str representation of this data_element"""
        repVal = self.repval
        if self.showVR:
            s = '%s %-*s %s: %s' % (str(self.tag), self.descripWidth,
             self.description()[:self.descripWidth], self.VR, repVal)
        else:
            s = '%s %-*s %s' % (str(self.tag), self.descripWidth,
             self.description()[:self.descripWidth], repVal)
        return s

    @property
    def repval(self):
        """Return a str representation of the current value for use in __str__"""
        byte_VRs = [
         'OB', 'OW', 'OW/OB', 'OW or OB', 'OB or OW', 'US or SS or OW', 'US or SS']
        if self.VR in byte_VRs and len(self.value) > self.maxBytesToDisplay:
            repVal = 'Array of %d bytes' % len(self.value)
        else:
            if hasattr(self, 'original_string'):
                repVal = repr(self.original_string)
            else:
                if isinstance(self.value, UID):
                    repVal = self.value.name
                else:
                    repVal = repr(self.value)
        return repVal

    def __unicode__(self):
        """Return unicode representation of this data_element"""
        if isinstance(self.value, str):
            strVal = str(self)
            uniVal = str(strVal.replace(self.repval, '')) + self.value
            return uniVal
        else:
            return str(str(self))

    def __getitem__(self, key):
        """Returns the item from my value's Sequence, if it is one."""
        try:
            return self.value[key]
        except TypeError:
            raise TypeError('DataElement value is unscriptable (not a Sequence)')

    @property
    def name(self):
        return self.description()

    def description(self):
        """Return the DICOM dictionary description for this dicom tag."""
        if dictionary_has_tag(self.tag):
            name = dictionary_description(self.tag)
        else:
            if self.tag.is_private:
                name = 'Private tag data'
                if hasattr(self, 'private_creator'):
                    try:
                        name = '[' + private_dictionary_description(self.tag, self.private_creator) + ']'
                    except KeyError:
                        pass

                elif self.tag.elem >> 8 == 0:
                    name = 'Private Creator'
            else:
                if self.tag.element == 0:
                    name = 'Group Length'
                else:
                    name = ''
        return name

    def __repr__(self):
        """Handle repr(data_element)"""
        if self.VR == 'SQ':
            return repr(self.value)
        else:
            return str(self)


class DeferredDataElement(DataElement):
    __doc__ = 'Subclass of DataElement where value is not read into memory until needed'

    def __init__(self, tag, VR, fp, file_mtime, data_element_tell, length):
        """Store basic info for the data element but value will be read later

        fp -- DicomFile object representing the dicom file being read
        file_mtime -- last modification time on file, used to make sure
           it has not changed since original read
        data_element_tell -- file position at start of data element,
           (not the start of the value part, but start of whole element)
        """
        self.tag = Tag(tag)
        self.VR = VR
        self._value = None
        self.fp_is_implicit_VR = fp.is_implicit_VR
        self.fp_is_little_endian = fp.is_little_endian
        self.filepath = fp.name
        self.file_mtime = file_mtime
        self.data_element_tell = data_element_tell
        self.length = length

    @property
    def repval(self):
        if self._value is None:
            return 'Deferred read: length %d' % self.length
        else:
            return DataElement.repval.fget(self)

    @property
    def value(self):
        """Get method for 'value' property"""
        if self._value is None:
            self.read_value()
        return DataElement.value.fget(self)

    @value.setter
    def value(self, val):
        DataElement.value.fset(self, val)


RawDataElement = namedtuple('RawDataElement', 'tag VR length value value_tell is_implicit_VR is_little_endian')

def DataElement_from_raw(raw_data_element, encoding=None):
    """Return a DataElement from a RawDataElement"""
    from dicom.values import convert_value
    raw = raw_data_element
    VR = raw.VR
    if VR is None:
        try:
            VR = dictionaryVR(raw.tag)
        except KeyError:
            if raw.tag.is_private:
                VR = 'OB'
            else:
                if raw.tag.element == 0:
                    VR = 'UL'
                else:
                    raise KeyError("Unknown DICOM tag {0:s} - can't look up VR".format(str(raw.tag)))

    try:
        value = convert_value(VR, raw, encoding)
    except NotImplementedError as e:
        raise NotImplementedError('{0:s} in tag {1!r}'.format(str(e), raw.tag))

    return DataElement(raw.tag, VR, value, raw.value_tell, raw.length == 4294967295, already_converted=True)