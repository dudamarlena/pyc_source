# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/easyapi/tests/test_project/api.py
# Compiled at: 2014-07-19 21:55:57
from easyapi.router import EasyApiRouter, AutoAppRouter, AutoAppListRouter
from easyapi.tests.test_project.models import Company, Project
from easyapi.viewsets import InstanceViewSet
__author__ = 'mikhailturilin'

class CompanyViewSet(InstanceViewSet):
    model = Company


class ProjectViewSet(InstanceViewSet):
    model = Project


router = EasyApiRouter()
router.register('company', CompanyViewSet)
router.register('project', ProjectViewSet)