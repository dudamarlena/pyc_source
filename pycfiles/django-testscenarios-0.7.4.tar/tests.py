# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/neil/code/lava/django-testscenarios/django_testscenarios/test_project/tests.py
# Compiled at: 2013-10-11 14:56:26
from django_testproject.tests import run_tests_for

def run_tests():
    return run_tests_for('django_testscenarios.test_project.settings')


if __name__ == '__main__':
    run_tests()