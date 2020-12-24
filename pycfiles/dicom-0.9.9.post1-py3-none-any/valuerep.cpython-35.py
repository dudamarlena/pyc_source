# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\valuerep.py
# Compiled at: 2017-01-26 21:09:38
# Size of source mod 2**32: 16119 bytes
"""Special classes for DICOM value representations (VR)"""
from decimal import Decimal
import dicom.config
from dicom.multival import MultiValue
from dicom import in_py3
import logging
logger = logging.getLogger('pydicom')
default_encoding = 'iso8859'
extra_length_VRs = ('OB', 'OW', 'OF', 'SQ', 'UN', 'UT')
text_VRs = ('SH', 'LO', 'ST', 'LT', 'UT')
import re
match_string = (b'').join([
 b'(?P<single_byte>',
 b'(?P<family_name>[^=\\^]*)',
 b'\\^?(?P<given_name>[^=\\^]*)',
 b'\\^?(?P<middle_name>[^=\\^]*)',
 b'\\^?(?P<name_prefix>[^=\\^]*)',
 b'\\^?(?P<name_suffix>[^=\\^]*)',
 b')',
 b'=?(?P<ideographic>[^=]*)',
 b'=?(?P<phonetic>[^=]*)$'])
match_string_uni = re.compile(match_string.decode('iso8859'))
match_string_bytes = re.compile(match_string)

class DSfloat(float):
    __doc__ = 'Store values for DICOM VR of DS (Decimal String) as a float.\n\n    If constructed from an empty string, return the empty string,\n    not an instance of this class.\n\n    '
    __slots__ = 'original_string'

    def __init__(self, val):
        """Store the original string if one given, for exact write-out of same
        value later.
        """
        if isinstance(val, str):
            self.original_string = val
        elif isinstance(val, (DSfloat, DSdecimal)) and hasattr(val, 'original_string'):
            self.original_string = val.original_string

    def __str__(self):
        if hasattr(self, 'original_string'):
            return self.original_string
        else:
            return super(DSfloat, self).__str__()

    def __repr__(self):
        return "'" + str(self) + "'"


class DSdecimal(Decimal):
    __doc__ = 'Store values for DICOM VR of DS (Decimal String).\n    Note: if constructed by an empty string, returns the empty string,\n    not an instance of this class.\n    '
    __slots__ = 'original_string'

    def __new__(cls, val):
        """Create an instance of DS object, or return a blank string if one is
        passed in, e.g. from a type 2 DICOM blank value.

        :param val: val must be a string or a number type which can be
                   converted to a decimal
        """
        enforce_length = dicom.config.enforce_valid_values
        if isinstance(val, str):
            val = val.strip()
            if len(val) <= 16:
                enforce_length = False
        if val == '':
            return val
        if isinstance(val, float) and not dicom.config.allow_DS_float:
            msg = 'DS cannot be instantiated with a float value, unless config.allow_DS_float is set to True. It is recommended to convert to a string instead, with the desired number of digits, or use Decimal.quantize and pass a Decimal instance.'
            raise TypeError(msg)
        if not isinstance(val, Decimal):
            val = super(DSdecimal, cls).__new__(cls, val)
        if len(str(val)) > 16 and enforce_length:
            msg = 'DS value representation must be <= 16 characters by DICOM standard. Initialize with a smaller string, or set config.enforce_valid_values to False to override, or use Decimal.quantize() and initialize with a Decimal instance.'
            raise OverflowError(msg)
        return val

    def __init__(self, val):
        """Store the original string if one given, for exact write-out of same
        value later. E.g. if set '1.23e2', Decimal would write '123', but DS
        will use the original
        """
        if isinstance(val, str):
            self.original_string = val
        elif isinstance(val, (DSfloat, DSdecimal)) and hasattr(val, 'original_string'):
            self.original_string = val.original_string

    def __str__(self):
        if hasattr(self, 'original_string') and len(self.original_string) <= 16:
            return self.original_string
        else:
            return super(DSdecimal, self).__str__()

    def __repr__(self):
        return "'" + str(self) + "'"


