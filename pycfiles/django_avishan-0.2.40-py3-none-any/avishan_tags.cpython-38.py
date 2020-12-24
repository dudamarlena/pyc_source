# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/afshari9978/Projects/namaki_backend/avishan/templatetags/avishan_tags.py
# Compiled at: 2020-04-21 05:34:59
# Size of source mod 2**32: 767 bytes
from django import template
from django.db import models
from avishan.models import AvishanModel
register = template.Library()

@register.filter
def translator--- This code section failed: ---

 L.  12         0  LOAD_STR                 'شماره همراه'

 L.  13         2  LOAD_STR                 'ایمیل'

 L.  11         4  LOAD_CONST               ('phone', 'email')
                6  BUILD_CONST_KEY_MAP_2     2 
                8  STORE_FAST               'data'

 L.  15        10  SETUP_FINALLY        26  'to 26'

 L.  16        12  LOAD_FAST                'data'
               14  LOAD_FAST                'value'
               16  LOAD_METHOD              lower
               18  CALL_METHOD_0         0  ''
               20  BINARY_SUBSCR    
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    10  '10'

 L.  17        26  DUP_TOP          
               28  LOAD_GLOBAL              KeyError
               30  COMPARE_OP               exception-match
               32  POP_JUMP_IF_FALSE    48  'to 48'
               34  POP_TOP          
               36  POP_TOP          
               38  POP_TOP          

 L.  18        40  LOAD_FAST                'value'
               42  ROT_FOUR         
               44  POP_EXCEPT       
               46  RETURN_VALUE     
             48_0  COME_FROM            32  '32'
               48  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 36


@register.filter
def leading_zeros(value, desired_digits):
    """
    Given an integer, returns a string representation, padded with [desired_digits] zeros.
    """
    num_zeros = int(desired_digits) - len(str(value))
    padded_value = []
    while num_zeros >= 1:
        padded_value.append('0')
        num_zeros = num_zeros - 1

    padded_value.append(str(value))
    return ''.join(padded_value)