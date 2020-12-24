# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/django_workflow/management/commands/autotransitions.py
# Compiled at: 2017-08-29 12:05:44
from django.core.management import BaseCommand
from django_workflow import workflow
__author__ = 'Daniele Bernardini'

class Command(BaseCommand):
    help = 'trigger automatic transitions in django_workflow'

    def handle(self, *args, **options):
        workflow_name = None
        if len(args) > 0:
            workflow_name = args[0]
        workflow.execute_automatic_transitions(workflow_name=workflow_name)
        return