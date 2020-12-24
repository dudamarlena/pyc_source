# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/sqlutils.py
# Compiled at: 2003-09-14 19:12:16
"""A few simple SQL-code manipulation functions"""

def characterType(dbDataType):
    """Is this a character data-type?"""
    likelyCharTypes = ('char', 'byte', 'text', 'inet', 'bool')
    dbDataType = dbDataType.lower()
    for typ in likelyCharTypes:
        if dbDataType.find(typ) > -1:
            return typ

    return None


def sqlEscape(value, encoding='utf-8', dbDataType=''):
    """Perform SQL escaping on given (string) value"""
    if isinstance(value, unicode):
        value = value.encode(encoding)
    if characterType(dbDataType) or isinstance(value, str):
        value = str(value)
        value = value.replace("'", "''").replace('\\', '\\\\')
        return "'%s'" % value
    else:
        return repr(value)