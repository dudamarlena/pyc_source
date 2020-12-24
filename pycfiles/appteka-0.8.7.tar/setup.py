# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apps/command/setup.py
# Compiled at: 2010-08-17 19:03:01
import logging, os, pkg_resources, shutil, sys, apps.command.base

class setup(apps.command.base.Command):
    help = 'Build a project directory and do initial setup.'
    dirs = ['css', 'html', 'lib', 'packages', 'test', 'build']
    user_options = [('name=', None, 'Name of the project to create.', None)]
    post_commands = ['generate']

    def create_dirs(self):
        for i in self.dirs:
            os.makedirs(os.path.join(self.project.path, i))

    def move_defaults(self):
        shutil.copy(pkg_resources.resource_filename('apps.data', '.ignore'), os.path.join(self.project.path, '.ignore'))
        shutil.copy(pkg_resources.resource_filename('apps.data', 'icon.bmp'), os.path.join(self.project.path, 'icon.bmp'))
        shutil.copy(pkg_resources.resource_filename('apps.data', 'main.html'), os.path.join(self.project.path, 'html', 'main.html'))
        shutil.copy(pkg_resources.resource_filename('apps.data', 'main.css'), os.path.join(self.project.path, 'css', 'main.css'))
        shutil.copy(pkg_resources.resource_filename('apps.data', 'index.js'), os.path.join(self.project.path, 'lib', 'index.js'))

    def run(self):
        if not self.options.get('name', None):
            logging.error('Must use the `--name` option to name the project.')
            return -1
        else:
            if os.path.exists(self.project.path):
                logging.error("The project already exists. Remove it if you'd like to create it again.")
                return -1
            self.create_dirs()
            self.write_metadata()
            self.move_defaults()
            self.update_deps()
            os.chdir(self.project.path)
            logging.error('Your new project is ready.')
            logging.error('To get started, you can find your new project in the "%s" directory' % (
             self.project.metadata['name'],))
            return