# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/asyncbots/events.py
# Compiled at: 2018-08-17 15:12:41
# Size of source mod 2**32: 1116 bytes
"""Module with helper functions for working with raw Slack API events"""
from functools import partial

def is_message--- This code section failed: ---

 L.   6         0  LOAD_STR                 'type'
                2  LOAD_FAST                'event'
                4  COMPARE_OP               in
                6  JUMP_IF_FALSE_OR_POP    78  'to 78'
                8  LOAD_FAST                'event'
               10  LOAD_STR                 'type'
               12  BINARY_SUBSCR    
               14  LOAD_STR                 'message'
               16  COMPARE_OP               ==
               18  JUMP_IF_FALSE_OR_POP    78  'to 78'

 L.   7        20  LOAD_FAST                'no_channel'
               22  POP_JUMP_IF_TRUE     40  'to 40'
               24  LOAD_STR                 'channel'
               26  LOAD_FAST                'event'
               28  COMPARE_OP               in
               30  JUMP_IF_FALSE_OR_POP    78  'to 78'
               32  LOAD_FAST                'event'
               34  LOAD_STR                 'channel'
               36  BINARY_SUBSCR    
               38  JUMP_IF_FALSE_OR_POP    78  'to 78'
             40_0  COME_FROM            22  '22'

 L.   8        40  LOAD_STR                 'text'
               42  LOAD_FAST                'event'
               44  COMPARE_OP               in
               46  JUMP_IF_FALSE_OR_POP    78  'to 78'

 L.   9        48  LOAD_STR                 'reply_to'
               50  LOAD_FAST                'event'
               52  COMPARE_OP               not-in
               54  JUMP_IF_FALSE_OR_POP    78  'to 78'

 L.  10        56  LOAD_STR                 'subtype'
               58  LOAD_FAST                'event'
               60  COMPARE_OP               not-in
               62  JUMP_IF_FALSE_OR_POP    78  'to 78'

 L.  11        64  LOAD_STR                 'bot_id'
               66  LOAD_FAST                'event'
               68  COMPARE_OP               not-in
               70  JUMP_IF_FALSE_OR_POP    78  'to 78'

 L.  12        72  LOAD_FAST                'event'
               74  LOAD_STR                 'text'
               76  BINARY_SUBSCR    
             78_0  COME_FROM            70  '70'
             78_1  COME_FROM            62  '62'
             78_2  COME_FROM            54  '54'
             78_3  COME_FROM            46  '46'
             78_4  COME_FROM            38  '38'
             78_5  COME_FROM            30  '30'
             78_6  COME_FROM            18  '18'
             78_7  COME_FROM             6  '6'
               78  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 78_7


def _type_is(e_type, event):
    """Helper function for checking event types"""
    return 'type' in event and event['type'] == e_type


is_group_join = partial(_type_is, 'group_joined')
is_team_join = partial(_type_is, 'team_join')
is_goodbye = partial(_type_is, 'goodbye')

def is_response(event):
    """Check whether an event is a response indicating a message was successfully sent"""
    return 'reply_to' in event and 'ok' in event and event['ok']