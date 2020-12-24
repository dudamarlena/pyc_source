# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/compatibility/optparse.py
# Compiled at: 2009-10-07 18:08:46
"""optparse - a powerful, extensible, and easy-to-use option parser.

By Greg Ward <gward@python.net>

Originally distributed as Optik; see http://optik.sourceforge.net/ .

If you have problems with this module, please do not file bugs,
patches, or feature requests with Python; instead, use Optik's
SourceForge project page:
  http://sourceforge.net/projects/optik

For support, use the optik-users@lists.sourceforge.net mailing list
(http://lists.sourceforge.net/lists/listinfo/optik-users).
"""
__version__ = '1.4.1+'
__all__ = [
 'Option', 'SUPPRESS_HELP', 'SUPPRESS_USAGE', 'STD_HELP_OPTION', 'STD_VERSION_OPTION', 'Values', 'OptionContainer', 'OptionGroup', 'OptionParser', 'HelpFormatter', 'IndentedHelpFormatter', 'TitledHelpFormatter', 'OptParseError', 'OptionError', 'OptionConflictError', 'OptionValueError', 'BadOptionError']
__copyright__ = '\nCopyright (c) 2001-2003 Gregory P. Ward.  All rights reserved.\n\nRedistribution and use in source and binary forms, with or without\nmodification, are permitted provided that the following conditions are\nmet:\n\n  * Redistributions of source code must retain the above copyright\n    notice, this list of conditions and the following disclaimer.\n\n  * Redistributions in binary form must reproduce the above copyright\n    notice, this list of conditions and the following disclaimer in the\n    documentation and/or other materials provided with the distribution.\n\n  * Neither the name of the author nor the names of its\n    contributors may be used to endorse or promote products derived from\n    this software without specific prior written permission.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS\nIS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED\nTO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A\nPARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR\nCONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,\nEXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,\nPROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR\nPROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF\nLIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING\nNEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\nSOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n'
import sys, os, types, textwrap

class OptParseError(Exception):
    __module__ = __name__

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class OptionError(OptParseError):
    """
    Raised if an Option instance is created with invalid or
    inconsistent arguments.
    """
    __module__ = __name__

    def __init__(self, msg, option):
        self.msg = msg
        self.option_id = str(option)

    def __str__(self):
        if self.option_id:
            return 'option %s: %s' % (self.option_id, self.msg)
        else:
            return self.msg


class OptionConflictError(OptionError):
    """
    Raised if conflicting options are added to an OptionParser.
    """
    __module__ = __name__


class OptionValueError(OptParseError):
    """
    Raised if an invalid option value is encountered on the command
    line.
    """
    __module__ = __name__


class BadOptionError(OptParseError):
    """
    Raised if an invalid or ambiguous option is seen on the command-line.
    """
    __module__ = __name__


