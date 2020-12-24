# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wangwenpei/Codes/nextoa/cabric/cabric/components/hardline.py
# Compiled at: 2018-01-17 10:49:54
# Size of source mod 2**32: 2378 bytes
import json, os, subprocess
from cliez.component import Component
from cabric.utils import get_roots
try:
    from shlex import quote as shell_quote
except ImportError:
    from pipes import quote as shell_quote

class HardlineComponent(Component):

    def run(self, options):
        """
        :param options:
        :return:
        """
        package_root, _, _ = get_roots(options.dir)
        config_file = os.path.join(package_root, 'hardlines.json')
        if not os.path.exists(config_file):
            raise OSError('%s not exists' % config_file)
        try:
            hardlines = json.load(open(config_file, 'r'))
        except ValueError:
            self.error('Invalid json syntax:%s' % config_file)
            return False
        else:
            if not options.node:
                docs = [(v, hardlines[v].get('title', '')) for v in sorted(hardlines)]
                self.print_message('All Hardline:\n')
                self.print_message('\n'.join([v[0] + '\t' + v[1] for v in docs]))
                return
            else:
                node = hardlines.get(options.node, {})
                if not node:
                    self.error('Invalid node :%s' % options.node)
                    return False
                workflow = [v for v in node.get('workflow', []) if v[0:3] in ('cab',
                                                                              'fab') if '&' not in v if '|' not in v if '>' not in v if '<' not in v]
                if not workflow:
                    self.error('No workflow set.')
                    return False
                commands = '\n'.join(workflow)
                if options.preview:
                    self.print_message('WorkFlow:\n')
                    self.print_message(commands)
                    return
                commands = 'shopt -s expand_aliases\nsource ~/.bash_profile\n' + commands
                if options.debug:
                    self.print_message('commands will be execute:\n' + commands)
            subprocess.call(commands, shell=True, executable='/bin/bash')

    @classmethod
    def add_arguments(cls):
        """
        sub parser document
        """
        return [
         (
          ('--preview', ),
          dict(action='store_true', help='show task')),
         (
          ('node', ),
          dict(nargs='?', help='which node to active'))]