# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/management/commands/uwsgi_conf.py
# Compiled at: 2015-09-25 04:10:37
import os
from django.core.management import BaseCommand
from django.conf import settings

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-n', '--name', type=str, dest='name', help='Name of the project. This should be same as the basename for the .wsgi file', nargs='?')
        parser.add_argument('-p', '--port', dest='port', type=int, help='Project port')

    def handle(self, **options):
        base_dir = os.path.abspath(os.path.join(os.environ['VIRTUAL_ENV'], '../'))
        content = template.format(project_dir=base_dir.rstrip('/') + '/', project_name=options['name'], project_port=options['port'])
        self.stdout.write(content)


template = '\n[uwsgi]\n\nchdir           = {project_dir}src/\n\nmodule          = {project_name}.wsgi\n\nhome            = {project_dir}venv/\n\nenv = VIRTUAL_ENV={project_dir}venv/\n\nhttp-socket     = 0.0.0.0:{project_port}\n\nmaster          = true\n\npidfile         = {project_dir}run/uwsgi.pid\n\n#logto           = {project_dir}log/uwsgi.log\n\nprocesses       = 2\n\nthreads         = 10\n\nvacuum          = true\n\nharakiri-verbose= 1\n\nauto-procname   = 1\n\nno-orphans      = 1\n\nmaster          = 1\n\ndisable-logging = false\n\nlimit-post      = 153600000\n\nhttp-timeout    = 10\n\nthreads         = 10\n\nenable-threads  = 1\n\ntouch-reload    = {project_dir}src/uwsgi.ini\n'