class HelpFormatter:
    """
    Abstract base class for formatting option help.  OptionParser
    instances should use one of the HelpFormatter subclasses for
    formatting help; by default IndentedHelpFormatter is used.

    Instance attributes:
      indent_increment : int
        the number of columns to indent per nesting level
      max_help_position : int
        the maximum starting column for option help text
      help_position : int
        the calculated starting column for option help text;
        initially the same as the maximum
      width : int
        total number of columns for output
      level : int
        current indentation level
      current_indent : int
        current indentation level (in columns)
      help_width : int
        number of columns available for option help text (calculated)
    """
    __module__ = __name__

    def __init__(self, indent_increment, max_help_position, width, short_first):
        self.indent_increment = indent_increment
        self.help_position = self.max_help_position = max_help_position
        self.width = width
        self.current_indent = 0
        self.level = 0
        self.help_width = width - max_help_position
        self.short_first = short_first

    def indent(self):
        self.current_indent += self.indent_increment
        self.level += 1

    def dedent(self):
        self.current_indent -= self.indent_increment
        assert self.current_indent >= 0, 'Indent decreased below 0.'
        self.level -= 1

    def format_usage(self, usage):
        raise NotImplementedError, 'subclasses must implement'

    def format_heading(self, heading):
        raise NotImplementedError, 'subclasses must implement'

    def format_description(self, description):
        desc_width = self.width - self.current_indent
        indent = ' ' * self.current_indent
        return textwrap.fill(description, desc_width, initial_indent=indent, subsequent_indent=indent)

    def format_option(self, option):
        result = []
        opts = option.option_strings
        opt_width = self.help_position - self.current_indent - 2
        if len(opts) > opt_width:
            opts = '%*s%s\n' % (self.current_indent, '', opts)
            indent_first = self.help_position
        else:
            opts = '%*s%-*s  ' % (self.current_indent, '', opt_width, opts)
            indent_first = 0
        result.append(opts)
        if option.help:
            help_lines = textwrap.wrap(option.help, self.help_width)
            result.append('%*s%s\n' % (indent_first, '', help_lines[0]))
            result.extend([ '%*s%s\n' % (self.help_position, '', line) for line in help_lines[1:] ])
        elif opts[(-1)] != '\n':
            result.append('\n')
        return ('').join(result)

    def store_option_strings(self, parser):
        self.indent()
        max_len = 0
        for opt in parser.option_list:
            strings = self.format_option_strings(opt)
            opt.option_strings = strings
            max_len = max(max_len, len(strings) + self.current_indent)

        self.indent()
        for group in parser.option_groups:
            for opt in group.option_list:
                strings = self.format_option_strings(opt)
                opt.option_strings = strings
                max_len = max(max_len, len(strings) + self.current_indent)

        self.dedent()
        self.dedent()
        self.help_position = min(max_len + 2, self.max_help_position)

    def format_option_strings(self, option):
        """Return a comma-separated list of option strings & metavariables."""
        if option.takes_value():
            metavar = option.metavar or option.dest.upper()
            short_opts = [ sopt + metavar for sopt in option._short_opts ]
            long_opts = [ lopt + '=' + metavar for lopt in option._long_opts ]
        else:
            short_opts = option._short_opts
            long_opts = option._long_opts
        if self.short_first:
            opts = short_opts + long_opts
        else:
            opts = long_opts + short_opts
        return (', ').join(opts)


class IndentedHelpFormatter(HelpFormatter):
    """Format help with indented section bodies.
    """
    __module__ = __name__

    def __init__(self, indent_increment=2, max_help_position=24, width=79, short_first=1):
        HelpFormatter.__init__(self, indent_increment, max_help_position, width, short_first)

    def format_usage(self, usage):
        return 'usage: %s\n' % usage

    def format_heading(self, heading):
        return '%*s%s:\n' % (self.current_indent, '', heading)


class TitledHelpFormatter(HelpFormatter):
    """Format help with underlined section headers.
    """
    __module__ = __name__

    def __init__(self, indent_increment=0, max_help_position=24, width=79, short_first=0):
        HelpFormatter.__init__(self, indent_increment, max_help_position, width, short_first)

    def format_usage(self, usage):
        return '%s  %s\n' % (self.format_heading('Usage'), usage)

    def format_heading(self, heading):
        return '%s\n%s\n' % (heading, '=-'[self.level] * len(heading))


_builtin_cvt = {'int': (int, 'integer'), 'long': (long, 'long integer'), 'float': (float, 'floating-point'), 'complex': (complex, 'complex')}

def check_builtin(option, opt, value):
    (cvt, what) = _builtin_cvt[option.type]
    try:
        return cvt(value)
    except ValueError:
        raise OptionValueError('option %s: invalid %s value: %r' % (opt, what, value))


def check_choice(option, opt, value):
    if value in option.choices:
        return value
    else:
        choices = (', ').join(map(repr, option.choices))
        raise OptionValueError('option %s: invalid choice: %r (choose from %s)' % (opt, value, choices))


NO_DEFAULT = 'NO' + 'DEFAULT'

