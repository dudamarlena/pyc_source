# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/google/protobuf/text_format.py
# Compiled at: 2009-12-02 20:07:05
"""Contains routines for printing protocol messages in text format."""
__author__ = 'kenton@google.com (Kenton Varda)'
import cStringIO
from google.protobuf import descriptor
__all__ = [
 'MessageToString', 'PrintMessage', 'PrintField', 'PrintFieldValue']

def MessageToString(message):
    out = cStringIO.StringIO()
    PrintMessage(message, out)
    result = out.getvalue()
    out.close()
    return result


def PrintMessage(message, out, indent=0):
    for (field, value) in message.ListFields():
        if field.label == descriptor.FieldDescriptor.LABEL_REPEATED:
            for element in value:
                PrintField(field, element, out, indent)

        else:
            PrintField(field, value, out, indent)


def PrintField(field, value, out, indent=0):
    """Print a single field name/value pair.  For repeated fields, the value
  should be a single element."""
    out.write(' ' * indent)
    if field.is_extension:
        out.write('[')
        if field.containing_type.GetOptions().message_set_wire_format and field.type == descriptor.FieldDescriptor.TYPE_MESSAGE and field.message_type == field.extension_scope and field.label == descriptor.FieldDescriptor.LABEL_OPTIONAL:
            out.write(field.message_type.full_name)
        else:
            out.write(field.full_name)
        out.write(']')
    elif field.type == descriptor.FieldDescriptor.TYPE_GROUP:
        out.write(field.message_type.name)
    else:
        out.write(field.name)
    if field.cpp_type != descriptor.FieldDescriptor.CPPTYPE_MESSAGE:
        out.write(': ')
    PrintFieldValue(field, value, out, indent)
    out.write('\n')


def PrintFieldValue(field, value, out, indent=0):
    """Print a single field value (not including name).  For repeated fields,
  the value should be a single element."""
    if field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_MESSAGE:
        out.write(' {\n')
        PrintMessage(value, out, indent + 2)
        out.write(' ' * indent + '}')
    elif field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_ENUM:
        out.write(field.enum_type.values_by_number[value].name)
    elif field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_STRING:
        out.write('"')
        out.write(_CEscape(value))
        out.write('"')
    elif field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_BOOL:
        if value:
            out.write('true')
        else:
            out.write('false')
    else:
        out.write(str(value))


def _CEscape(text):

    def escape(c):
        o = ord(c)
        if o == 10:
            return '\\n'
        if o == 13:
            return '\\r'
        if o == 9:
            return '\\t'
        if o == 39:
            return "\\'"
        if o == 34:
            return '\\"'
        if o == 92:
            return '\\\\'
        if o >= 127 or o < 32:
            return '\\%03o' % o
        return c

    return ('').join([ escape(c) for c in text ])