# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-projects/ovp_projects/tests/test_commands.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 1026 bytes
import sys
from io import StringIO
from django.test import TestCase
from django.utils import timezone
from ovp_users.models import User
from ovp_projects.models import Project, Job
from ovp_projects.management.commands.close_finished_projects import Command as CloseFinishedProjects

class TestCloseProjectsCommand(TestCase):

    def test_close_finished_projects(self):
        """Test close_finished_projects command"""
        user = User.objects.create_user(email='test_owner@test.com', password='test_owner')
        user.save()
        p = Project(name='test', owner=user)
        p.save()
        job = Job(start_date=timezone.now(), end_date=timezone.now(), project=p)
        job.save()
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            cmd = CloseFinishedProjects()
            cmd.handle()
            output = out.getvalue().strip()
        finally:
            sys.stdout = saved_stdout

        p = Project.objects.get(pk=p.pk)
        self.assertTrue(output == 'Closing 1 finished projects')
        self.assertTrue(p.closed)