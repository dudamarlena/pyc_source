# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/argos/Workspace/mamba-framework/mamba-server/mamba_server/commands/gencomponent.py
# Compiled at: 2020-05-07 10:19:34
# Size of source mod 2**32: 972 bytes
from mamba_server.commands import MambaCommand

class Command(MambaCommand):

    def syntax(self):
        return '[options] <name> <domain>'

    def short_desc(self):
        return 'Generate new component using pre-defined templates'

    def add_options(self, parser):
        MambaCommand.add_options(self, parser)
        parser.add_option('-l', '--list', dest='list', action='store_true', help='List available templates')
        parser.add_option('-e', '--edit', dest='edit', action='store_true', help='Edit spider after creating it')
        parser.add_option('-d', '--dump', dest='dump', metavar='TEMPLATE', help='Dump template to standard output')
        parser.add_option('-t', '--template', dest='template', default='basic', help='Uses a custom template.')
        parser.add_option('--force', dest='force', action='store_true', help='If the spider already exists, overwrite it with the template')