# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/hbmqtt/errors.py
# Compiled at: 2020-01-25 09:04:28
# Size of source mod 2**32: 531 bytes


class HBMQTTException(Exception):
    __doc__ = '\n    HBMQTT base exception\n    '


class MQTTException(Exception):
    __doc__ = '\n    Base class for all errors refering to MQTT specifications\n    '


class CodecException(Exception):
    __doc__ = '\n    Exceptions thrown by packet encode/decode functions\n    '


class NoDataException(Exception):
    __doc__ = '\n    Exceptions thrown by packet encode/decode functions\n    '