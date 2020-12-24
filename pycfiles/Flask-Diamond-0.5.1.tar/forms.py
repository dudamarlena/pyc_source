# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idm/Work/flask-diamond/flask_diamond/facets/forms.py
# Compiled at: 2016-11-18 16:26:44
from wtforms.fields import HiddenField, BooleanField

def init_forms(self):
    """
    WTForms helpers

    :returns: None

    `WTForms <http://wtforms.simplecodes.com/docs/>`_ is a great library
    for using forms and `Flask-WTF <https://flask-
    wtf.readthedocs.org/en/latest/>`_ provides good integration with it.
    WTForms helpers enable you to add custom filters and other custom
    behaviours.
    """
    add_helpers(self.app)


def add_helpers(app):
    """
    Create any Jinja2 helpers needed.
    """

    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)

    def is_boolean_field_filter(field):
        return isinstance(field, BooleanField)

    app.jinja_env.filters['is_hidden_field'] = is_hidden_field_filter
    app.jinja_env.filters['is_boolean_field'] = is_boolean_field_filter