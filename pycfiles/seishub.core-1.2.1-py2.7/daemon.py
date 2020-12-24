# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\daemon.py
# Compiled at: 2010-12-23 17:42:43
"""
The SeisHub Daemon: platform-independent interface.
"""
from seishub.core.env import Environment
from seishub.core.services.manhole import ManholeService
from seishub.core.services.sftp import SFTPService
from seishub.core.services.ssh import SSHService
from seishub.core.services.web import WebService
from twisted.application import service
from twisted.python import usage
from twisted.scripts.twistd import _SomeApplicationRunner, ServerOptions
import sys
__all__ = [
 'run', 'createApplication']

def createApplication(path, log_file=None, create=False):
    application = service.Application('SeisHub')
    env = Environment(path, application=application, log_file=log_file, create=create)
    WebService(env)
    SSHService(env)
    ManholeService(env)
    SFTPService(env)
    return application


class SeisHubApplicationRunner(_SomeApplicationRunner):
    """
    """

    def __init__(self, config, log_file):
        _SomeApplicationRunner.__init__(self, config)
        self.log_file = log_file
        self.config = config

    def createOrGetApplication(self):
        return createApplication(self.config.get('rundir'), self.log_file)


def run():
    config = ServerOptions()
    try:
        config.parseOptions()
    except usage.error as ue:
        print config
        print '%s: %s' % (sys.argv[0], ue)
        return

    if config['nodaemon']:
        log_file = None
    else:
        log_file = 'seishub.log'
    SeisHubApplicationRunner(config, log_file).run()
    return


if __name__ == '__main__':
    run()