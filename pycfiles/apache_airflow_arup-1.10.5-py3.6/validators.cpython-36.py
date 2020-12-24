# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/www_rbac/validators.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 2109 bytes
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError

class GreaterEqualThan(EqualTo):
    __doc__ = 'Compares the values of two fields.\n\n    :param fieldname:\n        The name of the other field to compare to.\n    :param message:\n        Error message to raise in case of a validation error. Can be\n        interpolated with `%(other_label)s` and `%(other_name)s` to provide a\n        more helpful error.\n    '

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'." % self.fieldname))

        if field.data is None or other.data is None:
            return
        if field.data < other.data:
            d = {'other_label':hasattr(other, 'label') and other.label.text or self.fieldname, 
             'other_name':self.fieldname}
            message = self.message
            if message is None:
                message = field.gettext('Field must be greater than or equal to %(other_label)s.' % d)
            else:
                message = message % d
            raise ValidationError(message)