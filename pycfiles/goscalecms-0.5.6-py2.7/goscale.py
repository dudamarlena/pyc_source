# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/management/commands/goscale.py
# Compiled at: 2013-03-18 00:49:37
from __future__ import absolute_import
from cms.management.commands.subcommands.base import SubcommandsCommand
from goscale.management.commands.subcommands.update_posts import UpdatePosts
from goscale.management.commands.subcommands.update_slugs import UpdateSlugs
from django.core.management.base import BaseCommand
from optparse import make_option

class Command(SubcommandsCommand):
    args = '<subcommand>'
    option_list = BaseCommand.option_list + (
     make_option('-s', '--site', default=None, help='Site ID to filter plugins.'),
     make_option('-t', '--theme', default=None, help='Theme name to filter plugins.'))
    command_name = 'goscale'
    subcommands = {'update_posts': UpdatePosts, 
       'update_slugs': UpdateSlugs}

    @property
    def help(self):
        lines = ['GoScale CMS command line interface.', '', 'Available subcommands:']
        for subcommand in sorted(self.subcommands.keys()):
            lines.append('  %s' % subcommand)

        lines.append('')
        lines.append('Use `manage.py %s <subcommand> --help` for help about subcommands' % self.command_name)
        return ('\n').join(lines)