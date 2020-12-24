# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/test/management/commands/testframework.py
# Compiled at: 2019-04-04 15:25:57
# Size of source mod 2**32: 7243 bytes
import os
from django.core.management import BaseCommand
from fabric.api import *
WORKSPACE_DIR = os.path.join(os.path.expanduser('~'), 'Documents/Workspace')

class Command(BaseCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--project', action='store_true', dest='project', default=False, help='Test project creation')
        parser.add_argument('--admin', action='store_true', dest='admin', default=False, help='Test admin application')
        parser.add_argument('--demo', action='store_true', dest='demo', default=False, help='Test demo applications')
        parser.add_argument('--installation', action='store_true', dest='installation', default=False, help='Test framework installation in debian/ubuntu')
        parser.add_argument('--implementation', action='store_true', dest='implementation', default=False, help='Test framework implementation with several projects')

    def handle(self, *args, **options):
        execute_tasks = []
        if options.get('project'):
            execute_tasks.append(_test_startpoject)
        else:
            if options.get('admin'):
                execute_tasks.append(_test_admin)
            else:
                if options.get('demo'):
                    execute_tasks.append(_test_demo_projects)
                else:
                    if options.get('installation'):
                        execute_tasks.append(_test_so_installation)
                    else:
                        if options.get('implementation'):
                            execute_tasks.append(_test_projects)
                        else:
                            execute_tasks = execute_tasks or [
                             _test_startpoject, _test_admin, _test_so_installation, _test_projects]
                        for execute_task in execute_tasks:
                            execute(execute_task)


EMPTY_TEST_FILE_CONTENT = "# -*- coding: utf-8 -*-\nfrom __future__ import unicode_literals\nfrom djangoplus._test_admin.models import User\nfrom djangoplus.test import TestCase\nfrom django.conf import settings\n\n\nclass AppTestCase(TestCase):\n\n    def test_app(self):\n\n        User.objects.create_superuser('_test_admin', None, settings.DEFAULT_PASSWORD)\n\n        self.login('_test_admin', settings.DEFAULT_PASSWORD)\n"
DOCKER_FILE_CONTENT = 'FROM {}\nENV DEBIAN_FRONTEND=noninteractive\nRUN apt-get update\nRUN apt-get -y install python3 python3-pip build-essential python3-dev libfreetype6-dev python3-cffi libtiff5-dev liblcms2-dev libwebp-dev tk8.6-dev libjpeg-dev ssh openssh-server dnsutils curl vim git wget\nRUN apt-get -y install chrpath libssl-dev libxft-dev libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev\nRUN apt-get -y install libgtk-3-dev\n\nRUN curl https://ftp.mozilla.org/pub/firefox/releases/60.0b3/linux-x86_64/en-US/firefox-60.0b3.tar.bz2 --output firefox.tar.bz2\nRUN tar xjf firefox.tar.bz2 --directory /usr/lib/\nRUN ln -s /usr/lib/firefox/firefox /usr/local/bin/firefox\nRUN rm firefox.tar.bz2\n\nRUN curl http://djangoplus.net/geckodriver-v0.21.0-linux64.tar.gz --output geckodriver.tar.gz\nRUN gunzip geckodriver.tar.gz\nRUN tar -xf geckodriver.tar\nRUN mv geckodriver /usr/local/bin/\nRUN rm geckodriver.tar\n\nENV LC_ALL=C.UTF-8\nENV LANG=C.UTF-8\nRUN export LANG=C.UTF-8\n\nRUN ln -sfn /usr/bin/pip3 /usr/bin/pip\nRUN ln -sfn /usr/bin/python3 /usr/bin/python\n\nRUN pip install --upgrade pip\n'
DEMO_PROJECTS = [
 ('petshop', 'git@bitbucket.org/brenokcc/petshop.git'),
 ('loja', 'git@bitbucket.org/brenokcc/loja.git'),
 ('biblioteca', 'git@bitbucket.org/brenokcc/biblioteca.git')]
EXTERAL_PROJECTS = [
 ('companies', 'git@djangoplus.net:companies.git'),
 ('emprestimos', 'git@djangoplus.net:emprestimos.git'),
 ('financeiro', 'git@bitbucket.org:brenokcc/financeiro.git'),
 ('formulacao', 'git@bitbucket.org:brenokcc/formulacao.git'),
 ('gerifes', 'git@bitbucket.org/brenokcc/gerifes.git'),
 ('simop', 'git@bitbucket.org/brenokcc/simop.git'),
 ('sigplac', 'git@bitbucket.org:brenokcc/sigplac.git'),
 ('gouveia', 'git@bitbucket.org:brenokcc/gouveia.git'),
 ('abstract', 'git@bitbucket.org:brenokcc/abstract.git'),
 ('blackpoint', 'git@bitbucket.org:brenokcc/blackpoint.git')]

def _test_startpoject():
    django_settings_module = os.environ['DJANGO_SETTINGS_MODULE']
    os.environ['DJANGO_SETTINGS_MODULE'] = 'xxx.settings'
    if os.path.exists('/tmp/xxx'):
        local('rm -r /tmp/xxx')
    with lcd('/tmp/'):
        local('startproject xxx')
        with lcd('/tmp/xxx'):
            local('python manage.py test')
        with lcd('/tmp'):
            local('rm -r /tmp/xxx')
    os.environ['DJANGO_SETTINGS_MODULE'] = django_settings_module


def _test_admin():
    local('python manage.py test djangoplus.admin.tests.AdminTestCase')


def _test_demo_projects():
    return _test_projects(external=False)


def _test_projects(demo=True, external=True):
    paths = []
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    projects = []
    if demo:
        projects += DEMO_PROJECTS
    if external:
        projects += EXTERAL_PROJECTS
    for project_name, project_url in projects:
        if os.path.exists(WORKSPACE_DIR):
            base_path = WORKSPACE_DIR
            if project_name in ('petshop', 'loja', 'biblioteca'):
                base_path = os.path.join(base_path, 'djangoplus/djangoplus-demos')
            project_path = os.path.join(base_path, project_name)
        else:
            project_path = os.path.join('/tmp', project_name)
            if not os.path.exists(project_path):
                local('git clone {} {}'.format(project_url, project_path))
            with lcd(project_path):
                local('git pull origin master')
        paths.append(project_path)

    django_settings_module = os.environ['DJANGO_SETTINGS_MODULE']
    for project_path in paths:
        project_name = project_path.split('/')[(-1)]
        print('Testing {}'.format(project_name))
        with lcd(project_path):
            os.environ['DJANGO_SETTINGS_MODULE'] = '{}.settings'.format(project_name)
            local('python manage.py test')

    os.environ['DJANGO_SETTINGS_MODULE'] = django_settings_module


def _test_testcases_generation():
    test_file_path = '{}/emprestimos/emprestimos/tests.py'.format(WORKSPACE_DIR)
    test_file_content = open(test_file_path).read()
    open(test_file_path, 'w').write(EMPTY_TEST_FILE_CONTENT)
    with lcd('{}/emprestimos'.format(WORKSPACE_DIR)):
        local('python manage.py test --add')
    print(open(test_file_path).read())
    open(test_file_path, 'w').write(test_file_content)


def _test_so_installation():
    for so in ('debian', ):
        docker_file = open('/tmp/Dockerfile', 'w')
        docker_file.write(DOCKER_FILE_CONTENT.format(so))
        docker_file.close()
        local('docker build -t djangoplus-{} /tmp'.format(so))
        django_settings_module = os.environ['DJANGO_SETTINGS_MODULE']
        os.environ['DJANGO_SETTINGS_MODULE'] = 'xyz.settings'
        local('docker run djangoplus-{} pip install djangoplus && startproject xyz && cd xyz && python manage.py test djangoplus.admin.tests.AdminTestCase'.format(so))
        os.environ['DJANGO_SETTINGS_MODULE'] = django_settings_module


def _test_deploy():
    pass