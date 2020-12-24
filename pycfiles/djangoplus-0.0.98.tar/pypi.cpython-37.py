# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/admin/management/commands/pypi.py
# Compiled at: 2018-10-14 16:33:48
# Size of source mod 2**32: 2468 bytes
import os, shutil, djangoplus
from django.core.management.base import BaseCommand
from fabric.api import local, execute, lcd
password = os.environ.get('TWINE_PASSWORD')
basedir = os.path.dirname(os.path.realpath(os.path.dirname(djangoplus.__file__)))

def release(upload=True):
    with lcd(basedir):
        version = None
        new_version = None
        setup_file_path = os.path.join(basedir, 'setup.py')
        setup_file_lines = open(setup_file_path).readlines()
        for i, line in enumerate(setup_file_lines):
            if 'version=' in line:
                version = line.strip()[-4:-2]
                new_version = str(int(version) + 1)
                setup_file_lines[i] = setup_file_lines[i].replace(version, new_version)
                break

        if new_version:
            if upload:
                open(setup_file_path, 'w').write(str(''.join(setup_file_lines)))
            github_git_dir_path = os.path.join(basedir, 'djangoplus/.git')
            github_git_tmp_path = '/tmp/djangoplus-version-{}'.format(version)
            print(version, '>>>', new_version)
            print('Moving', github_git_dir_path, github_git_tmp_path)
            shutil.move(github_git_dir_path, github_git_tmp_path)
            local('python setup.py sdist')
            print('Moving', github_git_tmp_path, github_git_dir_path)
            shutil.move(github_git_tmp_path, github_git_dir_path)
            if upload:
                local('twine upload dist/djangoplus-0.0.{}.tar.gz'.format(new_version))
                return new_version
            return version


def fake_release():
    version = release(False)
    with lcd(basedir):
        local('scp dist/djangoplus-0.0.{}.tar.gz root@djangoplus.net:/var/www/html/'.format(version))
        local('ssh root@djangoplus.net "chown www-data.www-data /var/www/html/djangoplus-0.0.{}.tar.gz"'.format(version))
        print('\n\n\nhttp://djangoplus.net/djangoplus-0.0.{}.tar.gz'.format(version))


class Command(BaseCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--fake', action='store_true', dest='fake', default=False, help='Upload to djangoplus.net instead of pypi.org')

    def handle(self, *args, **options):
        execute_task = release
        if options.get('fake'):
            execute_task = fake_release
        execute(execute_task)