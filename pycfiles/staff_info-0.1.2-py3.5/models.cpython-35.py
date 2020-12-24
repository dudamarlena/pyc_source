# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staff_info/models.py
# Compiled at: 2018-05-23 08:30:30
# Size of source mod 2**32: 9168 bytes
"""
Created on Sun Mar 19 12:40:12 2017

@author: IukhymchukS
"""
from collections import OrderedDict
from datetime import datetime
from staff_info.settings import connector

class Manager:

    def __init__(self):
        self.connector = connector

    def _create_objects(self, model, **kwargs):
        """
        Base method for object creation. It
        """
        pass

    def create_object(self, model, **kwargs):
        return self._create_objects(model, **kwargs)

    def create_related_object(self, obj, related_model, **kwargs):
        fk = obj.primary_key[0]
        kwargs[fk] = obj[fk]
        related_obj = related_model(**kwargs)
        self._create_objects(related_model, **related_obj.__dict__)

    def select_object(self, model, **conditions):
        pass

    def get_all(self, model):
        sql = 'SELECT * FROM {};'.format(model.table_name)
        result = connector.execute_sql(sql, change=False)
        for item in result:
            e_dict = {}
            for k, v in zip(model.fields, item):
                e_dict[k] = v

            model(**e_dict)

        return model.objects

    def select_related_object(self, model, related_model, **conditions):
        pass

    def get_related_last(self, obj, related_model):
        pk = obj.primary_key[0]
        related_table = related_model.table_name
        select_row = 'SELECT * FROM {}'.format(related_model.table_name)
        where_condition = ' WHERE {}={} and id in '.format(pk, obj[pk])
        inner_select = '(SELECT MAX(id) FROM {} GROUP BY {})'.format(related_table, pk)
        sql = select_row + where_condition + inner_select
        result = connector.execute_sql(sql, change=False)
        return result


class Employee:
    table_name = 'employee'
    fields = ['idEmp', 'fullname', 'dateOfEmp', 'dob']
    primary_key = ('idEmp', {'auto_increment': True})
    labels = OrderedDict({'idEmp': ('Id', 3), 'fullname': ('Full Name', 30), 
     'dateOfEmp': ('Employment Date', 20), 'dob': ('Birthday', 10)})
    objects = []

    def __init__(self, **kwargs):
        """
        Object initialization according main table (with primary key)
        """
        for item in self.fields:
            self.__dict__[item] = kwargs.get(item, None)

        Employee.objects.append(self)

    def __str__(self):
        return self.fullname

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def update_parameters(self, **kwargs):
        self.__dict__.update(**kwargs)

    @classmethod
    def get_related_models(cls, *models):
        """
        Return list of related model for this one
        """
        related_models = []
        for model in models:
            try:
                for fk in model.foreign_keys:
                    if cls.primary_key[0] == fk:
                        related_models.append(model)

            except AttributeError:
                pass

        return related_models


class AttributeTable:

    def __init__(self, **kwargs):
        for item in self.fields:
            self[item] = kwargs.get(item, None)

        self.date_of_change = datetime.today().strftime('%Y-%m-%d')
        self.description = 'Information at date of employment'

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def update_parameters(self, **kwargs):
        self.__dict__.update(kwargs)


class Position(AttributeTable):
    table_name = 'position'
    fields = ['idEmp', 'prev_pos', 'date_of_change', 'current_pos', 'id']
    primary_key = ('id', {'auto_increment': True})
    foreign_keys = ['idEmp']
    parent_model = Employee
    labels = OrderedDict({'prev_pos': ('Previous position', 15), 'current_pos': ('Position', 15), 
     'date_of_change': ('Date of change', 15)})


class Timeoff(AttributeTable):
    table_name = 'timeoff'
    fields = ['idEmp', 'date_of_change', 'status', 'description', 'timeoff_available', 'id']
    primary_key = ('id', {'auto_increment': True})
    foreign_keys = ['idEmp']
    parent_model = Employee
    labels = OrderedDict({'date_of_change': ('Date of change', 15), 'status': ('Operation', 15), 
     'description': ('Description', 20), 'timeoff_available': ('Timeoff', 10)})


class InformalVacation(AttributeTable):
    table_name = 'informal_vacation'
    fields = ['idEmp', 'date_of_change', 'description', 'informal_vacation_available', 'id']
    primary_key = ('id', {'auto_increment': True})
    foreign_keys = ['idEmp']
    parent_model = Employee
    labels = OrderedDict({'date_of_change': ('Date of change', 15), 'description': ('Description', 20), 
     'informal_vacation_available': ('Informal Vacation', 10)})


class Vacation(AttributeTable):
    table_name = 'vacation'
    fields = ['idEmp', 'date_of_change', 'description', 'vacation_available', 'id']
    primary_key = ('id', {'auto_increment': True})
    foreign_keys = ['idEmp']
    parent_model = Employee
    labels = OrderedDict({'date_of_change': ('Date of change', 15), 
     'description': ('Description', 20), 
     'vacation_available': ('Vacation', 10)})


class Salary(AttributeTable):
    table_name = 'salary'
    fields = ['idEmp', 'previous', 'date_of_change', 'current', 'id']
    primary_key = ('id', {'auto_increment': True})
    foreign_keys = ['idEmp']
    parent_model = Employee
    labels = OrderedDict({'previous': ('Previous salary', 15), 
     'date_of_change': ('Date of change', 15), 
     'current': ('Current salary', 15)})


class Commission(AttributeTable):
    table_name = 'commission'
    fields = ['idEmp', 'comm_percent', 'date_of_change', 'year', 'id']
    primary_key = ('id', {'auto_increment': True})
    foreign_keys = ['idEmp', 'year']
    labels = OrderedDict({'comm_percent': ('Commission percent', 15), 
     'date_of_change': ('Date of change', 15), 
     'year': ('Year', 10)})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.year = datetime.now().year


class Result:
    table_name = 'result'
    fields = ['year', 'fact_revenue', 'fact_margin', 'plan_revenue', 'plan_margin']
    primary_key = ('year', {'auto_increment': False})
    foreign_key = []
    labels = OrderedDict({'year': ('Year', 10), 'fact_revenue': ('Actual Revenue', 15), 
     'fact_margin': ('Actual Margin', 15), 
     'plan_revenue': ('Planning Revenue', 15), 
     'plan_margin': ('Planning Margin', 15)})


model_list = [
 Employee, Position, Timeoff, InformalVacation, Vacation, Salary, Commission, Result]
if __name__ == '__main__':
    pass