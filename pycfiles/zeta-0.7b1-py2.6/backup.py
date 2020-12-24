# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/scripts/backup.py
# Compiled at: 2010-01-24 10:23:28
"""Script to handle 'backup' sub-command from paster,
    backup -z <bkpcmd>
    
    bkpcmd,     db (or) db,env (or) all
                default is all 
"""
from paste.script import command

class Backup(command.Command):
    max_args = 1
    min_args = 1
    usage = 'bkpcmd'
    summary = 'Backup database and environment into a tar ball'
    group_name = 'zeta_backup'
    parser = command.Command.standard_parser(verbose=True)
    parser.add_option('-z', action='store_true', dest='gzip', help='Gzip the tar-ball')

    def command(self):
        """Handle the backup sub-command"""
        pass