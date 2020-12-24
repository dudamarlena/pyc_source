# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/utils.py
# Compiled at: 2015-10-04 18:11:45
import sys, operator

def python3_or_better():
    return sys.version_info.major >= 3


def python2():
    return sys.version_info.major == 2


if python3_or_better():

    def cxString_from_ascii(a_str):
        return a_str.decode('ascii')


    def cxString_from_encoded_string(a_str, encoding):
        return a_str.decode(encoding)


else:

    def cxString_from_ascii(a_str):
        return a_str


    def cxString_from_encoded_string(a_str, encoding):
        return a_str


try:
    bytes = bytes
except NameError:
    bytes = str

if python3_or_better():
    cxBinary = bytes
    cxString = unicode
else:
    cxBinary = buffer
    cxString = bytes
is_sequence = operator.isSequenceType
DRIVER_NAME = 'cx_Oracle-0.1'
MAX_STRING_CHARS = 4000
MAX_BINARY_BYTES = 4000