class Option:
    """
    Instance attributes:
      _short_opts : [string]
      _long_opts : [string]

      action : string
      type : string
      dest : string
      default : any
      nargs : int
      const : any
      choices : [string]
      callback : function
      callback_args : (any*)
      callback_kwargs : { string : any }
      help : string
      metavar : string
    """
    __module__ = __name__
    ATTRS = [
     'action', 'type', 'dest', 'default', 'nargs', 'const', 'choices', 'callback', 'callback_args', 'callback_kwargs', 'help', 'metavar']
    ACTIONS = (
     'store', 'store_const', 'store_true', 'store_false', 'append', 'count', 'callback', 'help', 'version')
    STORE_ACTIONS = (
     'store', 'store_const', 'store_true', 'store_false', 'append', 'count')
    TYPED_ACTIONS = (
     'store', 'append', 'callback')
    TYPES = (
     'string', 'int', 'long', 'float', 'complex', 'choice')
    TYPE_CHECKER = {'int': check_builtin, 'long': check_builtin, 'float': check_builtin, 'complex': check_builtin, 'choice': check_choice}
    CHECK_METHODS = None

    def __init__(self, *opts, **attrs):
        self._short_opts = []
        self._long_opts = []
        opts = self._check_opt_strings(opts)
        self._set_opt_strings(opts)
        self._set_attrs(attrs)
        for checker in self.CHECK_METHODS:
            checker(self)

    def _check_opt_strings(self, opts):
        opts = filter(None, opts)
        if not opts:
            raise TypeError('at least one option string must be supplied')
        return opts
        return

    def _set_opt_strings(self, opts):
        for opt in opts:
            if len(opt) < 2:
                raise OptionError('invalid option string %r: must be at least two characters long' % opt, self)
            elif len(opt) == 2:
                if not (opt[0] == '-' and opt[1] != '-'):
                    raise OptionError('invalid short option string %r: must be of the form -x, (x any non-dash char)' % opt, self)
                self._short_opts.append(opt)
            else:
                if not (opt[0:2] == '--' and opt[2] != '-'):
                    raise OptionError('invalid long option string %r: must start with --, followed by non-dash' % opt, self)
                self._long_opts.append(opt)

    def _set_attrs(self, attrs):
        for attr in self.ATTRS:
            if attrs.has_key(attr):
                setattr(self, attr, attrs[attr])
                del attrs[attr]
            elif attr == 'default':
                setattr(self, attr, NO_DEFAULT)
            else:
                setattr(self, attr, None)

        if attrs:
            raise OptionError('invalid keyword arguments: %s' % (', ').join(attrs.keys()), self)
        return

    def _check_action(self):
        if self.action is None:
            self.action = 'store'
        elif self.action not in self.ACTIONS:
            raise OptionError('invalid action: %r' % self.action, self)
        return

    def _check_type(self):
        if self.type is None:
            if self.action in ('store', 'append'):
                if self.choices is not None:
                    self.type = 'choice'
                else:
                    self.type = 'string'
        else:
            if self.type not in self.TYPES:
                raise OptionError('invalid option type: %r' % self.type, self)
            if self.action not in self.TYPED_ACTIONS:
                raise OptionError('must not supply a type for action %r' % self.action, self)
        return

    def _check_choice(self):
        if self.type == 'choice':
            if self.choices is None:
                raise OptionError("must supply a list of choices for type 'choice'", self)
            elif type(self.choices) not in (types.TupleType, types.ListType):
                raise OptionError("choices must be a list of strings ('%s' supplied)" % str(type(self.choices)).split("'")[1], self)
        elif self.choices is not None:
            raise OptionError('must not supply choices for type %r' % self.type, self)
        return

    def _check_dest(self):
        if self.action in self.STORE_ACTIONS and self.dest is None:
            if self._long_opts:
                self.dest = self._long_opts[0][2:].replace('-', '_')
            else:
                self.dest = self._short_opts[0][1]
        return

    def _check_const(self):
        if self.action != 'store_const' and self.const is not None:
            raise OptionError("'const' must not be supplied for action %r" % self.action, self)
        return

    def _check_nargs(self):
        if self.action in self.TYPED_ACTIONS:
            if self.nargs is None:
                self.nargs = 1
        elif self.nargs is not None:
            raise OptionError("'nargs' must not be supplied for action %r" % self.action, self)
        return

    def _check_callback(self):
        if self.action == 'callback':
            if not callable(self.callback):
                raise OptionError('callback not callable: %r' % self.callback, self)
            if self.callback_args is not None and type(self.callback_args) is not types.TupleType:
                raise OptionError('callback_args, if supplied, must be a tuple: not %r' % self.callback_args, self)
            if self.callback_kwargs is not None and type(self.callback_kwargs) is not types.DictType:
                raise OptionError('callback_kwargs, if supplied, must be a dict: not %r' % self.callback_kwargs, self)
        else:
            if self.callback is not None:
                raise OptionError('callback supplied (%r) for non-callback option' % self.callback, self)
            if self.callback_args is not None:
                raise OptionError('callback_args supplied for non-callback option', self)
            if self.callback_kwargs is not None:
                raise OptionError('callback_kwargs supplied for non-callback option', self)
        return

    CHECK_METHODS = [_check_action, _check_type, _check_choice, _check_dest, _check_const, _check_nargs, _check_callback]

    def __str__(self):
        return ('/').join(self._short_opts + self._long_opts)

    def takes_value(self):
        return self.type is not None
        return

    def check_value(self, opt, value):
        checker = self.TYPE_CHECKER.get(self.type)
        if checker is None:
            return value
        else:
            return checker(self, opt, value)
        return

    def process(self, opt, value, values, parser):
        if value is not None:
            if self.nargs == 1:
                value = self.check_value(opt, value)
            else:
                value = tuple([ self.check_value(opt, v) for v in value ])
        return self.take_action(self.action, self.dest, opt, value, values, parser)
        return

    def take_action(self, action, dest, opt, value, values, parser):
        if action == 'store':
            setattr(values, dest, value)
        elif action == 'store_const':
            setattr(values, dest, self.const)
        elif action == 'store_true':
            setattr(values, dest, True)
        elif action == 'store_false':
            setattr(values, dest, False)
        elif action == 'append':
            values.ensure_value(dest, []).append(value)
        elif action == 'count':
            setattr(values, dest, values.ensure_value(dest, 0) + 1)
        elif action == 'callback':
            args = self.callback_args or ()
            kwargs = self.callback_kwargs or {}
            self.callback(self, opt, value, parser, *args, **kwargs)
        elif action == 'help':
            parser.print_help()
            sys.exit(0)
        elif action == 'version':
            parser.print_version()
            sys.exit(0)
        else:
            raise RuntimeError, 'unknown action %r' % self.action
        return 1


