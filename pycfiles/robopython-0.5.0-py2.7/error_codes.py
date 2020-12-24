# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\robopython\pygatt\backends\bgapi\error_codes.py
# Compiled at: 2020-03-04 11:05:11
from __future__ import print_function
from enum import Enum

class ErrorCode(Enum):
    insufficient_authentication = 1029


return_codes = {0: 'Success', 
   384: 'Invalid parameter', 
   385: 'Device in wrong state', 
   386: 'Out of memory', 
   387: 'Feature not implemented', 
   388: 'Command not recognized', 
   389: 'Timeout', 
   390: 'Not connected', 
   391: 'Overflow/underflow', 
   392: 'User attribute', 
   393: 'Invalid liscense key', 
   394: 'Command too long', 
   395: 'Out of bounds', 
   517: 'Authentication failure', 
   518: 'Pin or key missing', 
   519: 'Memory capacity exceeded', 
   520: 'Connection timeout', 
   521: 'Connection limit exceeded', 
   524: 'Command disallowed', 
   530: 'Invalid command parameters', 
   531: 'Remote user terminated connection', 
   534: 'Connection terminated by local host', 
   546: 'Link layer reponse timeout', 
   552: 'Link layer instance passed', 
   570: 'Controller busy', 
   571: 'Unacceptable connection interval', 
   572: 'Directed advertising timeout', 
   573: 'MIC failure', 
   574: 'Connection failed to be established', 
   769: 'Passkey entry failed', 
   770: 'OOB data is not available', 
   771: 'Authentication requirements', 
   772: 'Confirm value failed', 
   773: 'Pairing not supported', 
   774: 'Encryption key size', 
   775: 'Command not supported', 
   776: 'Unspecified reason', 
   777: 'Repeated attempts', 
   778: 'Invalid parameters', 
   1025: 'Invalid handle', 
   1026: 'Read not permitted', 
   1027: 'Write not permitted', 
   1028: 'Invalid PDU', 
   ErrorCode.insufficient_authentication.value: 'Insufficient authentication', 
   1030: 'Request not supported', 
   1031: 'Invalid offset', 
   1032: 'Insufficient authorization', 
   1033: 'Prepare queue full', 
   1034: 'Attribute not found', 
   1035: 'Attribute not long', 
   1036: 'Insufficient encryption key size', 
   1037: 'Invalid attribute value length', 
   1038: 'Unlikely error', 
   1039: 'Insufficient encryption', 
   1040: 'Unsupported group type', 
   1041: 'Insufficient resources', 
   1152: 'Application error codes'}

def get_return_message(return_code):
    try:
        return return_codes[return_code]
    except KeyError:
        return 'Unknown return code %04x' % return_code