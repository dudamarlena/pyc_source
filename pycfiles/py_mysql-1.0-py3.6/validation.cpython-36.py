# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_mysql\lib\mysql\connector\django\validation.py
# Compiled at: 2017-12-07 02:34:36
# Size of source mod 2**32: 2605 bytes
import django
if django.VERSION >= (1, 8):
    from django.db.backends.base.validation import BaseDatabaseValidation
else:
    from django.db.backends import BaseDatabaseValidation
if django.VERSION < (1, 7):
    from django.db import models
else:
    from django.core import checks
    from django.db import connection

class DatabaseValidation(BaseDatabaseValidation):
    if django.VERSION < (1, 7):

        def validate_field(self, errors, opts, f):
            """
            MySQL has the following field length restriction:
            No character (varchar) fields can have a length exceeding 255
            characters if they have a unique index on them.
            """
            varchar_fields = (
             models.CharField,
             models.CommaSeparatedIntegerField,
             models.SlugField)
            if isinstance(f, varchar_fields):
                if f.max_length > 255:
                    if f.unique:
                        msg = '"%(name)s": %(cls)s cannot have a "max_length" greater than 255 when using "unique=True".'
                        errors.add(opts, msg % {'name':f.name,  'cls':f.__class__.__name__})

    else:

        def check_field(self, field, **kwargs):
            errors = (super(DatabaseValidation, self).check_field)(field, **kwargs)
            if getattr(field, 'rel', None) is None:
                field_type = field.db_type(connection)
                if field_type is None:
                    return errors
                if field_type.startswith('varchar'):
                    if field.unique:
                        if field.max_length is None or int(field.max_length) > 255:
                            errors.append(checks.Error('MySQL does not allow unique CharFields to have a max_length > 255.',
                              hint=None,
                              obj=field,
                              id='mysql.E001'))
            return errors