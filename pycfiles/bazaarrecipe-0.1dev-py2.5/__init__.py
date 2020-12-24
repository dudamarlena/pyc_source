# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bazaarrecipe/__init__.py
# Compiled at: 2007-12-02 15:45:22
import os, subprocess, logging, zc.buildout

class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.logger = logging.getLogger(name)
        base_dir = buildout['buildout']['directory']
        options['location'] = os.path.join(base_dir, name)

    def install(self):
        location = self.options['location']
        if not os.path.exists(location):
            os.makedirs(location)
        for (url, path) in self.urls():
            abs_path = os.path.join(location, path)
            self.logger.info(path)
            self.command('bzr branch %s %s' % (url, abs_path))

        return location

    def update(self):
        if self.buildout['buildout'].get('offline') == 'true':
            return
        location = self.options['location']
        for (url, path) in self.urls():
            abs_path = os.path.join(location, path)
            self.logger.info(path)
            self.command('bzr pull', abs_path)

    def command(self, cmd, working_dir=None):
        if working_dir is not None:
            old_cwd = os.getcwd()
            os.chdir(working_dir)
        output = subprocess.PIPE
        if self.buildout['buildout'].get('verbosity'):
            output = None
        command = subprocess.Popen(cmd, shell=True, stdout=output)
        if working_dir is not None:
            os.chdir(old_cwd)
        assert command.wait() == 0
        return

    def urls(self):
        for line in self.options['urls'].splitlines():
            if line:
                try:
                    (url, target) = line.split()
                except ValueError:
                    raise zc.buildout.UserError('Invalid URL specification: ' + line)
                else:
                    yield (
                     url, target)


def uninstall(name, options):
    location = options['location']
    old_cwd = os.getcwd()
    try:
        for f in os.listdir(location):
            branch = os.path.join(location, f)
            os.chdir(branch)
            command = subprocess.Popen('bzr status', shell=True, stdout=subprocess.PIPE)
            assert command.wait() == 0
            output = command.stdout.read()
            if output.strip():
                raise zc.buildout.UserError('Uncommitted changes:\n' + output)

    finally:
        os.chdir(old_cwd)