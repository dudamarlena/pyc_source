# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Brian/Work/github_projects/marvin_pypi/python/marvin/extern/wtforms-alchemy/wtforms_alchemy/validators.py
# Compiled at: 2018-01-12 14:08:15
# Size of source mod 2**32: 3313 bytes
from collections import Iterable, Mapping
import six
from sqlalchemy import Column
from sqlalchemy.orm.attributes import InstrumentedAttribute
from wtforms import ValidationError

class Unique(object):
    __doc__ = "Checks field values unicity against specified table fields.\n\n    :param column:\n        InstrumentedAttribute object, eg. User.name, or\n        Column object, eg. user.c.name, or\n        a field name, eg. 'name' or\n        a tuple of InstrumentedAttributes, eg. (User.name, User.email) or\n        a dictionary mapping field names to InstrumentedAttributes, eg.\n        {\n            'name': User.name,\n            'email': User.email\n        }\n    :param get_session:\n        A function that returns a SQAlchemy Session. This parameter is not\n        needed if the given model supports Flask-SQLAlchemy styled query\n        parameter.\n    :param message:\n        The error message.\n    "
    field_flags = ('unique', )

    def __init__(self, column, get_session=None, message=None):
        self.column = column
        self.message = message
        self.get_session = get_session

    @property
    def query(self):
        self._check_for_session(self.model)
        if self.get_session:
            return self.get_session().query(self.model)
        if hasattr(self.model, 'query'):
            return getattr(self.model, 'query')
        raise Exception('Validator requires either get_session or Flask-SQLAlchemy styled query parameter')

    def _check_for_session(self, model):
        if not hasattr(model, 'query'):
            if not self.get_session:
                raise Exception('Could not obtain SQLAlchemy session.')

    def _syntaxes_as_tuples(self, form, field, column):
        """Converts a set of different syntaxes into a tuple of tuples"""
        if isinstance(column, six.string_types):
            return (
             (
              column, getattr(form.Meta.model, column)),)
        else:
            if isinstance(column, Mapping):
                return tuple((x[0], self._syntaxes_as_tuples(form, field, x[1])[0][1]) for x in column.items())
            if isinstance(column, Iterable):
                return tuple(self._syntaxes_as_tuples(form, field, x)[0] for x in column)
            if isinstance(column, (Column, InstrumentedAttribute)):
                return (
                 (
                  column.key, column),)
        raise TypeError('Invalid syntax for column')

    def __call__(self, form, field):
        columns = self._syntaxes_as_tuples(form, field, self.column)
        self.model = columns[0][1].class_
        query = self.query
        for field_name, column in columns:
            query = query.filter(column == form[field_name].data)

        obj = query.first()
        if not hasattr(form, '_obj'):
            raise Exception("Couldn't access Form._obj attribute. Either make your form inherit WTForms-Alchemy ModelForm or WTForms-Components ModelForm or make this attribute available in your form.")
        else:
            if obj:
                if not form._obj == obj:
                    if self.message is None:
                        self.message = field.gettext('Already exists.')
                    raise ValidationError(self.message)