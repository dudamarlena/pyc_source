# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/pyami/installers/ubuntu/installer.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3545 bytes
import boto.pyami.installers, os, os.path, stat, boto, random
from pwd import getpwnam

class Installer(boto.pyami.installers.Installer):
    """Installer"""

    def add_cron(self, name, command, minute='*', hour='*', mday='*', month='*', wday='*', who='root', env=None):
        """
        Write a file to /etc/cron.d to schedule a command
            env is a dict containing environment variables you want to set in the file
            name will be used as the name of the file
        """
        if minute == 'random':
            minute = str(random.randrange(60))
        if hour == 'random':
            hour = str(random.randrange(24))
        fp = open('/etc/cron.d/%s' % name, 'w')
        if env:
            for key, value in env.items():
                fp.write('%s=%s\n' % (key, value))

        fp.write('%s %s %s %s %s %s %s\n' % (minute, hour, mday, month, wday, who, command))
        fp.close()

    def add_init_script(self, file, name):
        """
        Add this file to the init.d directory
        """
        f_path = os.path.join('/etc/init.d', name)
        f = open(f_path, 'w')
        f.write(file)
        f.close()
        os.chmod(f_path, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
        self.run('/usr/sbin/update-rc.d %s defaults' % name)

    def add_env(self, key, value):
        """
        Add an environemnt variable
        For Ubuntu, the best place is /etc/environment.  Values placed here do
        not need to be exported.
        """
        boto.log.info('Adding env variable: %s=%s' % (key, value))
        if not os.path.exists('/etc/environment.orig'):
            self.run('cp /etc/environment /etc/environment.orig', notify=False, exit_on_error=False)
        fp = open('/etc/environment', 'a')
        fp.write('\n%s="%s"' % (key, value))
        fp.close()
        os.environ[key] = value

    def stop(self, service_name):
        self.run('/etc/init.d/%s stop' % service_name)

    def start(self, service_name):
        self.run('/etc/init.d/%s start' % service_name)

    def create_user(self, user):
        """
        Create a user on the local system
        """
        self.run('useradd -m %s' % user)
        usr = getpwnam(user)
        return usr

    def install(self):
        """
        This is the only method you need to override
        """
        raise NotImplementedError