# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/easyapi/tests/test_project/models.py
# Compiled at: 2015-05-27 18:57:33
from django.db import models
from enum import Enum
from enumfields import EnumField
from rest_framework import fields as rest_fields
from easyapi.decorators import rest_method, rest_property, rest_embeddable_function, rest_embeddable_property
from easyapi.fields import PrimaryKeyReadOnlyField, RestEnumField
__author__ = 'mikhailturilin'

class CompanyType(Enum):
    PUBLIC = 1
    PRIVATE = 2


class ProjectScope(Enum):
    Client = 'Client'
    Department = 'Department'
    Company = 'Company'


class CompanyManager(models.Manager):

    @rest_method(arg_types={'country': str}, many=True)
    def select_by_country(self, country):
        return self.filter(country=country)


class Category(models.Model):
    name = models.TextField()


class Address(models.Model):
    street = models.TextField()


class Company(models.Model):
    name = models.TextField()
    category = models.ForeignKey(Category)
    country = models.CharField(max_length=100)
    company_type = EnumField(CompanyType)
    address = models.OneToOneField(Address, null=True, blank=True, related_name='company')
    objects = CompanyManager()

    @rest_method()
    def total_budget(self):
        return sum([ float(project.budget) for project in self.projects.filter(is_open=True) ])

    @rest_method(many=True)
    def project_list(self):
        return list(self.projects.filter(is_open=True))

    @rest_method(many=True)
    def project_qs(self):
        return self.projects.filter(is_open=True)

    @rest_method(rest_verbs=['POST'], arg_types={'number': int})
    def multiply_by_100(self, number):
        return number * 100

    @rest_embeddable_function(many=True)
    def projects_embedded(self):
        return self.projects.all()

    @rest_embeddable_function(name='projects_embedded_custom_function', many=True)
    def projects_embedded_custom(self):
        return self.projects.all()

    @rest_embeddable_property(many=True)
    def projects_embedded_prop(self):
        return self.projects.all()

    @rest_property(rest_fields.Field)
    def title(self):
        return self.name.title()

    @rest_property(PrimaryKeyReadOnlyField)
    def first_project(self):
        return self.projects.all().first()

    @rest_embeddable_function(data_type=RestEnumField)
    def my_company_type(self):
        return self.company_type

    @rest_property(RestEnumField)
    def first_project_scope(self):
        try:
            return self.first_project.scope
        except AttributeError:
            return

        return


class ManagerManager(models.Manager):

    @rest_method(arg_types={'a': int, 'b': int})
    def plus(self, a, b):
        return a + b

    @rest_method(arg_types={'id': int})
    def by_id(self, id):
        return self.get(id=id)


class Manager(models.Model):
    name = models.TextField()
    rest_embedded = [
     'projects']
    objects = ManagerManager()


class Project(models.Model):
    company = models.ForeignKey(Company, related_name='projects')
    name = models.TextField()
    budget = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    is_open = models.BooleanField(default=True)
    start_date = models.DateField()
    manager = models.ForeignKey(Manager, related_name='projects')
    scope = EnumField(ProjectScope)
    extra_rest_fields = {'company_name': rest_fields.Field(source='company.name')}