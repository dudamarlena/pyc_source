# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/messaging/codes.py
# Compiled at: 2014-01-14 18:58:51
"""
Message codes and constants.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'MessageType', 'MessageCode', 'MessagePriority',
 'MSG_PRIORITIES', 'MSG_TYPES', 'MSG_CODES',
 'MSG_DATA_CODES', 'MSG_RPC_CODES',
 'MSG_CONTROL_CODES', 'MSG_STATUS_CODES']
from ..common import Singleton

class MessageConstants(Singleton):
    """
    Base class for message constants enumerations.
    """

    @classmethod
    def get_names(cls):
        """
        Get the names of all constants defined here.

        :returns: Names of the constants.
        :rtype: set(str)
        """
        return {name for name in dir(cls) if name.startswith('MSG_') if name.startswith('MSG_')}

    @classmethod
    def get_values(cls):
        """
        Get the values of all constants defined here.

        :returns: Values of the constants.
        :rtype: set(int)
        """
        return {getattr(cls, name) for name in dir(cls) if name.startswith('MSG_')}

    @classmethod
    def get_name_from_value(cls, value, prefix='MSG_'):
        """
        Finds a constant name based on its numeric value.

        :param value: Value of the constant.
        :type value: int

        :param prefix: Prefix of the constant.
        :type prefix: str

        :returns: Name of the constant.
        :rtype: str
        """
        if not prefix:
            raise ValueError('Missing prefix!')
        for name in dir(cls):
            if name.startswith(prefix) and getattr(cls, name) == value:
                return name


class MessagePriority(MessageConstants):
    MSG_PRIORITY_HIGH = 0
    MSG_PRIORITY_MEDIUM = 1
    MSG_PRIORITY_LOW = 2


class MessageType(MessageConstants):
    MSG_TYPE_DATA = 0
    MSG_TYPE_CONTROL = 1
    MSG_TYPE_RPC = 2
    MSG_TYPE_STATUS = 3


class MessageCode(MessageConstants):
    __prefix_for_type = {MessageType.MSG_TYPE_DATA: 'MSG_DATA_', 
       MessageType.MSG_TYPE_CONTROL: 'MSG_CONTROL_', 
       MessageType.MSG_TYPE_RPC: 'MSG_RPC_', 
       MessageType.MSG_TYPE_STATUS: 'MSG_STATUS_'}

    @classmethod
    def get_name_from_value_and_type(cls, value, message_type):
        """
        Finds a constant name based on its numeric value.

        :param value: Value of the constant.
        :type value: int

        :param message_type: Message type. Must be one of the constants from MessageType.
        :type mesage_type: int

        :returns: Name of the constant.
        :rtype: str
        """
        if type(message_type) != int:
            raise TypeError('Expected int, got %r instead' % type(message_type))
        try:
            prefix = cls.__prefix_for_type[message_type]
        except KeyError:
            raise ValueError('Invalid message type: %d' % message_type)

        return cls.get_name_from_value(value, prefix)

    MSG_DATA_REQUEST = 0
    MSG_DATA_RESPONSE = 1
    MSG_CONTROL_ACK = 0
    MSG_CONTROL_ERROR = 1
    MSG_CONTROL_WARNING = 2
    MSG_CONTROL_LOG = 3
    MSG_CONTROL_STOP = 5
    MSG_CONTROL_START_AUDIT = 10
    MSG_CONTROL_STOP_AUDIT = 11
    MSG_CONTROL_START_UI = 20
    MSG_CONTROL_STOP_UI = 21
    MSG_RPC_BULK = 0
    MSG_RPC_REQUEST_SLOT = 1
    MSG_RPC_RELEASE_SLOT = 2
    MSG_RPC_CACHE_GET = 3
    MSG_RPC_CACHE_SET = 4
    MSG_RPC_CACHE_CHECK = 5
    MSG_RPC_CACHE_REMOVE = 6
    MSG_RPC_DATA_ADD = 10
    MSG_RPC_DATA_ADD_MANY = 11
    MSG_RPC_DATA_REMOVE = 12
    MSG_RPC_DATA_REMOVE_MANY = 13
    MSG_RPC_DATA_CHECK = 14
    MSG_RPC_DATA_GET = 15
    MSG_RPC_DATA_GET_MANY = 16
    MSG_RPC_DATA_KEYS = 17
    MSG_RPC_DATA_COUNT = 18
    MSG_RPC_DATA_PLUGINS = 19
    MSG_RPC_PLUGIN_GET_IDS = 20
    MSG_RPC_PLUGIN_GET_INFO = 21
    MSG_RPC_AUDIT_COUNT = 30
    MSG_RPC_AUDIT_NAMES = 31
    MSG_RPC_AUDIT_CONFIG = 32
    MSG_RPC_AUDIT_TIMES = 33
    MSG_RPC_AUDIT_STATS = 34
    MSG_RPC_AUDIT_LOG = 35
    MSG_RPC_AUDIT_SCOPE = 36
    MSG_RPC_SHARED_MAP_GET = 40
    MSG_RPC_SHARED_MAP_CHECK_ALL = 41
    MSG_RPC_SHARED_MAP_CHECK_ANY = 42
    MSG_RPC_SHARED_MAP_CHECK_EACH = 43
    MSG_RPC_SHARED_MAP_POP = 44
    MSG_RPC_SHARED_MAP_PUT = 45
    MSG_RPC_SHARED_MAP_SWAP = 46
    MSG_RPC_SHARED_MAP_DELETE = 47
    MSG_RPC_SHARED_MAP_KEYS = 48
    MSG_RPC_SHARED_HEAP_CHECK_ALL = 50
    MSG_RPC_SHARED_HEAP_CHECK_ANY = 51
    MSG_RPC_SHARED_HEAP_CHECK_EACH = 52
    MSG_RPC_SHARED_HEAP_POP = 53
    MSG_RPC_SHARED_HEAP_ADD = 54
    MSG_RPC_SHARED_HEAP_REMOVE = 55
    MSG_STATUS_STAGE_UPDATE = 0
    MSG_STATUS_PLUGIN_BEGIN = 1
    MSG_STATUS_PLUGIN_END = 2
    MSG_STATUS_PLUGIN_STEP = 3
    MSG_STATUS_AUDIT_ABORTED = 4


MSG_PRIORITIES = MessagePriority.get_values()
MSG_TYPES = MessageType.get_values()
MSG_CODES = MessageCode.get_values()
MSG_DATA_CODES = {getattr(MessageCode, x) for x in MessageCode.get_names() if x.startswith('MSG_DATA_') if x.startswith('MSG_DATA_')}
MSG_CONTROL_CODES = {getattr(MessageCode, x) for x in MessageCode.get_names() if x.startswith('MSG_CONTROL_') if x.startswith('MSG_CONTROL_')}
MSG_RPC_CODES = {getattr(MessageCode, x) for x in MessageCode.get_names() if x.startswith('MSG_RPC_') if x.startswith('MSG_RPC_')}
MSG_STATUS_CODES = {getattr(MessageCode, x) for x in MessageCode.get_names() if x.startswith('MSG_STATUS_') if x.startswith('MSG_STATUS_')}