# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\charset.py
# Compiled at: 2017-01-26 21:09:36
# Size of source mod 2**32: 5124 bytes
"""Handle alternate character sets for character strings."""
import logging
logger = logging.getLogger('pydicom')
from dicom.valuerep import PersonNameUnicode, text_VRs
from dicom import in_py3
python_encoding = {'': 'iso8859', 
 'ISO_IR 6': 'iso8859', 
 'ISO_IR 100': 'latin_1', 
 'ISO 2022 IR 87': 'iso2022_jp', 
 'ISO 2022 IR 13': 'shift_jis', 
 'ISO 2022 IR 149': 'euc_kr', 
 'ISO_IR 192': 'UTF8', 
 'GB18030': 'GB18030', 
 'ISO_IR 126': 'iso_ir_126', 
 'ISO_IR 127': 'iso_ir_127', 
 'ISO_IR 138': 'iso_ir_138', 
 'ISO_IR 144': 'iso_ir_144'}
default_encoding = 'iso8859'

def clean_escseq(element, encodings):
    """Remove escape sequences that Python does not remove from
       Korean encoding ISO 2022 IR 149 due to the G1 code element.
    """
    if 'euc_kr' in encodings:
        return element.replace('\x1b$)C', '').replace('\x1b(B', '')
    else:
        return element


def convert_encodings(encodings):
    """Converts DICOM encodings into corresponding python encodings"""
    encodings = encodings[:]
    if isinstance(encodings, str):
        encodings = [
         encodings]
    else:
        if not encodings[0]:
            encodings[0] = 'ISO_IR 6'
        try:
            encodings = [python_encoding[x] for x in encodings]
        except KeyError:
            pass

        if len(encodings) == 1:
            encodings = [
             encodings[0]] * 3
        elif len(encodings) == 2:
            encodings.append(encodings[1])
    return encodings


def decode(data_element, dicom_character_set):
    """Apply the DICOM character encoding to the data element

    data_element -- DataElement instance containing a value to convert
    dicom_character_set -- the value of Specific Character Set (0008,0005),
                    which may be a single value,
                    a multiple value (code extension), or
                    may also be '' or None.
                    If blank or None, ISO_IR 6 is used.

    """
    if not dicom_character_set:
        dicom_character_set = [
         'ISO_IR 6']
    encodings = convert_encodings(dicom_character_set)
    if data_element.VR == 'PN':
        if in_py3:
            if data_element.VM == 1:
                data_element.value = data_element.value.decode(encodings)
        else:
            data_element.value = [val.decode(encodings) for val in data_element.value]
    else:
        if data_element.VM == 1:
            data_element.value = PersonNameUnicode(data_element.value, encodings)
        else:
            data_element.value = [PersonNameUnicode(value, encodings) for value in data_element.value]
        if data_element.VR in text_VRs:
            pass
        if len(encodings) > 1:
            del encodings[0]
        if data_element.VM == 1:
            if isinstance(data_element.value, str):
                return
            data_element.value = clean_escseq(data_element.value.decode(encodings[0]), encodings)
        else:
            output = list()
            for value in data_element.value:
                if isinstance(value, str):
                    output.append(value)
                else:
                    output.append(clean_escseq(value.decode(encodings[0]), encodings))

            data_element.value = output