# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/utctime.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 2071 bytes
"""
web2ldap.utctime - various functions for parsing display UTCTime

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import time, datetime
UTC_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

def strptime(s):
    if isinstance(s, bytes):
        s = s.decode('ascii')
    else:
        len_dt_str = len(s)
        if s[(-1)].upper() == 'Z':
            if len_dt_str == 15:
                dt = datetime.datetime.strptime(s, '%Y%m%d%H%M%SZ')
                return dt
            elif len_dt_str == 13:
                dt = datetime.datetime.strptime(s, '%y%m%d%H%M%SZ')
                return dt
                if len_dt_str > 16:
                    s = s[:-1]
                    tz_offset = datetime.timedelta(0)
                else:
                    raise ValueError('Could not determine UTC time format of %r' % s)
            elif len_dt_str >= 19 and s[(-5)] in {'-', '+'}:
                tzstr = s[-4:]
                tz_offset = datetime.timedelta(hours=(int(tzstr[0:2])),
                  minutes=(int(tzstr[2:4])))
                s = s[:-5]
            else:
                raise ValueError('Time zone part missing in %r' % s)
            s = s.replace(',', '.')
            if '.' in s:
                dt = datetime.datetime.strptime(s, '%Y%m%d%H%M%S.%f')
        else:
            dt = datetime.datetime.strptime(s, '%Y%m%d%H%M%S')
    return dt - tz_offset


def strftimeiso8601--- This code section failed: ---

 L.  68         0  SETUP_FINALLY        14  'to 14'

 L.  69         2  LOAD_FAST                't'
                4  LOAD_METHOD              strftime
                6  LOAD_GLOBAL              UTC_TIME_FORMAT
                8  CALL_METHOD_1         1  ''
               10  POP_BLOCK        
               12  RETURN_VALUE     
             14_0  COME_FROM_FINALLY     0  '0'

 L.  70        14  DUP_TOP          
               16  LOAD_GLOBAL              AttributeError
               18  COMPARE_OP               exception-match
               20  POP_JUMP_IF_FALSE    44  'to 44'
               22  POP_TOP          
               24  POP_TOP          
               26  POP_TOP          

 L.  71        28  LOAD_GLOBAL              time
               30  LOAD_METHOD              strftime
               32  LOAD_GLOBAL              UTC_TIME_FORMAT
               34  LOAD_FAST                't'
               36  CALL_METHOD_2         2  ''
               38  ROT_FOUR         
               40  POP_EXCEPT       
               42  RETURN_VALUE     
             44_0  COME_FROM            20  '20'
               44  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 24