# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\config.py
# Compiled at: 2017-01-26 21:08:30
# Size of source mod 2**32: 1389 bytes
"""Pydicom configuration options."""
use_DS_decimal = False

def DS_decimal(use_Decimal_boolean=True):
    """Set DS class to be derived from Decimal (True) or from float (False)
    If this function is never called, the default in pydicom >= 0.9.8
    is for DS to be based on float.
    """
    use_DS_decimal = use_Decimal_boolean
    import dicom.valuerep
    if use_DS_decimal:
        dicom.valuerep.DSclass = dicom.valuerep.DSdecimal
    else:
        dicom.valuerep.DSclass = dicom.valuerep.DSfloat


allow_DS_float = False
enforce_valid_values = True