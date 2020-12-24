# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\CommandLine\FancyGetOpt.py
# Compiled at: 2004-08-20 18:11:33
__doc__ = '\nAdvanced argument & option processing for command-line scripts\n\nCopyright 2004 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import getopt, CommandLineUtil

def FancyGetopt(cmd, option_table, args):
    """
    Parses command line options and parameter list. args is the argument list
    to be parsed, without the leading reference to the running program.
    Typically, this means "sys.argv[1:]". option_table is an instance of
    Ft.Lib.CommandLine.Options.Options. Raises an exception if args contains
    syntax errors. Returns a tuple of (options, args) where options is a
    dictionary and args is the list of args after the first arg that wasn't
    in option_table. Note the options return value is different than what
    getopt.getopt() returns.

    cmd is an Ft.Lib.CommandLine.Command instance, and is only used
    in reporting errors.
    """
    short_opts = []
    long_opts = []
    short2long = {}
    takes_arg = {}
    options = {}
    for option in option_table:
        (short, long) = option.getForGetOpt(short2long, takes_arg)
        short_opts.append(short)
        long_opts.extend(long)

    short_opts = ('').join(short_opts)
    try:
        (opts, args) = getopt.getopt(args, short_opts, long_opts)
    except getopt.error, msg:
        raise CommandLineUtil.ArgumentError(cmd, str(msg))

    for (opt, val) in opts:
        if len(opt) == 2 and opt[0] == '-':
            opt = short2long[opt[1]]
        elif len(opt) > 2 and opt[0:2] == '--':
            opt = opt[2:]
        if not takes_arg[opt]:
            val = 1
        if options.has_key(opt):
            if type(options[opt]) != type([]):
                options[opt] = [
                 options[opt]]
            options[opt].append(val)
        else:
            options[opt] = val

    return (
     options, args)