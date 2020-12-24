# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/django-chuck/django_chuck/commands/install_modules.py
# Compiled at: 2012-06-13 09:41:05
from django_chuck.commands.base import BaseCommand
import os, sys, shutil
from django_chuck.utils import append_to_file, get_files, get_template_engine, compile_template
from random import choice

class Command(BaseCommand):
    help = 'Create all modules'
    modules_to_install = []
    installed_modules = []
    module_cache = {}
    post_build_actions = []

    def __init__(self):
        super(Command, self).__init__()
        self.opts.append(('modules',
         {'help': 'Comma seperated list of module names (can include pip modules)', 
            'default': 'core', 
            'nargs': '?'}))

    def install_module(self, module_name):
        module = self.module_cache.get(module_name, None)
        if module.cfg:
            cfg = self.inject_variables_and_functions(module.cfg)
            setattr(cfg, 'installed_modules', self.installed_modules)
            if module.post_build:
                self.post_build_actions.append((module.name, module.post_build))
        self.print_header('BUILDING ' + module.name)
        self.installed_modules.append(module)
        for f in get_files(module.dir):
            if 'chuck_module.py' not in f:
                input_file = f
                rel_path_old = f.replace(module.dir, '')
                rel_path_new = f.replace(module.dir, '').replace('project', self.project_name)
                output_file = f.replace(module.dir, self.site_dir).replace(rel_path_old, rel_path_new)
                print '\t%s -> %s' % (input_file, output_file)
                compile_template(input_file, output_file, self.placeholder, self.site_dir, self.project_dir, self.template_engine, self.debug)

        if module == 'core':
            secret_key = ('').join([ choice('abcdefghijklmnopqrstuvwxyz0123456789!@%^&*(-_=+)') for i in range(50) ])
            shutil.move(os.path.join(self.site_dir, '.gitignore_' + self.project_name), os.path.join(self.site_dir, '.gitignore'))
            append_to_file(os.path.join(self.project_dir, 'settings', 'common.py'), "\nSECRET_KEY = '" + secret_key + "'\n")
        self.installed_modules.append(module.name)
        return

    def handle(self, args, cfg):
        super(Command, self).handle(args, cfg)
        self.installed_modules = []
        self.module_cache = self.get_module_cache()
        self.modules_to_install = self.get_install_modules()
        template_engine = get_template_engine(self.site_dir, self.project_dir, cfg.get('template_engine'))
        self.placeholder = {'PROJECT_PREFIX': self.project_prefix, 
           'PROJECT_NAME': self.project_name, 
           'SITE_NAME': self.site_name, 
           'MODULE_BASEDIR': self.module_basedir, 
           'PYTHON_VERSION': self.python_version, 
           'PROJECT_BASEDIR': self.project_basedir, 
           'VIRTUALENV_BASEDIR': self.virtualenv_basedir, 
           'SERVER_PROJECT_BASEDIR': self.server_project_basedir, 
           'SERVER_VIRTUALENV_BASEDIR': self.server_virtualenv_basedir, 
           'EMAIL_DOMAIN': self.email_domain, 
           'MODULES': (',').join(self.modules_to_install)}
        if os.path.exists(self.site_dir) and not cfg.get('updating'):
            self.print_header('EXISTING PROJECT ' + self.site_dir)
            answer = raw_input('Delete old project dir? <y/N>: ')
            if answer.lower() == 'y' or answer.lower() == 'j':
                shutil.rmtree(self.site_dir)
                os.makedirs(self.site_dir)
            else:
                print 'Aborting.'
                sys.exit(0)
        else:
            os.makedirs(self.site_dir)
        self.modules_to_install = self.clean_module_list(self.modules_to_install, self.module_cache)
        for module in self.modules_to_install:
            self.install_module(module)

        not_installed_modules = [ m for m in self.modules_to_install if m not in self.installed_modules ]
        if not_installed_modules:
            print '\n<<< The following modules cannot be found ' + (',').join(not_installed_modules)
            self.kill_system()
        if (self.template_engine == 'django_chuck.template.notch_interactive.engine' or not self.template_engine) and not self.debug:
            for f in get_files(self.site_dir):
                template_engine.remove_keywords(f)

        if self.post_build_actions:
            self.print_header('EXECUTING POST BUILD ACTIONS')
            for action in self.post_build_actions:
                print '>>> ' + action[0]
                try:
                    action[1]()
                    print '\n'
                except Exception as e:
                    print str(e)
                    self.kill_system()