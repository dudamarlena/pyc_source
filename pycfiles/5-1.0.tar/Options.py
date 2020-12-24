# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\CommandLine\Options.py
# Compiled at: 2005-04-13 18:41:04
__doc__ = '\nClasses that support advanced option processing for command-line scripts\n\nCopyright 2004 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
from distutils.fancy_getopt import wrap_text
from Ft.Lib.CommandLine import CommandLineUtil, CONSOLE_WIDTH

class Options(list):
    """
    A set of options that are available to be used in an invocation of a
    command-line script, plus related functions.
    """
    __module__ = __name__

    def __init__(self, options=None):
        if options is None:
            options = ()
        list.__init__(self, options)
        shorts = []
        longs = []
        for opt in options:
            if not isinstance(opt, BaseOption):
                raise TypeError('Option %s is not of BaseOption' % opt)
            (short, long) = opt.getForGetOpt({}, {})
            for s in short:
                if s != ':' and s in shorts:
                    raise Exception('Duplicate short option in %s' % str(self))
                shorts.append(s)

            for l in long:
                if l in longs:
                    raise Exception('Duplicate long option in %s' % str(self))
                longs.append(l)

        return

    def findMaxOption(self, level=0):
        max_opt = 0
        for option in self:
            l = option.displayLength()
            l = l + 2 * level
            if hasattr(option, 'subOptions'):
                sublen = option.subOptions.findMaxOption(level + 1)
                if sublen > l:
                    l = sublen
            if l > max_opt:
                max_opt = l

        return max_opt

    def generate_help(self, level=1, max_opt=0):
        """Generate help text (a list of strings, one per suggested line of
        output) from the option table for this FancyGetopt object.
        """
        if max_opt > 0:
            opt_width = max_opt - 2 * (level - 1)
        else:
            opt_width = max_opt = self.findMaxOption()
        col_width = 2 * level + 4 + 2 + max_opt + 2 + 2
        line_width = CONSOLE_WIDTH
        text_width = line_width - col_width
        indent = '  ' * level
        big_indent = ' ' * col_width
        lines = []
        for option in self:
            if isinstance(option, ExclusiveOptions):
                lines.extend(option.choices.generate_help(level, max_opt))
                continue
            text = wrap_text(option.description, text_width)
            short_opt = option.shortName
            if option.takesArg:
                long_opt = '%s=<%s>' % (option.longName, option.argName)
            else:
                long_opt = option.longName
            if option.shortName:
                short_part = '-%s' % short_opt
            else:
                short_part = '  '
            if option.shortName and option.longName:
                short_part += ', '
            else:
                short_part += '  '
            long_part = '--%-*s' % (opt_width, long_opt)
            if text:
                lines.append('%s%s%s  %s' % (indent, short_part, long_part, text[0]))
            else:
                lines.append('%s%s%s' % (indent, short_part, long_part))
            for line in text[1:]:
                lines.append(big_indent + line)

            if isinstance(option, TypedOption):
                for (val, desc) in option.allowed:
                    text = wrap_text(desc, text_width)
                    lines.append('%s    %-*s%s' % (indent, opt_width, val, text[0]))
                    for line in text[1:]:
                        lines.append(big_indent + line)

            if hasattr(option, 'subOptions'):
                lines.extend(option.subOptions.generate_help(level + 1, max_opt))

        return lines


class BaseOption:
    """
    An option that is available to be used in an invocation of a
    command-line script, plus related functions.
    """
    __module__ = __name__
    multiple = False

    def validate(self):
        return

    def getForGetOpt(self, short2long, takes_arg):
        raise NotImplementedError('subclass must override')

    def displayLength(self):
        raise NotImplementedError('subclass %s must override' % self.__class__)

    def gen_command_line(self):
        raise NotImplementedError('subclass %s must override' % self.__class__)

    def gen_description(self):
        raise NotImplementedError('subclass %s must override' % self.__class__)

    def apply_options(self, options):
        raise NotImplementedError('subclass %s must override' % self.__class__)

    def isApplied(self):
        raise NotImplementedError('subclass %s must override' % self.__class__)

    def getName(self):
        raise NotImplementedError('subclass %s must override' % self.__class__)

    def __str__(self):
        return self.gen_command_line()

    __repr__ = __str__


