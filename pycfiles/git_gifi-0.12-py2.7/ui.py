# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gifi/utils/ui.py
# Compiled at: 2017-06-14 09:08:44
from gifi.command import CommandException

def ask(question, value):
    raw_value = raw_input('%s (%s): ' % (question, value))
    if raw_value is not '':
        value = parse_value(raw_value, type(value))
    return value


def parse_value(rawValue, destType):
    rawValue = str(rawValue)
    if destType is bool:
        if rawValue in ('True', 'true', 'yes', '1'):
            return True
        if rawValue in ('False', 'false', 'no', '0'):
            return False
        raise CommandException("Wrong value '%s' (with: %s) for '%s'" % (rawValue, type(rawValue), destType))
    else:
        if destType is str:
            return rawValue
        if destType is unicode:
            return rawValue
        if destType is int:
            return int(rawValue)
        raise CommandException('Unsupported type: %s' % destType)