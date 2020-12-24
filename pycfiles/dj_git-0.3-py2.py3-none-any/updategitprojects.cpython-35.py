# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/damien/Dropbox/Projects/dj/git/management/commands/updategitprojects.py
# Compiled at: 2016-06-24 11:33:58
# Size of source mod 2**32: 1047 bytes
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
import sys
from git.utils import update_database, is_git_project
from git.models import Project, Commit
if not hasattr(settings, 'PROJECTS_DIR'):
    print('Please define PROJECTS_DIR in settings.py')
    sys.exit(1)
elif not Path(settings.PROJECTS_DIR).expanduser().is_dir():
    print("Can't find the directory {0} defined with PROJECTS_DIR.".format(settings.PROJECTS_DIR))
    sys.exit(1)
projects_dir = Path(settings.PROJECTS_DIR).expanduser()
projects = filter(is_git_project, projects_dir.iterdir())

class Command(BaseCommand):
    help = 'Updates the database'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write('Updating the database...')
        for project in projects:
            update_database(project)

        self.stdout.write('Number of projects: {0}'.format(Project.objects.all().count()))