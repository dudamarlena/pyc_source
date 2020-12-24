# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/movister/env/src/fabriclassed/fabriclassed/contrib/django.py
# Compiled at: 2015-02-27 04:15:18
from fabric.api import local, run, cd
from os.path import join
import re

class DjangoFabric(object):
    """
    Fabric command file with base django's manage.py commands
    """
    manage_file = './manage.py'
    test_default_app = None
    test_settings = None
    settings_remote_db = 'settings_remote_db'
    shell_plus = False
    devserver_port = 8000
    devserver_params = ''
    fixtures_dir = 'fixtures'
    fixtures_format = 'json'
    fixtures_map = ('sites.site', )

    def get_manage_commend(self, command, settings=False):
        return '%(manage)s %(command)s %(settings)s' % {'manage': self.manage_file, 
           'command': command, 
           'settings': '--settings=%s' % settings if settings else ''}

    def local_manage(self, *args, **kwargs):
        """
        Run manage.py on development
        """
        if 'remote_db' in kwargs and kwargs.pop('remote_db'):
            kwargs['settings'] = self.settings_remote_db
        if getattr(self, 'use_virtualenv', False):
            with self.virtualenv():
                local(self.get_manage_commend(*args, **kwargs), capture=False)
        else:
            local(self.get_manage_commend(*args, **kwargs), capture=False)

    def run_manage(self, *args, **kwargs):
        """
        Run manage.py on production
        """
        if getattr(self, 'use_virtualenv', False):
            with self.virtualenv(remote=True):
                run(self.get_manage_commend(*args, **kwargs))
        else:
            run(self.get_manage_commend(*args, **kwargs))

    def fab_dev(self, remote_db=False):
        """
        Run Django's dev server
        """
        self.local_manage('runserver %(params)s %(host)s:%(port)d' % {'host': self.hosts[0] if self.is_remote() else '127.0.0.1', 
           'port': self.devserver_port, 
           'params': self.devserver_params}, remote_db=remote_db)

    def fab_sh(self, remote_db=False, sql=False):
        """
        Run Django's standart shell or shell from django_extentions application if `shell_plus=True`
        """
        command = 'shell_plus' if self.shell_plus else 'shell'
        sql = ' --print-sql' if sql else ''
        self.local_manage(command + sql, remote_db=remote_db)

    def fab_test(self, test_name=''):
        """
        Run Django's tests. Argument can be application name, name of test class or method of test class
        """
        if self.test_default_app:
            if not test_name:
                test_name = self.test_default_app
            if re.search('^[^\\.]+Test', test_name):
                test_name = ('.').join([self.test_default_app, test_name])
        self.local_manage('test %(name)s' % {'name': test_name}, settings=self.test_settings)

    def get_fixtures_file(self, model):
        return join(self.fixtures_dir, ('.').join([model, self.fixtures_format]))

    def fab_update_fixtures(self):
        """
        Put remote fixtures to repository on production, get and load them on development
        """
        with cd(self.remote_project_path):
            for model in self.fixtures_map:
                self.run_manage('dumpdata --format=%s %s > %s' % (self.fixtures_format, model, self.get_fixtures_file(model)))

            run('git add %s' % self.fixtures_dir)
            run('git commit -m "updated fixtures"')
            run('git push')
        local('git pull', capture=False)
        for model in self.fixtures_map:
            self.local_manage('loaddata %s' % self.get_fixtures_file(model))