if dicom.config.use_DS_decimal:
    DSclass = DSdecimal
else:
    DSclass = DSfloat

def DS(val):
    """Factory function for creating DS class instances.
    Checks for blank string; if so, return that. Else calls DSfloat or DSdecimal
    to create the class instance. This avoids overriding __new__ in DSfloat
    (which carries a time penalty for large arrays of DS).
    Similarly the string clean and check can be avoided and DSfloat called
    directly if a string has already been processed.
    """
    if isinstance(val, str):
        val = val.strip()
    if val == '':
        return val
    return DSclass(val)


class IS(int):
    __doc__ = 'Derived class of int. Stores original integer string for exact rewriting\n    of the string originally read or stored.\n    '
    if not in_py3:
        __slots__ = 'original_string'

    def __new__(cls, val):
        """Create instance if new integer string"""
        if isinstance(val, str) and val.strip() == '':
            return ''
        newval = super(IS, cls).__new__(cls, val)
        if isinstance(val, (float, Decimal)) and newval != val:
            raise TypeError('Could not convert value to integer without loss')
        if (newval < -2147483648 or newval >= 2147483648) and dicom.config.enforce_valid_values:
            message = 'Value exceeds DICOM limits of -2**31 to (2**31 - 1) for IS'
            raise OverflowError(message)
        return newval

    def __init__(self, val):
        if isinstance(val, str):
            self.original_string = val
        elif isinstance(val, IS) and hasattr(val, 'original_string'):
            self.original_string = val.original_string

    def __repr__(self):
        if hasattr(self, 'original_string'):
            return "'" + self.original_string + "'"
        else:
            return "'" + int.__str__(self) + "'"


def MultiString(val, valtype=str):
    """Split a bytestring by delimiters if there are any

    val -- DICOM bytestring to split up
    valtype -- default str, but can be e.g. UID to overwrite to a specific type
    """
    if val and (val.endswith(' ') or val.endswith('\x00')):
        val = val[:-1]
    splitup = val.split('\\')
    if len(splitup) == 1:
        val = splitup[0]
        if val:
            return valtype(val)
        return val
    else:
        return MultiValue(valtype, splitup)


class PersonName3(object):

    def __init__(self, val, encodings=default_encoding):
        if isinstance(val, PersonName3):
            val = val.original_string
        self.original_string = val
        self.encodings = self._verify_encodings(encodings)
        self.parse(val)

    def parse(self, val):
        if isinstance(val, bytes):
            matchstr = match_string_bytes
        else:
            matchstr = match_string_uni
        matchobj = re.match(matchstr, val)
        self.__dict__.update(matchobj.groupdict())
        groups = matchobj.groups()
        self.components = [groups[i] for i in (0, -2, -1)]

    def __eq__(self, other):
        return self.original_string == other

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return self.original_string.__str__()

    def __repr__(self):
        return self.original_string.__repr__()

    def decode(self, encodings=None):
        encodings = self._verify_encodings(encodings)
        from dicom.charset import clean_escseq
        if not isinstance(self.components[0], bytes):
            comps = self.components
        else:
            comps = [clean_escseq(comp.decode(enc), encodings) for comp, enc in zip(self.components, encodings)]
        while len(comps) and not comps[(-1)]:
            comps.pop()

        return PersonName3('='.join(comps), encodings)

    def encode(self, encodings=None):
        encodings = self._verify_encodings(encodings)
        if isinstance(self.components[0], bytes):
            comps = self.components
        else:
            comps = [C.encode(enc) for C, enc in zip(self.components, encodings)]
        while len(comps) and not comps[(-1)]:
            comps.pop()

        return (b'=').join(comps)

    def family_comma_given(self):
        return self.formatted('%(family_name)s, %(given_name)s')

    def formatted(self, format_str):
        if isinstance(self.original_string, bytes):
            return format_str % self.decode(default_encoding).__dict__
        else:
            return format_str % self.__dict__

    def _verify_encodings(self, encodings):
        if encodings is None:
            return self.encodings
        if not isinstance(encodings, list):
            encodings = [
             encodings] * 3
        if len(encodings) == 2:
            encodings.append(encodings[1])
        return encodings


