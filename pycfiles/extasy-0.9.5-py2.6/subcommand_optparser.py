# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\extasy\subcommand_optparser.py
# Compiled at: 2010-11-20 06:10:24
"""A simple addition to Python's optparse module supporting subcommands
like those found in the svn or hg CLIs.

To use it, instantiate the Subcommand class for every subcommand you
want to support. Each subcommand has a name, aliases, a help message,
and a separate OptionParser instance. Then pass a list of Subcommands
to the constructor of SubcommandsOptionParser to make a subcommand-
aware parser. Calling parse_args on that parser gives you the
subcommand invoked, the subcommand's arguments and options, and the
global options all in one fell swoop. See the smoke test at the bottom
of the file for an example.

The SubcommandsOptionParser automatically adds a "help" command for
getting global help or (with an argument) help on a specific
subcommand.

I wrote this because none of the more sophisticated command-line
parsers that support subcommands (argparse, cmdln, opster, pyopt,
optfunc, simpleopt). Many of them sport a bizarre, introspection- or
decorator-based API that doesn't lend itself well to extensibility.
argparse is the most promising (and will be included in the standard
library), but crucially lacks support for aliasing and has cosmetic
issues with the help output for subcommands.
"""
import optparse, textwrap

class Subcommand(object):
    """A subcommand of a root command-line application that may be
    invoked by a SubcommandOptionParser.
    """

    def __init__(self, name, parser=None, help='', aliases=()):
        """Creates a new subcommand. name is the primary way to invoke
        the subcommand; aliases are alternate names. parser is an
        OptionParser responsible for parsing the subcommand's options.
        help is a short description of the command. If no parser is
        given, it defaults to a new, empty OptionParser.
        """
        self.name = name
        self.parser = parser or optparse.OptionParser()
        self.aliases = aliases
        self.help = help


class SubcommandsOptionParser(optparse.OptionParser):
    """A variant of OptionParser that parses subcommands and their
    arguments.
    """
    _HelpSubcommand = Subcommand('help', optparse.OptionParser(), help='give detailed help on a specific sub-command', aliases=('?', ))

    def __init__(self, *args, **kwargs):
        """Create a new subcommand-aware option parser. All of the
        options to OptionParser.__init__ are supported in addition
        to subcommands, a sequence of Subcommand objects.
        """
        self.subcommands = list(kwargs.pop('subcommands', []))
        self.subcommands.append(self._HelpSubcommand)
        if 'usage' not in kwargs:
            kwargs['usage'] = '\n  %prog COMMAND [ARGS...]\n  %prog help COMMAND'
        optparse.OptionParser.__init__(self, *args, **kwargs)
        for subcommand in self.subcommands:
            subcommand.parser.prog = '%s %s' % (
             self.get_prog_name(), subcommand.name)

        self.disable_interspersed_args()

    def add_subcommand(self, cmd):
        """Adds a Subcommand object to the parser's list of commands.
        """
        self.subcommands.append(cmd)

    def format_help(self, formatter=None):
        out = optparse.OptionParser.format_help(self, formatter)
        if formatter is None:
            formatter = self.formatter
        result = [
         '\n']
        result.append(formatter.format_heading('Commands'))
        formatter.indent()
        disp_names = []
        help_position = 0
        for subcommand in self.subcommands:
            name = subcommand.name
            if subcommand.aliases:
                name += ' (%s)' % (', ').join(subcommand.aliases)
            disp_names.append(name)
            proposed_help_position = len(name) + formatter.current_indent + 2
            if proposed_help_position <= formatter.max_help_position:
                help_position = max(help_position, proposed_help_position)

        for (subcommand, name) in zip(self.subcommands, disp_names):
            name_width = help_position - formatter.current_indent - 2
            if len(name) > name_width:
                name = '%*s%s\n' % (formatter.current_indent, '', name)
                indent_first = help_position
            else:
                name = '%*s%-*s  ' % (formatter.current_indent, '',
                 name_width, name)
                indent_first = 0
            result.append(name)
            help_width = formatter.width - help_position
            help_lines = textwrap.wrap(subcommand.help, help_width)
            result.append('%*s%s\n' % (indent_first, '', help_lines[0]))
            result.extend([ '%*s%s\n' % (help_position, '', line) for line in help_lines[1:]
                          ])

        formatter.dedent()
        return out + ('').join(result)

    def _subcommand_for_name(self, name):
        """Return the subcommand in self.subcommands matching the
        given name. The name may either be the name of a subcommand or
        an alias. If no subcommand matches, returns None.
        """
        for subcommand in self.subcommands:
            if name == subcommand.name or name in subcommand.aliases:
                return subcommand

        return

    def parse_args(self, a=None, v=None):
        """Like OptionParser.parse_args, but returns these four items:
        - options: the options passed to the root parser
        - subcommand: the Subcommand object that was invoked
        - suboptions: the options passed to the subcommand parser
        - subargs: the positional arguments passed to the subcommand
        """
        (options, args) = optparse.OptionParser.parse_args(self, a, v)
        if not args:
            self.print_help()
            self.exit()
        else:
            cmdname = args.pop(0)
            subcommand = self._subcommand_for_name(cmdname)
            if not subcommand:
                self.error('unknown command ' + cmdname)
        (suboptions, subargs) = subcommand.parser.parse_args(args)
        if subcommand is self._HelpSubcommand:
            if subargs:
                cmdname = subargs[0]
                helpcommand = self._subcommand_for_name(cmdname)
                helpcommand.parser.print_help()
                self.exit()
            else:
                self.print_help()
                self.exit()
        return (
         options, subcommand, suboptions, subargs)


if __name__ == '__main__':
    add_cmd = Subcommand('add', optparse.OptionParser(usage='%prog [OPTIONS] FILE...'), 'add the specified files on the next commit')
    add_cmd.parser.add_option('-n', '--dry-run', dest='dryrun', help='do not perform actions, just print output', action='store_true')
    commit_cmd = Subcommand('commit', optparse.OptionParser(usage='%prog [OPTIONS] [FILE...]'), 'commit the specified files or all outstanding changes', ('ci', ))
    long_cmd = Subcommand('very_very_long_command_name', optparse.OptionParser(), 'description should start on next line')
    long_help_cmd = Subcommand('somecmd', optparse.OptionParser(), 'very long help text should wrap to the next line at which point the indentation should match the previous line', ('history', ))
    parser = SubcommandsOptionParser(subcommands=(
     add_cmd, commit_cmd, long_cmd, long_help_cmd))
    parser.add_option('-R', '--repository', dest='repository', help='repository root directory or symbolic path name', metavar='PATH')
    parser.add_option('-v', dest='verbose', help='enable additional output', action='store_true')
    (options, subcommand, suboptions, subargs) = parser.parse_args()
    if subcommand is add_cmd:
        if subargs:
            print 'Adding files:', (', ').join(subargs)
            print 'Dry run:',
            print 'yes' if suboptions.dryrun else 'no'
        else:
            subcommand.parser.error('need at least one file to add')
    elif subcommand is commit_cmd:
        if subargs:
            print 'Committing files:', (', ').join(subargs)
        else:
            print 'Committing all changes.'
    else:
        print '(dummy command)'
    print 'Repository:',
    print options.repository if options.repository else '(default)'
    print 'Verbose:',
    print 'yes' if options.verbose else 'no'