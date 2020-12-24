# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/commands/alias.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import print_function, unicode_literals
from collections import defaultdict
from subprocess import list2cmdline
import six
from rbtools.commands import command_exists, Command, CommandError, Option
from rbtools.utils.aliases import expand_alias
from rbtools.utils.filesystem import get_config_paths, parse_config_file

class Alias(Command):
    """A command for managing aliases defined in .reviewboardrc files."""
    name = b'alias'
    author = b'The Review Board Project'
    description = b'Manage aliases defined in .reviewboardrc files.'
    option_list = [
     Option(b'--list', action=b'store_true', dest=b'list_aliases', default=False, help=b'List all aliases defined in .reviewboardrc files.'),
     Option(b'--dry-run', metavar=b'ALIAS', dest=b'dry_run_alias', default=None, help=b'Print the command as it would be executed with the given command-line arguments.')]

    def list_aliases(self):
        """Print a list of .reviewboardrc aliases to the command line.

        This function shows in which file each alias is defined in and if the
        alias is valid (that is, if it won't be executable because an rbt
        command exists with the same name).
        """
        aliases = defaultdict(dict)
        predefined_aliases = {}
        config_paths = get_config_paths()
        for config_path in config_paths:
            config = parse_config_file(config_path)
            if b'ALIASES' in config:
                for alias_name, alias_cmd in six.iteritems(config[b'ALIASES']):
                    predefined = alias_name in predefined_aliases
                    aliases[config_path][alias_name] = {b'command': alias_cmd, 
                       b'overridden': predefined, 
                       b'invalid': command_exists(alias_name)}
                    if not predefined:
                        predefined_aliases[alias_name] = config_path

        for config_path in config_paths:
            if aliases[config_path]:
                print(b'[%s]' % config_path)
                for alias_name, entry in six.iteritems(aliases[config_path]):
                    print(b'    %s = %s' % (alias_name, entry[b'command']))
                    if entry[b'invalid']:
                        print(b'      !! This alias is overridden by an rbt command !!')
                    elif entry[b'overridden']:
                        print(b'      !! This alias is overridden by another alias in "%s" !!' % predefined_aliases[alias_name])

                print()

    def main(self, *args):
        """Run the command."""
        if self.options.list_aliases and self.options.dry_run_alias or not (self.options.list_aliases or self.options.dry_run_alias):
            raise CommandError(b'You must provide exactly one of --list or --dry-run.')
        if self.options.list_aliases:
            self.list_aliases()
        elif self.options.dry_run_alias:
            try:
                alias = self.config[b'ALIASES'][self.options.dry_run_alias]
            except KeyError:
                raise CommandError(b'No such alias "%s"' % self.options.dry_run_alias)

            command = expand_alias(alias, args)[0]
            print(list2cmdline(command))