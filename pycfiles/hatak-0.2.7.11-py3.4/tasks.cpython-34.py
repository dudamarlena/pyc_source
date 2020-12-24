# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bael/hatak/tasks.py
# Compiled at: 2015-05-15 05:53:06
# Size of source mod 2**32: 3521 bytes
from os import mkdir, path
from bael.project.virtualenv import VirtualenvTask
from baelfire.application.commands.init.models import InitFile
from baelfire.dependencies import AlwaysRebuild, FileDoesNotExists
from baelfire.task import Task

class CreateDataDir(Task):
    name = 'Creating data directory'
    path = '/data'
    directorie_names = [
     'datadir']

    @property
    def directories(self):
        for name in self.directorie_names:
            yield self.paths[name]

    def generate_dependencies(self):
        for directory in self.directories:
            self.add_dependecy(FileDoesNotExists(directory))

    def make(self):
        for directory in self.directories:
            if not path.exists(directory):
                mkdir(directory)
                continue


class Develop(Task):

    def generate_links(self):
        self.add_link('bael.hatak.templates:FrontendIni')
        self.add_link('bael.project.virtualenv:Develop')
        self.add_link('bael.hatak.alembic:AlembicMigration')


class CommandTask(VirtualenvTask):

    def generate_dependencies(self):
        self.add_dependecy(AlwaysRebuild())

    def generate_links(self):
        self.add_link(Develop)


class Serve(CommandTask):
    name = 'Run development server'
    path = '/serve'

    def make(self):
        self.pserve('%(data:frontend.ini)s --reload' % self.paths)

    def pserve(self, command, *args, **kwargs):
        command = self.paths['exe:pserve'] + ' ' + command
        return self.command([command], *args, **kwargs)


class Shell(VirtualenvTask):
    name = 'Run development shell'
    path = '/shell'

    def generate_dependencies(self):
        self.add_dependecy(AlwaysRebuild())

    def generate_links(self):
        self.add_link(Develop)

    def make(self):
        self.pshell('%(data:frontend.ini)s' % self.paths)

    def pshell(self, command, *args, **kwargs):
        command = self.paths['exe:pshell'] + ' ' + command
        return self.command([command], *args, **kwargs)


class BaelfireInitFile(Task):
    path = '/initfile'

    def get_output_file(self):
        return InitFile.filename

    def make(self):
        initfile = InitFile()
        initfile.assign('bael.hatak.recipe:HatakRecipe')
        initfile.save()


class ProjectTemplates(Task):
    path = '/templates'

    def generate_links(self):
        self.add_link('bael.hatak.templates:InitPy')
        self.add_link('bael.hatak.templates:ManagePy')
        self.add_link('bael.hatak.templates:Routes')
        self.add_link('bael.hatak.templates:Settings')
        self.add_link('bael.hatak.templates:TestFixtures')
        self.add_link('bael.hatak.templates:Conftest')
        self.add_link('bael.hatak.templates:Pytestini')
        self.add_link('bael.hatak.templates:TestSettings')
        self.add_link('bael.hatak.templates:RedmeFile')
        self.add_link('bael.hatak.templates:PShell')


class Tests(CommandTask):
    name = 'Run tests'
    path = '/tests'

    def make(self):
        if 'g' in self.kwargs:
            self.tests('%s' % self.kwargs['g'][0])
        else:
            self.tests()

    def tests(self, command='', *args, **kwargs):
        kwargs['cwd'] = self.paths['project:src']
        command = self.paths['exe:pytest'] + '  ' + command
        return self.command([command], *args, **kwargs)


class Coverage(Tests):
    name = 'Generate test coverage report'
    path = '/tests/coverage'

    def make(self):
        self.tests('--cov %(package:name)s' % self.settings)