def get_prog_name():
    return os.path.basename(sys.argv[0])


SUPPRESS_HELP = 'SUPPRESS' + 'HELP'
SUPPRESS_USAGE = 'SUPPRESS' + 'USAGE'
STD_HELP_OPTION = Option('-h', '--help', action='help', help='show this help message and exit')
STD_VERSION_OPTION = Option('--version', action='version', help="show program's version number and exit")

class Values:
    __module__ = __name__

    def __init__(self, defaults=None):
        if defaults:
            for (attr, val) in defaults.items():
                setattr(self, attr, val)

    def __repr__(self):
        return '<%s at 0x%x: %r>' % (self.__class__.__name__, id(self), self.__dict__)

    def _update_careful(self, dict):
        """
        Update the option values from an arbitrary dictionary, but only
        use keys from dict that already have a corresponding attribute
        in self.  Any keys in dict without a corresponding attribute
        are silently ignored.
        """
        for attr in dir(self):
            if dict.has_key(attr):
                dval = dict[attr]
                if dval is not None:
                    setattr(self, attr, dval)

        return

    def _update_loose(self, dict):
        """
        Update the option values from an arbitrary dictionary,
        using all keys from the dictionary regardless of whether
        they have a corresponding attribute in self or not.
        """
        self.__dict__.update(dict)

    def _update(self, dict, mode):
        if mode == 'careful':
            self._update_careful(dict)
        elif mode == 'loose':
            self._update_loose(dict)
        else:
            raise ValueError, 'invalid update mode: %r' % mode

    def read_module(self, modname, mode='careful'):
        __import__(modname)
        mod = sys.modules[modname]
        self._update(vars(mod), mode)

    def read_file(self, filename, mode='careful'):
        vars = {}
        execfile(filename, vars)
        self._update(vars, mode)

    def ensure_value(self, attr, value):
        if not hasattr(self, attr) or getattr(self, attr) is None:
            setattr(self, attr, value)
        return getattr(self, attr)
        return