class Option(BaseOption):
    __module__ = __name__

    def __init__(self, shortName, longName, description, subOptions=None, multiple=False):
        if len(longName) < 2:
            raise SyntaxError('invalid long option: ' + longName)
        if shortName is not None and len(shortName) != 1:
            raise SyntaxError('invalid short option: ' + shortName)
        self.shortName = shortName or ''
        i = longName.find('=')
        if i > 0:
            self.takesArg = 1
            argName = longName[i + 1:]
            longName = longName[:i]
            self.argName = argName or longName
        else:
            self.takesArg = 0
        self.longName = longName
        self.description = description
        if not isinstance(subOptions, Options):
            subOptions = Options(subOptions)
        self.subOptions = subOptions
        self.multiple = multiple
        return

    def getForGetOpt(self, short2long, takes_arg):
        short_opts = self.shortName
        if self.takesArg:
            if short_opts:
                short_opts = short_opts + ':'
            long_opts = [
             self.longName + '=']
        else:
            long_opts = [
             self.longName]
        takes_arg[self.longName] = self.takesArg
        if self.shortName:
            short2long[self.shortName] = self.longName
        for option in self.subOptions:
            (short, long) = option.getForGetOpt(short2long, takes_arg)
            short_opts = short_opts + short
            long_opts.extend(long)

        return (
         short_opts, long_opts)

    def displayLength(self):
        l = len(self.longName)
        if self.takesArg:
            l = l + 1 + len(self.argName)
        return l

    def validate(self):
        for option in self.subOptions:
            option.validate()

        for option in self.subOptions:
            if option.isApplied() and not self.applied:
                raise CommandLineUtil.ArgumentError('%s specified without %s' % (option.getName(), self.longName))

        return

    def apply_options(self, options):
        self.applied = options.has_key(self.longName)
        for option in self.subOptions:
            option.apply_options(options)

        return

    def isApplied(self):
        return self.applied

    def getName(self):
        return self.longName

    def gen_command_line(self):
        cl = '[--%s' % self.longName
        if self.takesArg:
            cl = cl + '=<%s>' % self.argName
        if self.subOptions:
            sub = map(lambda s: s.gen_command_line(), self.subOptions)
            if len(sub) > 1:
                cl = cl + ' [%s]' % (' ').join(sub)
            else:
                cl = cl + ' ' + sub[0]
        return cl + ']'


class TypedOption(Option):
    __module__ = __name__

    def __init__(self, shortName, longName, description, allowed, subOptions=None):
        Option.__init__(self, shortName, longName, description, subOptions)
        self.allowedValues = map(lambda (value, desc): value, allowed)
        self.allowed = allowed

    def apply_options(self, options):
        self.applied = options.get(self.longName)
        for option in self.subOptions:
            option.apply_options(options)

        return

    def validate(self):
        if self.applied and self.applied not in self.allowedValues:
            expected = (', ').join(self.allowedValues)
            raise SyntaxError('option %s: expected %s, got %s' % (self.longName, expected, self.applied))
        Option.validate(self)
        return

    def gen_command_line(self):
        sub = ''
        for option in self.subOptions:
            sub = sub + '%s ' % option.gen_command_line()

        av = '['
        for a in self.allowedValues:
            av = av + a
            if a != self.allowedValues[(-1)]:
                av = av + '|'

        av = av + ']'
        if sub:
            return '[--%s=%s [%s]]' % (self.longName, av, sub)
        else:
            return '[--%s=%s]' % (self.longName, av)


class ExclusiveOptions(BaseOption):
    __module__ = __name__

    def __init__(self, choices):
        if not isinstance(choices, Options):
            choices = Options(choices)
        self.choices = choices

    def getForGetOpt(self, short2long, takes_arg):
        short_opts = ''
        long_opts = []
        for option in self.choices:
            (short, long) = option.getForGetOpt(short2long, takes_arg)
            short_opts = short_opts + short
            long_opts.extend(long)

        return (
         short_opts, long_opts)

    def displayLength(self):
        return self.choices.findMaxOption()

    def validate(self):
        applied = 0
        for opt in self.choices:
            if opt.isApplied():
                if applied:
                    opts = (', ').join(map(lambda x: '--%s' % x.getName(), self.choices))
                    raise CommandLineUtil.ArgumentError('Only one of %s allowed' % opts)
                applied = opt

        if applied:
            applied.validate()
        for option in self.choices:
            option.validate()

    def apply_options(self, options):
        for option in self.choices:
            option.apply_options(options)

        return

    def isApplied(self):
        for option in self.choices:
            if option.isApplied():
                return 1

        return 0

    def getName(self):
        return '(%s)' % (', ').join(map(lambda x: '--%s' % x.getName(), self.choices))

    def gen_command_line(self):
        cl = '['
        first = 1
        for c in self.choices:
            if not first:
                cl = cl + ' | '
            else:
                first = 0
            cl = cl + c.gen_command_line()

        return cl + ']'