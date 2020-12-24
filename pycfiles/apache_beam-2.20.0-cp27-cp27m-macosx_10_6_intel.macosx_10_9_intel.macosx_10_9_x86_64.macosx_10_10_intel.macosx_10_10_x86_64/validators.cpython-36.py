# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/www_rbac/validators.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 2109 bytes
from wtforms.validators import EqualTo
from wtforms.validators import ValidationError

class GreaterEqualThan(EqualTo):
    """GreaterEqualThan"""

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