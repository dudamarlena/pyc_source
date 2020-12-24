# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/FakeWebware/MiscUtils/CSVJoiner.py
# Compiled at: 2006-10-22 17:01:01
import types

def joinCSVFields(fields):
    """
        Returns a CSV record (eg a string) from a sequence of fields.
        Fields containing commands (,) or double quotes (") are quotes
        and double quotes are escaped (""). The terminating newline is
        NOT included.
        """
    newFields = []
    for field in fields:
        assert type(field) is types.StringType
        if field.find('"') != -1:
            newField = '"' + field.replace('"', '""') + '"'
        elif field.find(',') != -1 or field.find('\n') != -1 or field.find('\r') != -1:
            newField = '"' + field + '"'
        else:
            newField = field
        newFields.append(newField)

    return (',').join(newFields)