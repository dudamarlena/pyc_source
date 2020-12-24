# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tgmigrate\command.py
# Compiled at: 2006-12-10 07:17:06
from migrate.versioning.shell import main
from turbogears import config
from turbogears.command.base import CommandWithDB

class MigrateCommand(CommandWithDB):
    """Make project to a Stand Alone Application
    """
    __module__ = __name__
    desc = 'Make the sqlalchemy migration'
    need_project = True

    def __init__(self, *args, **kwargs):
        self.find_config()
        self.name = 'migration'
        if config.get('sqlalchemy.dburi'):
            self.dburi = config.get('sqlalchemy.dburi')
        else:
            print 'you shold set sqlalchemy dburi in config first'

    def run(self):
        print 'The repository is %s\nThe dburi is in %s' % (self.name, self.dburi)
        main(url=self.dburi, repository=self.name, name=self.name)