class PersonNameBase(object):
    __doc__ = 'Base class for Person Name classes'

    def __init__(self, val):
        """Initialize the PN properties"""
        self.parse()

    def formatted(self, format_str):
        """Return a formatted string according to the format pattern

        Use "...%(property)...%(property)..." where property is one of
           family_name, given_name, middle_name, name_prefix, name_suffix
        """
        return format_str % self.__dict__

    def parse(self):
        """Break down the components and name parts"""
        self.components = self.split('=')
        nComponents = len(self.components)
        self.single_byte = self.components[0]
        self.ideographic = ''
        self.phonetic = ''
        if nComponents > 1:
            self.ideographic = self.components[1]
        if nComponents > 2:
            self.phonetic = self.components[2]
        if self.single_byte:
            name_string = self.single_byte + '^^^^'
            parts = name_string.split('^')[:5]
            self.family_name, self.given_name, self.middle_name = parts[:3]
            self.name_prefix, self.name_suffix = parts[3:]
        else:
            self.family_name, self.given_name, self.middle_name, self.name_prefix, self.name_suffix = ('',
                                                                                                       '',
                                                                                                       '',
                                                                                                       '',
                                                                                                       '')


class PersonName(PersonNameBase, bytes):
    __doc__ = 'Human-friendly class to hold VR of Person Name (PN)\n\n    Name is parsed into the following properties:\n    single-byte, ideographic, and phonetic components (PS3.5-2008 6.2.1)\n    family_name,\n    given_name,\n    middle_name,\n    name_prefix,\n    name_suffix\n\n    '

    def __new__(cls, val):
        """Return instance of the new class"""
        if isinstance(val, PersonName):
            return val
        return super(PersonName, cls).__new__(cls, val)

    def encode(self, *args):
        """Dummy method to mimic py2 str behavior in py3 bytes subclass"""
        return self

    def family_comma_given(self):
        """Return name as 'Family-name, Given-name'"""
        return self.formatted('%(family_name)s, %(given_name)s')


class PersonNameUnicode(PersonNameBase, str):
    __doc__ = 'Unicode version of Person Name'

    def __new__(cls, val, encodings):
        """Return unicode string after conversion of each part
        val -- the PN value to store
        encodings -- a list of python encodings, generally found
                 from dicom.charset.python_encodings mapping
                 of values in DICOM data element (0008,0005).
        """
        from dicom.charset import clean_escseq
        if not isinstance(encodings, list):
            encodings = [
             encodings] * 3
        if len(encodings) == 2:
            encodings.append(encodings[1])
        components = val.split(b'=')
        if len(components) == 1:
            del encodings[0]
        comps = [clean_escseq(C.decode(enc), encodings) for C, enc in zip(components, encodings)]
        new_val = '='.join(comps)
        return str.__new__(cls, new_val)

    def __init__(self, val, encodings):
        self.encodings = self._verify_encodings(encodings)
        PersonNameBase.__init__(self, val)

    def _verify_encodings(self, encodings):
        """Checks the encoding to ensure proper format"""
        if encodings is None:
            return self.encodings
        if not isinstance(encodings, list):
            encodings = [
             encodings] * 3
        if len(encodings) == 2:
            encodings.append(encodings[1])
        return encodings

    def encode(self, encodings):
        """Encode the unicode using the specified encoding"""
        encodings = self._verify_encodings(encodings)
        components = self.split('=')
        comps = [C.encode(enc) for C, enc in zip(components, encodings)]
        while len(comps) and not comps[(-1)]:
            comps.pop()

        return '='.join(comps)

    def family_comma_given(self):
        """Return name as 'Family-name, Given-name'"""
        return self.formatted('%(family_name)u, %(given_name)u')