class OptionContainer:
    """
    Abstract base class.

    Class attributes:
      standard_option_list : [Option]
        list of standard options that will be accepted by all instances
        of this parser class (intended to be overridden by subclasses).

    Instance attributes:
      option_list : [Option]
        the list of Option objects contained by this OptionContainer
      _short_opt : { string : Option }
        dictionary mapping short option strings, eg. "-f" or "-X",
        to the Option instances that implement them.  If an Option
        has multiple short option strings, it will appears in this
        dictionary multiple times. [1]
      _long_opt : { string : Option }
        dictionary mapping long option strings, eg. "--file" or
        "--exclude", to the Option instances that implement them.
        Again, a given Option can occur multiple times in this
        dictionary. [1]
      defaults : { string : any }
        dictionary mapping option destination names to default
        values for each destination [1]

    [1] These mappings are common to (shared by) all components of the
        controlling OptionParser, where they are initially created.

    """
    __module__ = __name__

    def __init__(self, option_class, conflict_handler, description):
        self._create_option_list()
        self.option_class = option_class
        self.set_conflict_handler(conflict_handler)
        self.set_description(description)

    def _create_option_mappings(self):
        self._short_opt = {}
        self._long_opt = {}
        self.defaults = {}

    def _share_option_mappings(self, parser):
        self._short_opt = parser._short_opt
        self._long_opt = parser._long_opt
        self.defaults = parser.defaults

    def set_conflict_handler(self, handler):
        if handler not in ('ignore', 'error', 'resolve'):
            raise ValueError, 'invalid conflict_resolution value %r' % handler
        self.conflict_handler = handler

    def set_description(self, description):
        self.description = description

    def _check_conflict(self, option):
        conflict_opts = []
        for opt in option._short_opts:
            if self._short_opt.has_key(opt):
                conflict_opts.append((opt, self._short_opt[opt]))

        for opt in option._long_opts:
            if self._long_opt.has_key(opt):
                conflict_opts.append((opt, self._long_opt[opt]))

        if conflict_opts:
            handler = self.conflict_handler
            if handler == 'ignore':
                pass
            elif handler == 'error':
                raise OptionConflictError('conflicting option string(s): %s' % (', ').join([ co[0] for co in conflict_opts ]), option)
            elif handler == 'resolve':
                for (opt, c_option) in conflict_opts:
                    if opt.startswith('--'):
                        c_option._long_opts.remove(opt)
                        del self._long_opt[opt]
                    else:
                        c_option._short_opts.remove(opt)
                        del self._short_opt[opt]
                    if not (c_option._short_opts or c_option._long_opts):
                        c_option.container.option_list.remove(c_option)

    def add_option(self, *args, **kwargs):
        """add_option(Option)
           add_option(opt_str, ..., kwarg=val, ...)
        """
        if type(args[0]) is types.StringType:
            option = self.option_class(*args, **kwargs)
        elif len(args) == 1 and not kwargs:
            option = args[0]
            if not isinstance(option, Option):
                raise TypeError, 'not an Option instance: %r' % option
        else:
            raise TypeError, 'invalid arguments'
        self._check_conflict(option)
        self.option_list.append(option)
        option.container = self
        for opt in option._short_opts:
            self._short_opt[opt] = option

        for opt in option._long_opts:
            self._long_opt[opt] = option

        if option.dest is not None:
            if option.default is not NO_DEFAULT:
                self.defaults[option.dest] = option.default
            elif not self.defaults.has_key(option.dest):
                self.defaults[option.dest] = None
        return option
        return

    def add_options(self, option_list):
        for option in option_list:
            self.add_option(option)

    def get_option(self, opt_str):
        return self._short_opt.get(opt_str) or self._long_opt.get(opt_str)

    def has_option(self, opt_str):
        return self._short_opt.has_key(opt_str) or self._long_opt.has_key(opt_str)

    def remove_option(self, opt_str):
        option = self._short_opt.get(opt_str)
        if option is None:
            option = self._long_opt.get(opt_str)
        if option is None:
            raise ValueError('no such option %r' % opt_str)
        for opt in option._short_opts:
            del self._short_opt[opt]

        for opt in option._long_opts:
            del self._long_opt[opt]

        option.container.option_list.remove(option)
        return

    def format_option_help(self, formatter):
        if not self.option_list:
            return ''
        result = []
        for option in self.option_list:
            if not option.help is SUPPRESS_HELP:
                result.append(formatter.format_option(option))

        return ('').join(result)

    def format_description(self, formatter):
        if self.description:
            return formatter.format_description(self.description)
        else:
            return ''

    def format_help(self, formatter):
        if self.description:
            desc = self.format_description(formatter) + '\n'
        else:
            desc = ''
        return desc + self.format_option_help(formatter)


