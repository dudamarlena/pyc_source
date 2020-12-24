# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/userfield.py
# Compiled at: 2020-01-18 11:47:38
"""Class to show and manipulate user fields in odf documents."""
import sys, zipfile
from odf.text import UserFieldDecl
from odf.namespaces import OFFICENS
from odf.opendocument import load
import io, sys
if sys.version_info[0] == 3:
    unicode = str
OUTENCODING = 'utf-8'
VALUE_TYPES = {'float': (
           OFFICENS, 'value'), 
   'percentage': (
                OFFICENS, 'value'), 
   'currency': (
              OFFICENS, 'value'), 
   'date': (
          OFFICENS, 'date-value'), 
   'time': (
          OFFICENS, 'time-value'), 
   'boolean': (
             OFFICENS, 'boolean-value'), 
   'string': (
            OFFICENS, 'string-value')}

class UserFields(object):
    """List, view and manipulate user fields."""
    src_file = None
    dest_file = None

    def __init__(self, src=None, dest=None):
        """Constructor

        @param src open file in binary mode: source document,
        or filename as a unicode string, or None for stdin.
        @param dest opendile in binary mode: destination document,
        or filename as a unicode string, or None for stdout.
        """
        assert src == None or 'rb' in repr(src) or 'BufferedReader' in repr(src) or 'BytesIO' in repr(src) or type(src) == type('')
        assert dest == None or 'wb' in repr(dest) or 'BufferedWriter' in repr(dest) or 'BytesIO' in repr(dest) or type(dest) == type('')
        self.src_file = src
        self.dest_file = dest
        self.document = None
        return

    def loaddoc(self):
        if sys.version_info[0] == 3 and (isinstance(self.src_file, str) or isinstance(self.src_file, io.IOBase)) or sys.version_info[0] == 2 and isinstance(self.src_file, basestring):
            if not zipfile.is_zipfile(self.src_file):
                raise TypeError('%s is no odt file.' % self.src_file)
        elif self.src_file is None:
            self.src_file = sys.stdin
        self.document = load(self.src_file)
        return

    def savedoc(self):
        if self.dest_file is None:
            self.document.save('-')
        else:
            self.document.save(self.dest_file)
        return

    def list_fields(self):
        """List (extract) all known user-fields.

        @return list of user-field names as unicode strings.
        """
        return [ x[0] for x in self.list_fields_and_values() ]

    def list_fields_and_values(self, field_names=None):
        """List (extract) user-fields with type and value.

        @param field_names list of field names as unicode strings
        to show, or None for all.

        @return list of tuples (<field name>, <field type>, <value>)
        as type (unicode string, stringified type, unicode string).

        """
        self.loaddoc()
        found_fields = []
        all_fields = self.document.getElementsByType(UserFieldDecl)
        for f in all_fields:
            value_type = f.getAttribute('valuetype')
            if value_type == 'string':
                value = f.getAttribute('stringvalue')
            else:
                value = f.getAttribute('value')
            field_name = f.getAttribute('name')
            if field_names is None or field_name in field_names:
                found_fields.append((field_name,
                 value_type,
                 value))

        return found_fields

    def list_values(self, field_names):
        """Extract the contents of given field names from the file.

        @param field_names list of field names as unicode strings

        @return list of field values as unicode strings.

        """
        return [ x[2] for x in self.list_fields_and_values(field_names) ]

    def get(self, field_name):
        """Extract the contents of this field from the file.
        @param field_name unicode string: name of a field
        @return field value as a unicode string or None if field does not exist.

        """
        if not type(field_name) == type(''):
            raise AssertionError
            values = self.list_values([field_name])
            return values or None
        else:
            return values[0]

    def get_type_and_value(self, field_name):
        """Extract the type and contents of this field from the file.
        @param field_name unicode string: name of a field
        @return tuple (<type>, <field-value>) as a pair of unicode strings
        or None if field does not exist.

        """
        if not type(field_name) == type(''):
            raise AssertionError
            fields = self.list_fields_and_values([field_name])
            return fields or None
        else:
            field_name, value_type, value = fields[0]
            return (value_type, value)

    def update(self, data):
        """Set the value of user fields. The field types will be the same.

        data ... dict, with field name as key, field value as value

        Returns None

        """
        self.loaddoc()
        all_fields = self.document.getElementsByType(UserFieldDecl)
        for f in all_fields:
            field_name = f.getAttribute('name')
            if field_name in data:
                value_type = f.getAttribute('valuetype')
                value = data.get(field_name)
                if value_type == 'string':
                    f.setAttribute('stringvalue', value)
                else:
                    f.setAttribute('value', value)

        self.savedoc()