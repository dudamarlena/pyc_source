# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flask_ponymanager/former.py
# Compiled at: 2020-02-25 09:39:56
# Size of source mod 2**32: 7199 bytes
import datetime
from wtforms import Form
from typing import Type, List
from pony.orm import db_session
from pony.orm.core import Entity, Attribute
from wtforms import SubmitField, StringField, IntegerField, FloatField, BooleanField, HiddenField, SelectField, SelectMultipleField
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms.validators import DataRequired
EntityList = List[Entity]
type_mapping = {str: StringField, 
 int: IntegerField, 
 float: FloatField, 
 bool: BooleanField, 
 datetime.date: DateField, 
 datetime.datetime: DateTimeField, 
 Entity: SelectField, 
 EntityList: SelectMultipleField, 
 'primary_key': HiddenField, 
 'default': StringField}
unsupported_types = list()
date_format = '%d. %m. %Y'
datetime_format = date_format + ' %H:%M:%S'

class EntityForm(Form):
    with_primary_keys: bool = None


class EntityFormer:

    def __init__(self, entity: Type[Entity]):
        self.entity = entity
        self.date_format = date_format
        self.datetime_format = datetime_format

    def columns(self) -> dict:
        """
        Get entity columns.
        """
        columns = dict()
        for key, value in self.entity.__dict__.items():
            if key is not '_pk_' and issubclass(type(value), Attribute):
                columns[key] = value

        return columns

    def primary_keys(self) -> List[str]:
        """
        List of names of primary keys.
        """
        return [key for key, value in self.columns().items() if value.is_pk]

    def primary_key(self) -> str:
        """
        First primary key.
        """
        try:
            return self.primary_keys()[0]
        except IndexError:
            raise Exception('Entity must have some primary key to be managed with PonyManager.')

    def get_form(self, add_primary_keys: bool=True, add_submit: bool=True) -> Type[EntityForm]:
        """
        Generate form for entity.
        """

        class GeneratedEntityForm(EntityForm):
            with_primary_keys = add_primary_keys

        for name, column in self.columns().items():
            if column.py_type in unsupported_types:
                pass
            else:
                field_kwargs = dict(label=name,
                  validators=(list()))
                if column.is_required:
                    if column.py_type not in [bool, EntityList]:
                        field_kwargs['validators'].append(DataRequired())
                    else:
                        if column.is_pk:
                            if add_primary_keys:
                                form_input_class = type_mapping['primary_key']
                            else:
                                continue
                        else:
                            if column.is_relation:
                                form_input_class = type_mapping[EntityList] if column.is_collection else type_mapping[Entity]
                            else:
                                form_input_class = type_mapping[column.py_type] if column.py_type in type_mapping.keys() else type_mapping['default']
                    if column.is_relation:
                        with db_session:
                            field_kwargs['choices'] = [(str(getattr(entity, self.primary_key())), str(entity)) for entity in column.py_type.select()]
                    else:
                        if column.py_type is datetime.date:
                            field_kwargs['format'] = self.date_format
                        else:
                            if column.py_type is datetime.datetime:
                                field_kwargs['format'] = self.datetime_format
                        setattr(GeneratedEntityForm, name, form_input_class(**field_kwargs))

        if add_submit:
            setattr(GeneratedEntityForm, 'submit', SubmitField('Submit'))
        return GeneratedEntityForm

    def fill_form(self, entity_form: Type[EntityForm], entity_row: Entity) -> EntityForm:
        """
        Fill entity form with values from entity.
        """
        form_values = dict()
        for name, column in self.columns().items():
            if not entity_form.with_primary_keys and column.is_pk:
                continue
            else:
                if column.is_relation:
                    form_values[name] = [str(getattr(row, self.primary_key())) for row in column.py_type.select()]
                else:
                    form_values[name] = getattr(entity_row, name)

        return entity_form(**form_values)

    def get_form_values(self, form: EntityForm) -> dict:
        """
        Process data from (posted) form.
        """
        form_values = dict()
        for name, column in self.columns().items():
            if not form.with_primary_keys:
                if column.is_pk:
                    continue
            try:
                data = getattr(form, name).data
                if column.is_relation:
                    if column.is_collection:
                        selected = [self.columns()[self.primary_key()].py_type(value) for value in data or list()]
                        data = [(column.py_type.get)(**{self.primary_key(): key}) for key in selected]
                    else:
                        selected = self.columns()[self.primary_key()].py_type(data)
                        data = (column.py_type.get)(**{self.primary_key(): selected})
                else:
                    if column.py_type is datetime.date:
                        if data:
                            data = datetime.datetime.strptime(data, self.date_format)
                if column.py_type is datetime.datetime:
                    if data:
                        data = datetime.datetime.strptime(data, self.datetime_format)
                if column.py_type in [datetime.date, datetime.datetime]:
                    if not data:
                        data = None
                form_values[name] = data
            except KeyError:
                pass

        return form_values

    def update_entity_from_form(self, form: EntityForm) -> Entity:
        """
        Update database row with form values.
        """
        form_values = self.get_form_values(form)
        select_by = {key:form_values.pop(key) for key in self.primary_keys()}
        with db_session:
            row = (self.entity.get)(**select_by)
            for key, value in form_values.items():
                setattr(row, key, value)

        return row

    def add_entity_from_form(self, form: EntityForm) -> Entity:
        """
        Add database row with from values.
        """
        return (self.entity)(**self.get_form_values(form))