class OptionGroup(OptionContainer):
    __module__ = __name__

    def __init__(self, parser, title, description=None):
        self.parser = parser
        OptionContainer.__init__(self, parser.option_class, parser.conflict_handler, description)
        self.title = title

    def _create_option_list(self):
        self.option_list = []
        self._share_option_mappings(self.parser)

    def set_title(self, title):
        self.title = title

    def format_help(self, formatter):
        result = formatter.format_heading(self.title)
        formatter.indent()
        result += OptionContainer.format_help(self, formatter)
        formatter.dedent()
        return result


class OptionParser(OptionContainer):
    """
    Class attributes:
      standard_option_list : [Option]
        list of standard options that will be accepted by all instances
        of this parser class (intended to be overridden by subclasses).

    Instance attributes:
      usage : string
        a usage string for your program.  Before it is displayed
        to the user, "%prog" will be expanded to the name of
        your program (self.prog or os.path.basename(sys.argv[0])).
      prog : string
        the name of the current program (to override
        os.path.basename(sys.argv[0])).

      allow_interspersed_args : boolean = true
        if true, positional arguments may be interspersed with options.
        Assuming -a and -b each take a single argument, the command-line
          -ablah foo bar -bboo baz
        will be interpreted the same as
          -ablah -bboo -- foo bar baz
        If this flag were false, that command line would be interpreted as
          -ablah -- foo bar -bboo baz
        -- ie. we stop processing options as soon as we see the first
        non-option argument.  (This is the tradition followed by
        Python's getopt module, Perl's Getopt::Std, and other argument-
        parsing libraries, but it is generally annoying to users.)

      rargs : [string]
        the argument list currently being parsed.  Only set when
        parse_args() is active, and continually trimmed down as
        we consume arguments.  Mainly there for the benefit of
        callback options.
      largs : [string]
        the list of leftover arguments that we have skipped while
        parsing options.  If allow_interspersed_args is false, this
        list is always empty.
      values : Values
        the set of option values currently being accumulated.  Only
        set when parse_args() is active.  Also mainly for callbacks.

    Because of the 'rargs', 'largs', and 'values' attributes,
    OptionParser is not thread-safe.  If, for some perverse reason, you
    need to parse command-line arguments simultaneously in different
    threads, use different OptionParser instances.

    """
    __module__ = __name__
    standard_option_list = []

    def __init__(self, usage=None, option_list=None, option_class=Option, version=None, conflict_handler='error', description=None, formatter=None, add_help_option=1, prog=None):
        OptionContainer.__init__(self, option_class, conflict_handler, description)
        self.set_usage(usage)
        self.prog = prog
        self.version = version
        self.allow_interspersed_args = 1
        if formatter is None:
            formatter = IndentedHelpFormatter()
        self.formatter = formatter
        self._populate_option_list(option_list, add_help=add_help_option)
        self._init_parsing_state()
        return

    def _create_option_list(self):
        self.option_list = []
        self.option_groups = []
        self._create_option_mappings()

    def _populate_option_list(self, option_list, add_help=1):
        if self.standard_option_list:
            self.add_options(self.standard_option_list)
        if option_list:
            self.add_options(option_list)
        if self.version:
            self.add_option(STD_VERSION_OPTION)
        if add_help:
            self.add_option(STD_HELP_OPTION)

    def _init_parsing_state(self):
        self.rargs = None
        self.largs = None
        self.values = None
        return

    def _get_prog_name(self):
        if self.prog:
            return self.prog
        else:
            return get_prog_name()

    def set_usage(self, usage):
        if usage is None:
            self.usage = '%prog [options]'
        elif usage is SUPPRESS_USAGE:
            self.usage = None
        elif usage.startswith('usage: '):
            self.usage = usage[7:]
        else:
            self.usage = usage
        return

    def enable_interspersed_args(self):
        self.allow_interspersed_args = 1

    def disable_interspersed_args(self):
        self.allow_interspersed_args = 0

    def set_default(self, dest, value):
        self.defaults[dest] = value

    def set_defaults(self, **kwargs):
        self.defaults.update(kwargs)

    def get_default_values(self):
        return Values(self.defaults)

    def add_option_group(self, *args, **kwargs):
        if type(args[0]) is types.StringType:
            group = OptionGroup(self, *args, **kwargs)
        elif len(args) == 1 and not kwargs:
            group = args[0]
            if not isinstance(group, OptionGroup):
                raise TypeError, 'not an OptionGroup instance: %r' % group
            if group.parser is not self:
                raise ValueError, 'invalid OptionGroup (wrong parser)'
        else:
            raise TypeError, 'invalid arguments'
        self.option_groups.append(group)
        return group

    def get_option_group(self, opt_str):
        option = self._short_opt.get(opt_str) or self._long_opt.get(opt_str)
        if option and option.container is not self:
            return option.container
        return None
        return

    def _get_args(self, args):
        if args is None:
            return sys.argv[1:]
        else:
            return args[:]
        return

    def parse_args(self, args=None, values=None):
        """
        parse_args(args : [string] = sys.argv[1:],
                   values : Values = None)
        -> (values : Values, args : [string])

        Parse the command-line options found in 'args' (default:
        sys.argv[1:]).  Any errors result in a call to 'error()', which
        by default prints the usage message to stderr and calls
        sys.exit() with an error message.  On success returns a pair
        (values, args) where 'values' is an Values instance (with all
        your option values) and 'args' is the list of arguments left
        over after parsing options.
        """
        rargs = self._get_args(args)
        if values is None:
            values = self.get_default_values()
        self.rargs = rargs
        self.largs = largs = []
        self.values = values
        try:
            stop = self._process_args(largs, rargs, values)
        except (BadOptionError, OptionValueError), err:
            self.error(err.msg)

        args = largs + rargs
        return self.check_values(values, args)
        return

    def check_values(self, values, args):
        """
        check_values(values : Values, args : [string])
        -> (values : Values, args : [string])

        Check that the supplied option values and leftover arguments are
        valid.  Returns the option values and leftover arguments
        (possibly adjusted, possibly completely new -- whatever you
        like).  Default implementation just returns the passed-in
        values; subclasses may override as desired.
        """
        return (
         values, args)

    def _process_args(self, largs, rargs, values):
        """_process_args(largs : [string],
                         rargs : [string],
                         values : Values)

        Process command-line arguments and populate 'values', consuming
        options and arguments from 'rargs'.  If 'allow_interspersed_args' is
        false, stop at the first non-option argument.  If true, accumulate any
        interspersed non-option arguments in 'largs'.
        """
        while rargs:
            arg = rargs[0]
            if arg == '--':
                del rargs[0]
                return
            elif arg[0:2] == '--':
                self._process_long_opt(rargs, values)
            elif arg[:1] == '-' and len(arg) > 1:
                self._process_short_opts(rargs, values)
            elif self.allow_interspersed_args:
                largs.append(arg)
                del rargs[0]
            else:
                return

    def _match_long_opt(self, opt):
        """_match_long_opt(opt : string) -> string

        Determine which long option string 'opt' matches, ie. which one
        it is an unambiguous abbrevation for.  Raises BadOptionError if
        'opt' doesn't unambiguously match any long option string.
        """
        return _match_abbrev(opt, self._long_opt)

    def _process_long_opt(self, rargs, values):
        arg = rargs.pop(0)
        if '=' in arg:
            (opt, next_arg) = arg.split('=', 1)
            rargs.insert(0, next_arg)
            had_explicit_value = 1
        else:
            opt = arg
            had_explicit_value = 0
        opt = self._match_long_opt(opt)
        option = self._long_opt[opt]
        if option.takes_value():
            nargs = option.nargs
            if len(rargs) < nargs:
                if nargs == 1:
                    self.error('%s option requires a value' % opt)
                else:
                    self.error('%s option requires %d values' % (opt, nargs))
            elif nargs == 1:
                value = rargs.pop(0)
            else:
                value = tuple(rargs[0:nargs])
                del rargs[0:nargs]
        elif had_explicit_value:
            self.error('%s option does not take a value' % opt)
        else:
            value = None
        option.process(opt, value, values, self)
        return

    def _process_short_opts(self, rargs, values):
        arg = rargs.pop(0)
        stop = 0
        i = 1
        for ch in arg[1:]:
            opt = '-' + ch
            option = self._short_opt.get(opt)
            i += 1
            if not option:
                self.error('no such option: %s' % opt)
            if option.takes_value():
                if i < len(arg):
                    rargs.insert(0, arg[i:])
                    stop = 1
                nargs = option.nargs
                if len(rargs) < nargs:
                    if nargs == 1:
                        self.error('%s option requires a value' % opt)
                    else:
                        self.error('%s option requires %s values' % (opt, nargs))
                elif nargs == 1:
                    value = rargs.pop(0)
                else:
                    value = tuple(rargs[0:nargs])
                    del rargs[0:nargs]
            else:
                value = None
            option.process(opt, value, values, self)
            if stop:
                break

        return

    def error(self, msg):
        """error(msg : string)

        Print a usage message incorporating 'msg' to stderr and exit.
        If you override this in a subclass, it should not return -- it
        should either exit or raise an exception.
        """
        self.print_usage(sys.stderr)
        sys.exit('%s: error: %s' % (self._get_prog_name(), msg))

    def get_usage(self):
        if self.usage:
            return self.formatter.format_usage(self.usage.replace('%prog', self._get_prog_name()))
        else:
            return ''

    def print_usage(self, file=None):
        """print_usage(file : file = stdout)

        Print the usage message for the current program (self.usage) to
        'file' (default stdout).  Any occurence of the string "%prog" in
        self.usage is replaced with the name of the current program
        (basename of sys.argv[0]).  Does nothing if self.usage is empty
        or not defined.
        """
        if self.usage:
            print >> file, self.get_usage()

    def get_version(self):
        if self.version:
            return self.version.replace('%prog', self._get_prog_name())
        else:
            return ''

    def print_version(self, file=None):
        """print_version(file : file = stdout)

        Print the version message for this program (self.version) to
        'file' (default stdout).  As with print_usage(), any occurence
        of "%prog" in self.version is replaced by the current program's
        name.  Does nothing if self.version is empty or undefined.
        """
        if self.version:
            print >> file, self.get_version()

    def format_option_help(self, formatter=None):
        if formatter is None:
            formatter = self.formatter
        formatter.store_option_strings(self)
        result = []
        result.append(formatter.format_heading('options'))
        formatter.indent()
        if self.option_list:
            result.append(OptionContainer.format_option_help(self, formatter))
            result.append('\n')
        for group in self.option_groups:
            result.append(group.format_help(formatter))
            result.append('\n')

        formatter.dedent()
        return ('').join(result[:-1])
        return

    def format_help(self, formatter=None):
        if formatter is None:
            formatter = self.formatter
        result = []
        if self.usage:
            result.append(self.get_usage() + '\n')
        if self.description:
            result.append(self.format_description(formatter) + '\n')
        result.append(self.format_option_help(formatter))
        return ('').join(result)
        return

    def print_help(self, file=None):
        """print_help(file : file = stdout)

        Print an extended help message, listing all options and any
        help text provided with them, to 'file' (default stdout).
        """
        if file is None:
            file = sys.stdout
        file.write(self.format_help())
        return


def _match_abbrev(s, wordmap):
    """_match_abbrev(s : string, wordmap : {string : Option}) -> string

    Return the string key in 'wordmap' for which 's' is an unambiguous
    abbreviation.  If 's' is found to be ambiguous or doesn't match any of
    'words', raise BadOptionError.
    """
    if wordmap.has_key(s):
        return s
    else:
        possibilities = [ word for word in wordmap.keys() if word.startswith(s) ]
        if len(possibilities) == 1:
            return possibilities[0]
        elif not possibilities:
            raise BadOptionError('no such option: %s' % s)
        else:
            raise BadOptionError('ambiguous option: %s (%s?)' % (s, (', ').join(possibilities)))


make_option = Option