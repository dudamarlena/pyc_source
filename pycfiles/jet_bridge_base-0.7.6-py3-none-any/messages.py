# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/messages.py
# Compiled at: 2019-10-12 07:46:27
GET_ACTION_LIST = 'get_action_list'
EXECUTE_ACTION = 'execute_action'
message_handlers = {}

def add_handler(message_name, func):
    message_handlers[message_name] = func


def get_handler(message_name):
    return message_handlers.get(message_name)