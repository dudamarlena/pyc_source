# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/Sandbox/huru-server/.venv/lib/python2.7/site-packages/data_importer/importers/base.py
# Compiled at: 2020-04-17 10:46:24
from __future__ import unicode_literals
import os, sys, re, io, six, codecs
from django.db import transaction
from django.db.models.fields import FieldDoesNotExist
from django.core.exceptions import ValidationError
from data_importer.core.descriptor import ReadDescriptor
from data_importer.core.exceptions import StopImporter
from data_importer.core.base import objclass2dict
from data_importer.core.base import DATA_IMPORTER_EXCEL_DECODER
from data_importer.core.base import DATA_IMPORTER_DECODER
from data_importer.core.base import convert_alphabet_to_number
from data_importer.core.base import reduce_list
from collections import OrderedDict
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

class BaseImporter(object):
    """
    Base Importer method to create simples importes CSV files.

    set_reader: can be override to create new importers files
    """

    def __new__(cls, **kargs):
        """
        Provide custom methods in subclass Meta
        """
        if hasattr(cls, b'Meta'):
            cls.Meta = objclass2dict(cls.Meta)
        return super(BaseImporter, cls).__new__(cls)

    def __init__(self, source=None, *args, **kwargs):
        self.file_history = None
        self._error = []
        self._fields = []
        self._cleaned_data = ()
        self._reader = None
        self._excluded = False
        self._readed = False
        self._reduce_list = []
        self.start_fields()
        if source:
            self.source = source
            self.set_reader()
        return

    class Meta:
        """Importer configurations"""
        pass

    @staticmethod
    def to_unicode(bytestr):
        """
        Receive string bytestr and try to return a utf-8 string.
        """
        if not isinstance(bytestr, str):
            return bytestr
        try:
            decoded = bytestr.decode(DATA_IMPORTER_EXCEL_DECODER)
        except (UnicodeEncodeError, AttributeError):
            decoded = force_text(bytestr, DATA_IMPORTER_DECODER)

        return decoded

    @property
    def source(self):
        """Return source opened"""
        return self._source

    @source.setter
    def source(self, source=None, encoding=b'cp1252'):
        """Open source to reader"""
        if isinstance(source, io.IOBase):
            self._source = source
        elif isinstance(source, six.string_types) and os.path.exists(source) and source.endswith(b'csv'):
            if sys.version_info >= (3, 0):
                self._source = codecs.open(source, b'rb', encoding=encoding)
            else:
                self._source = codecs.open(source, b'rb')
        elif isinstance(source, list):
            self._source = source
        elif hasattr(source, b'file_upload'):
            self._source = source.file_upload
            self.file_history = source
        elif hasattr(source, b'file'):
            self._source = io.open(source.file.name, b'rb')
        else:
            self._source = source

    @property
    def meta(self):
        """Is same to use .Meta"""
        if hasattr(self, b'Meta'):
            return self.Meta

    def start_fields(self):
        """
        Initial function to find fields or headers values
        This values will be used to process clean and save method
        If this method not have fields and have Meta.model this method
        will use model fields to populate content without id
        """
        if self.Meta.model and not hasattr(self, b'fields'):
            all_models_fields = [ i.name for i in self.Meta.model._meta.fields if i.name != b'id' ]
            self.fields = all_models_fields
        self.exclude_fields()
        if self.Meta.descriptor:
            self.load_descriptor()

    def exclude_fields(self):
        """
        Exclude fields from Meta.exclude
        """
        if hasattr(self, b'fields') and isinstance(self.fields, dict):
            order_dict = OrderedDict(self.fields)
            self.fields = list(self.fields)
            self._reduce_list = list(map(convert_alphabet_to_number, order_dict.values()))
        if self.Meta.exclude and not self._excluded:
            self._excluded = True
            for exclude in self.Meta.exclude:
                if exclude in self.fields:
                    self.fields = list(self.fields)
                    self.fields.remove(exclude)

    def load_descriptor(self):
        """
        Set fields from descriptor file
        """
        descriptor = ReadDescriptor(self.Meta.descriptor, self.Meta.descriptor_model)
        self.fields = descriptor.get_fields()
        self.exclude_fields()

    @property
    def errors(self):
        """
        Show errors catch by clean methods
        """
        return self._error

    def is_valid(self):
        """
        Clear content and return False if have errors
        """
        if not self.cleaned_data:
            self.cleaned_data
        return not any(self._error)

    def set_reader(self):
        """
        Method responsable to convert file content into a list with same values that
        have fields

            fields: ['myfield1', 'myfield2']

            response: [['value_myfield1', 'value_myfield2'],
                        ['value2_myfield1', 'value2_myfield2']]
        """
        raise NotImplementedError(b'No reader implemented')

    def clean_field(self, field_name, value):
        """
        User default django field validators to clean content
        and run custom validates
        """
        if self.Meta.model:
            try:
                field = self.Meta.model._meta.get_field(field_name)
                field.clean(value, field)
            except FieldDoesNotExist:
                pass
            except Exception as msg:
                default_msg = msg.messages[0].replace(b'This field', b'')
                new_msg = (b'Field ({0!s}) {1!s}').format(field.name, default_msg)
                raise ValidationError(new_msg)

        clean_function = getattr(self, (b'clean_{0!s}').format(field_name), False)
        if clean_function:
            try:
                return clean_function(value)
            except Exception as msg:
                default_msg = str(msg).replace(b'This field', b'')
                new_msg = (b'Field ({0!s}) {1!s}').format(field_name, default_msg)
                raise ValidationError(new_msg)

        return value

    def process_row(self, row, values):
        """
        Read clean functions from importer and return tupla with row number, field and value
        """
        values_encoded = [ self.to_unicode(i) for i in values ]
        try:
            if self._reduce_list:
                values_encoded = reduce_list(self._reduce_list, values_encoded)
            values = dict(zip(self.fields, values_encoded))
        except TypeError:
            raise TypeError((b'Invalid Line: {0!s}').format(row))

        has_error = False
        if self.Meta.ignore_empty_lines:
            if not any(values.values()):
                return
        for k, v in values.items():
            if self.Meta.raise_errors:
                values[k] = self.clean_field(k, v)
            else:
                try:
                    values[k] = self.clean_field(k, v)
                except StopImporter as e:
                    raise StopImporter(self.get_error_message(e, row))
                except Exception as e:
                    self._error.append(self.get_error_message(e, row))
                    has_error = True

        if has_error:
            return
        else:
            try:
                clean_row_values = self.clean_row(values)
                if clean_row_values is not None:
                    values = clean_row_values
            except Exception as e:
                self._error.append(self.get_error_message(e, row))
                return

            return (row, values)

    def get_error_message(self, error, row=None, error_type=None):
        messages = b''
        if not error_type:
            error_type = (b'{0!s}').format(type(error).__name__)
        if hasattr(error, b'message') and error.message:
            messages = (b'{0!s}').format(error.message)
        if hasattr(error, b'messages') and not messages:
            if error.messages:
                messages = (b',').join(error.messages)
        messages = re.sub(b"'", b'', messages)
        messages = re.sub(b'"', b'', messages)
        error_type = re.sub(b"'", b'', error_type)
        error_type = re.sub(b'"', b'', error_type)
        if row:
            return (row, error_type, messages)
        else:
            return (
             error_type, messages)

    @property
    def cleaned_data(self):
        """
        Return tupla with data cleaned
        """
        if self._readed:
            return self._cleaned_data
        self._readed = True
        try:
            self.pre_clean()
        except Exception as e:
            self._error.append(self.get_error_message(e, error_type=b'__pre_clean__'))

        try:
            self.clean()
        except Exception as e:
            self._error.append(self.get_error_message(e, error_type=b'__clean_all__'))

        for data in self._read_file():
            if data:
                self._cleaned_data += (data,)

        try:
            self.post_clean()
        except Exception as e:
            self._error.append(self.get_error_message(e, error_type=b'__post_clean__'))

        return self._cleaned_data

    def pre_clean(self):
        """
        Executed before all clean methods
        Important: pre_clean dont have cleaned_data content
        """
        pass

    def post_clean(self):
        """
        Excuted after all clean method
        """
        pass

    def clean(self):
        """
        Custom clean method
        """
        pass

    def clean_row(self, row_values):
        """
        Custom clean method for full row data
        """
        return row_values

    def pre_commit(self):
        """
        Executed before commit multiple register
        """
        pass

    def post_save_all_lines(self):
        """
        End exection
        """
        pass

    def _read_file(self):
        """
        Create cleaned_data content
        """
        if hasattr(self._reader, b'read'):
            reader = self._reader.read()
        else:
            reader = self._reader
        for row, values in enumerate(reader, 1):
            if self.Meta.ignore_first_line:
                row -= 1
            if self.Meta.starting_row and row < self.Meta.starting_row:
                pass
            elif row < 1:
                pass
            else:
                yield self.process_row(row, values)

    def save(self, instance=None):
        """
        Save all contents
        DONT override this method
        """
        if not instance:
            instance = self.Meta.model
        if not instance:
            raise AttributeError(b'Invalid instance model')
        if self.Meta.transaction:
            with transaction.atomic():
                for row, data in self.cleaned_data:
                    record = instance(**data)
                    record.save()

                try:
                    self.pre_commit()
                except Exception as e:
                    self._error.append(self.get_error_message(e, error_type=b'__pre_commit__'))
                    transaction.rollback()

                try:
                    transaction.commit()
                except Exception as e:
                    self._error.append(self.get_error_message(e, error_type=b'__trasaction__'))
                    transaction.rollback()

        else:
            for row, data in self.cleaned_data:
                record = instance(**data)
                record.save(force_update=False)

        self.post_save_all_lines()
        return True