# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hasher/apps/workflow/workflowapp/tests.py
# Compiled at: 2016-03-07 02:16:09
from django.contrib.auth.models import User
from django.http import request
from django.test import TestCase
from django.contrib.auth import authenticate, login
from workflowapp.createflow import create_workflow, add_states, add_connection, create_task

class test_recommender_algorithm(TestCase):
    """
        Testing various functions in recommender
    """

    def setUp(self):
        pass

    def test_create_workflow(self):
        workflow_title = 'Sample Workflow'
        result = create_workflow(workflow_title)
        add_states(result, ['a', 'b', 'c'])
        add_states(result, ['e', 'f', 'g'])
        add_connection(result, [['a', 'to', 'b'], ['b', 'to', 'c']])
        result3 = create_task('hasher', [[result, 'newtask']])
        print result3