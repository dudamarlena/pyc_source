# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lucaadalbertovandro/git/crowdschool/django_grunt/management/commands/gruntserver.py
# Compiled at: 2014-07-28 20:01:44
import os, subprocess, atexit, signal, sys
from django.conf import settings
from django.core.management.base import CommandError
from django.contrib.staticfiles.management.commands.runserver import Command as StaticfilesRunserverCommand

class Command(StaticfilesRunserverCommand):

    def inner_run(self, *args, **options):
        self.start_grunt()
        return super(Command, self).inner_run(*args, **options)

    def start_grunt(self):
        try:
            grunt_root = getattr(settings, 'GRUNTFILE_ROOT', settings.BASE_DIR)
        except AttributeError as e:
            if not getattr(settings, 'GRUNTFILE_ROOT', False):
                self.stderr.write('The GRUNTFILE_ROOT setting must not be empty')
                self.stderr.write('Set the GRUNTFILE_ROOT setting to the directory containing Gruntfile.js')
            else:
                raise e
            os._exit(1)

        self.stdout.write('>>> Starting grunt')
        self.grunt_process = subprocess.Popen([
         ('grunt --gruntfile={0}/Gruntfile.js --base=.').format(grunt_root)], shell=True, stdin=subprocess.PIPE, stdout=self.stdout, stderr=self.stderr)
        self.stdout.write(('>>> Grunt process on pid {0}').format(self.grunt_process.pid))

        def kill_grunt_process(pid):
            self.stdout.write('>>> Closing grunt process')
            os.kill(pid, signal.SIGTERM)

        atexit.register(kill_grunt_process, self.grunt_process.pid)