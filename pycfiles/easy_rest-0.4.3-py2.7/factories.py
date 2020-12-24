# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/easyapi/tests/factories.py
# Compiled at: 2014-08-29 20:42:38
from easyapi.tests.test_project.models import Project, Company, Category, CompanyType, ProjectScope, Address, Manager
from datetime import timedelta, date
from django.utils import timezone
import factory
from factory import django as factory_django
from factory import fuzzy
__author__ = 'mikhailturilin'

class CategoryFactory(factory_django.DjangoModelFactory):

    class Meta:
        model = Category

    name = fuzzy.FuzzyText()


class AddressFactory(factory_django.DjangoModelFactory):

    class Meta:
        model = Address

    street = fuzzy.FuzzyText()


class CompanyFactory(factory_django.DjangoModelFactory):

    class Meta:
        model = Company

    category = factory.SubFactory(CategoryFactory)
    name = fuzzy.FuzzyText()
    country = fuzzy.FuzzyText(length=20)
    company_type = fuzzy.FuzzyChoice(CompanyType)
    address = None


SIX_MONTH_EARLIER = date.today() - timedelta(days=int(183.0))

class ManagerFactory(factory_django.DjangoModelFactory):

    class Meta:
        model = Manager

    name = fuzzy.FuzzyText()


class ProjectFactory(factory_django.DjangoModelFactory):

    class Meta:
        model = Project

    company = factory.SubFactory(CompanyFactory)
    name = fuzzy.FuzzyText()
    budget = fuzzy.FuzzyInteger(1000, 9000)
    start_date = fuzzy.FuzzyDate(start_date=SIX_MONTH_EARLIER)
    scope = fuzzy.FuzzyChoice(ProjectScope)
    manager = factory.SubFactory(ManagerFactory)