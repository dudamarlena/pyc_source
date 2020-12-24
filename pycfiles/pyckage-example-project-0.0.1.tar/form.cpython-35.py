# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /MyWork/Projects/PyCK/pyck/forms/form.py
# Compiled at: 2015-02-06 10:57:09
# Size of source mod 2**32: 4647 bytes
import sys, wtforms
from mako.template import Template
from .template_lookup import template_lookup
PY3 = sys.version > '3'

class Form(wtforms.Form):
    """Form"""

    def __init__(self, formdata=None, obj=None, prefix='', request_obj=None, use_csrf_protection=False, **kwargs):
        super(Form, self).__init__(formdata, obj, prefix, **kwargs)
        self._use_csrf_protection = use_csrf_protection
        if use_csrf_protection:
            if request_obj is None:
                raise Exception('Cannot use CSRF protection without a request object being passed to the form')
        else:
            self._request = request_obj
            self._csrf_token = self._request.session.get_csrf_token()

    def validate(self):
        """
        Validate form fields and check for CSRF token match if use_csrf_protection was set to true when
        initializing the form.
        """
        validate_result = super(Form, self).validate()
        if validate_result and self._use_csrf_protection and self._csrf_token != self._request.params['csrf_token']:
            self.errors['_csrf'] = [
             'CSRF token did not match']
            return False
        return validate_result

    def as_p(self, labels='top', errors='right'):
        """
        Output each form field as html **p** tags. By default labels are displayed on top of the form fields
        and validation erros are displayed on the right of the form fields. Both these behaviors can be
        changed by settings values for the labels and errors parameters.

        Values can be left, top, right or bottom

        :param labels:
            Placement of labels relative to the field
        :param errors:
            Placement of validation errors (if any) relative to the field

        """
        tmpl = template_lookup.get_template('form_as_p.mako')
        output = tmpl.render(form=self, labels_position=labels.lower(), errors_position=errors.lower())
        if PY3:
            output = output.decode('utf-8')
        return output

    def as_table(self, labels='left', errors='top', include_table_tag=False):
        """
        Output the form as HTML Table, optionally add the table tags too if include_table_tag is set to True (default False)

        :param labels:
            Placement of labels relative to the field
        :param errors:
            Placement of validation errors (if any) relative to the field
        :param include_table_tag:
            Whether to include the html <table> and </table> tags in the output or not

        """
        tmpl = template_lookup.get_template('form_as_table.mako')
        output = tmpl.render(form=self, labels_position=labels.lower(), errors_position=errors.lower(), include_table_tag=include_table_tag)
        if PY3:
            output = output.decode('utf-8')
        return output

    def as_div(self):
        """
        Output each form field as html **p** tags. By default labels are displayed on top of the form fields
        and validation erros are displayed on the right of the form fields. Both these behaviors can be
        changed by settings values for the labels and errors parameters.

        Values can be left, top, right or bottom

        :param labels:
            Placement of labels relative to the field
        :param errors:
            Placement of validation errors (if any) relative to the field

        """
        tmpl = template_lookup.get_template('form_as_div.mako')
        output = tmpl.render(form=self)
        if PY3:
            output = output.decode('utf-8')
        return output