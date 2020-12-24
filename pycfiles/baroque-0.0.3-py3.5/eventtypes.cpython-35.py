# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/baroque/exceptions/eventtypes.py
# Compiled at: 2017-03-03 13:37:20
# Size of source mod 2**32: 287 bytes


class UnregisteredEventTypeError(Exception):
    __doc__ = 'Raised when attempting to publish on the broker events of an\n    unregistered type'


class InvalidEventSchemaError(Exception):
    __doc__ = 'Raised when the event validation against its eventtype JSON\n    schema fails'