# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/scripts/staticwiki.py
# Compiled at: 2010-01-24 10:23:30
"""Script to handle staticwiki sub-command from paster"""
from os.path import abspath
from paste.script import command
from zeta.comp.environ import open_environment

class CmdStaticWiki(command.Command):
    max_args = 2
    min_args = 2
    usage = 'action <dir>'
    summary = 'Pull or push static wiki tree from file system to DataBase'
    group_name = 'zeta_staticwiki'
    parser = command.Command.standard_parser(verbose=True)

    def command(self):
        """Handle the sub-command"""
        from zeta.comp.system import SystemComponent
        compmgr = open_environment(False)
        syscomp = SystemComponent(compmgr)
        if len(self.args) == 2:
            action = self.args[0]
            rootdir = abspath(self.args[1])
        else:
            action = ''
            rootdir = ''
        if action == 'pull':
            print 'Pulling Static wiki files into %s ...' % rootdir
            files = syscomp.pull_staticwiki(rootdir)
            for f in files:
                print '    ', f

        elif action == 'push':
            print 'Pushing Static wiki files from %s ...' % rootdir
            (files, skipped) = syscomp.push_staticwiki(rootdir)
            for f in files:
                print '    ', f

            print 'Skipped files ...'
            for f in skipped:
                print '    ', f

        else:
            print 'Please provide a valid command. Use -h to know the usage ...'