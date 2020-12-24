# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/djutils/forms.py
# Compiled at: 2016-08-27 09:24:56


def transform_form_error(form, verbose=True):
    """
        transform form errors to list like
        ["field1: error1", "field2: error2"]
    """
    errors = []
    for field, err_msg in form.errors.items():
        if field == '__all__':
            errors.append((', ').join(err_msg))
        else:
            field_name = field
            if verbose and field in form.fields:
                field_name = form.fields[field].label or field
            errors.append('%s: %s' % (field_name, (', ').join(err_msg)))

    return errors