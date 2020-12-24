# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/scripts/zwiki.py
# Compiled at: 2010-01-24 10:23:30
"""Script to handle staticwiki sub-command from paster
        zwiki upgradedb"""
from paste.script import command
from pylons import config
from zeta.comp.environ import open_environment

class CmdZwiki(command.Command):
    max_args = 1
    min_args = 1
    usage = 'upgradedb'
    summary = 'Upgrade the translated HTML content to latest zwiki'
    group_name = 'zeta_zwiki'
    parser = command.Command.standard_parser(verbose=True)

    def command(self):
        """Handle the sub-command"""
        from zeta.comp.system import SystemComponent
        from zeta.comp.ticket import TicketComponent
        from zeta.comp.wiki import WikiComponent
        if len(self.args) == 1 and self.args[0] == 'upgradedb':
            syscomp = SystemComponent(compmgr)
            tckcomp = TicketComponent(compmgr)
            wikicomp = WikiComponent(compmgr)
            count = syscomp.upgradewiki()
            print 'Upgraded %s static wiki pages ... ok' % count
            count = tckcomp.upgradewiki()
            print 'Upgraded %s ticket comments ... ok' % count
            (cnt_wcnt, cnt_wcmt) = wikicomp.upgradewiki()
            print 'Upgraded %s wiki contents and %s wiki comments ... ok' % (
             cnt_wcnt, cnt_wcmt)
        else:
            print 'Please provide a valid command. Use -h to know the usage ...'