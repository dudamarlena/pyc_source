# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-QtVhoA/setuptools/setuptools/command/alias.py
# Compiled at: 2019-02-06 16:42:30
from distutils.errors import DistutilsOptionError
from setuptools.extern.six.moves import map
from setuptools.command.setopt import edit_config, option_base, config_file

def shquote(arg):
    """Quote an argument for later parsing by shlex.split()"""
    for c in ('"', "'", '\\', '#'):
        if c in arg:
            return repr(arg)

    if arg.split() != [arg]:
        return repr(arg)
    return arg


class alias(option_base):
    """Define a shortcut that invokes one or more commands"""
    description = 'define a shortcut to invoke one or more commands'
    command_consumes_arguments = True
    user_options = [
     ('remove', 'r', 'remove (unset) the alias')] + option_base.user_options
    boolean_options = option_base.boolean_options + ['remove']

    def initialize_options(self):
        option_base.initialize_options(self)
        self.args = None
        self.remove = None
        return

    def finalize_options(self):
        option_base.finalize_options(self)
        if self.remove and len(self.args) != 1:
            raise DistutilsOptionError('Must specify exactly one argument (the alias name) when using --remove')

    def run(self):
        aliases = self.distribution.get_option_dict('aliases')
        if not self.args:
            print 'Command Aliases'
            print '---------------'
            for alias in aliases:
                print (
                 'setup.py alias', format_alias(alias, aliases))

            return
        if len(self.args) == 1:
            alias, = self.args
            if self.remove:
                command = None
            else:
                if alias in aliases:
                    print (
                     'setup.py alias', format_alias(alias, aliases))
                    return
                else:
                    print 'No alias definition found for %r' % alias
                    return

        else:
            alias = self.args[0]
            command = (' ').join(map(shquote, self.args[1:]))
        edit_config(self.filename, {'aliases': {alias: command}}, self.dry_run)
        return


def format_alias(name, aliases):
    source, command = aliases[name]
    if source == config_file('global'):
        source = '--global-config '
    elif source == config_file('user'):
        source = '--user-config '
    elif source == config_file('local'):
        source = ''
    else:
        source = '--filename=%r' % source
    return source + name + ' ' + command