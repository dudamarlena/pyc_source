# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/cmdline.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 17398 bytes
"""
    pygments.cmdline
    ~~~~~~~~~~~~~~~~

    Command line interface.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from __future__ import print_function
import sys, getopt
from textwrap import dedent
from pygments import __version__, highlight
from pygments.util import ClassNotFound, OptionError, docstring_headline, guess_decode, guess_decode_from_terminal, terminal_encoding
from pygments.lexers import get_all_lexers, get_lexer_by_name, guess_lexer, get_lexer_for_filename, find_lexer_class_for_filename
from pygments.lexers.special import TextLexer
from pygments.formatters.latex import LatexEmbeddedLexer, LatexFormatter
from pygments.formatters import get_all_formatters, get_formatter_by_name, get_formatter_for_filename, find_formatter_class
from pygments.formatters.terminal import TerminalFormatter
from pygments.filters import get_all_filters, find_filter_class
from pygments.styles import get_all_styles, get_style_by_name
USAGE = 'Usage: %s [-l <lexer> | -g] [-F <filter>[:<options>]] [-f <formatter>]\n          [-O <options>] [-P <option=value>] [-s] [-v] [-o <outfile>] [<infile>]\n\n       %s -S <style> -f <formatter> [-a <arg>] [-O <options>] [-P <option=value>]\n       %s -L [<which> ...]\n       %s -N <filename>\n       %s -H <type> <name>\n       %s -h | -V\n\nHighlight the input file and write the result to <outfile>.\n\nIf no input file is given, use stdin, if -o is not given, use stdout.\n\nIf -s is passed, lexing will be done in "streaming" mode, reading and\nhighlighting one line at a time.  This will only work properly with\nlexers that have no constructs spanning multiple lines!\n\n<lexer> is a lexer name (query all lexer names with -L). If -l is not\ngiven, the lexer is guessed from the extension of the input file name\n(this obviously doesn\'t work if the input is stdin).  If -g is passed,\nattempt to guess the lexer from the file contents, or pass through as\nplain text if this fails (this can work for stdin).\n\nLikewise, <formatter> is a formatter name, and will be guessed from\nthe extension of the output file name. If no output file is given,\nthe terminal formatter will be used by default.\n\nWith the -O option, you can give the lexer and formatter a comma-\nseparated list of options, e.g. ``-O bg=light,python=cool``.\n\nThe -P option adds lexer and formatter options like the -O option, but\nyou can only give one option per -P. That way, the option value may\ncontain commas and equals signs, which it can\'t with -O, e.g.\n``-P "heading=Pygments, the Python highlighter".\n\nWith the -F option, you can add filters to the token stream, you can\ngive options in the same way as for -O after a colon (note: there must\nnot be spaces around the colon).\n\nThe -O, -P and -F options can be given multiple times.\n\nWith the -S option, print out style definitions for style <style>\nfor formatter <formatter>. The argument given by -a is formatter\ndependent.\n\nThe -L option lists lexers, formatters, styles or filters -- set\n`which` to the thing you want to list (e.g. "styles"), or omit it to\nlist everything.\n\nThe -N option guesses and prints out a lexer name based solely on\nthe given filename. It does not take input or highlight anything.\nIf no specific lexer can be determined "text" is returned.\n\nThe -H option prints detailed help for the object <name> of type <type>,\nwhere <type> is one of "lexer", "formatter" or "filter".\n\nThe -s option processes lines one at a time until EOF, rather than\nwaiting to process the entire file.  This only works for stdin, and\nis intended for streaming input such as you get from \'tail -f\'.\nExample usage: "tail -f sql.log | pygmentize -s -l sql"\n\nThe -v option prints a detailed traceback on unhandled exceptions,\nwhich is useful for debugging and bug reports.\n\nThe -h option prints this help.\nThe -V option prints the package version.\n'

def _parse_options(o_strs):
    opts = {}
    if not o_strs:
        return opts
    for o_str in o_strs:
        if not o_str.strip():
            pass
        else:
            o_args = o_str.split(',')
            for o_arg in o_args:
                o_arg = o_arg.strip()
                try:
                    o_key, o_val = o_arg.split('=', 1)
                    o_key = o_key.strip()
                    o_val = o_val.strip()
                except ValueError:
                    opts[o_arg] = True
                else:
                    opts[o_key] = o_val

    return opts


def _parse_filters(f_strs):
    filters = []
    if not f_strs:
        return filters
    for f_str in f_strs:
        if ':' in f_str:
            fname, fopts = f_str.split(':', 1)
            filters.append((fname, _parse_options([fopts])))
        else:
            filters.append((f_str, {}))

    return filters


def _print_help(what, name):
    try:
        if what == 'lexer':
            cls = get_lexer_by_name(name)
            print('Help on the %s lexer:' % cls.name)
            print(dedent(cls.__doc__))
        else:
            if what == 'formatter':
                cls = find_formatter_class(name)
                print('Help on the %s formatter:' % cls.name)
                print(dedent(cls.__doc__))
            elif what == 'filter':
                cls = find_filter_class(name)
                print('Help on the %s filter:' % name)
                print(dedent(cls.__doc__))
        return 0
    except (AttributeError, ValueError):
        print('%s not found!' % what, file=sys.stderr)
        return 1


def _print_list(what):
    if what == 'lexer':
        print()
        print('Lexers:')
        print('~~~~~~~')
        info = []
        for fullname, names, exts, _ in get_all_lexers():
            tup = (', '.join(names) + ':', fullname,
             exts and '(filenames ' + ', '.join(exts) + ')' or '')
            info.append(tup)

        info.sort()
        for i in info:
            print('* %s\n    %s %s' % i)

    else:
        if what == 'formatter':
            print()
            print('Formatters:')
            print('~~~~~~~~~~~')
            info = []
            for cls in get_all_formatters():
                doc = docstring_headline(cls)
                tup = (', '.join(cls.aliases) + ':', doc,
                 cls.filenames and '(filenames ' + ', '.join(cls.filenames) + ')' or '')
                info.append(tup)

            info.sort()
            for i in info:
                print('* %s\n    %s %s' % i)

        else:
            if what == 'filter':
                print()
                print('Filters:')
                print('~~~~~~~~')
                for name in get_all_filters():
                    cls = find_filter_class(name)
                    print('* ' + name + ':')
                    print('    %s' % docstring_headline(cls))

            elif what == 'style':
                print()
                print('Styles:')
                print('~~~~~~~')
                for name in get_all_styles():
                    cls = get_style_by_name(name)
                    print('* ' + name + ':')
                    print('    %s' % docstring_headline(cls))


def main_inner(popts, args, usage):
    opts = {}
    O_opts = []
    P_opts = []
    F_opts = []
    for opt, arg in popts:
        if opt == '-O':
            O_opts.append(arg)
        else:
            if opt == '-P':
                P_opts.append(arg)
            elif opt == '-F':
                F_opts.append(arg)
        opts[opt] = arg

    if opts.pop('-h', None) is not None:
        print(usage)
        return 0
    if opts.pop('-V', None) is not None:
        print('Pygments version %s, (c) 2006-2015 by Georg Brandl.' % __version__)
        return 0
    L_opt = opts.pop('-L', None)
    if L_opt is not None:
        if opts:
            print(usage, file=sys.stderr)
            return 2
        main(['', '-V'])
        if not args:
            args = [
             'lexer', 'formatter', 'filter', 'style']
        for arg in args:
            _print_list(arg.rstrip('s'))

        return 0
    H_opt = opts.pop('-H', None)
    if H_opt is not None:
        if opts or len(args) != 2:
            print(usage, file=sys.stderr)
            return 2
        what, name = args
        if what not in ('lexer', 'formatter', 'filter'):
            print(usage, file=sys.stderr)
            return 2
        return _print_help(what, name)
    parsed_opts = _parse_options(O_opts)
    opts.pop('-O', None)
    for p_opt in P_opts:
        try:
            name, value = p_opt.split('=', 1)
        except ValueError:
            parsed_opts[p_opt] = True
        else:
            parsed_opts[name] = value

    opts.pop('-P', None)
    inencoding = parsed_opts.get('inencoding', parsed_opts.get('encoding'))
    outencoding = parsed_opts.get('outencoding', parsed_opts.get('encoding'))
    infn = opts.pop('-N', None)
    if infn is not None:
        lexer = find_lexer_class_for_filename(infn)
        if lexer is None:
            lexer = TextLexer
        print(lexer.aliases[0])
        return 0
    S_opt = opts.pop('-S', None)
    a_opt = opts.pop('-a', None)
    if S_opt is not None:
        f_opt = opts.pop('-f', None)
        if not f_opt:
            print(usage, file=sys.stderr)
            return 2
        if opts or args:
            print(usage, file=sys.stderr)
            return 2
            try:
                parsed_opts['style'] = S_opt
                fmter = get_formatter_by_name(f_opt, **parsed_opts)
            except ClassNotFound as err:
                print(err, file=sys.stderr)
                return 1

            print(fmter.get_style_defs(a_opt or ''))
            return 0
    if a_opt is not None:
        print(usage, file=sys.stderr)
        return 2
    F_opts = _parse_filters(F_opts)
    opts.pop('-F', None)
    lexer = None
    lexername = opts.pop('-l', None)
    if lexername:
        try:
            lexer = get_lexer_by_name(lexername, **parsed_opts)
        except (OptionError, ClassNotFound) as err:
            print('Error:', err, file=sys.stderr)
            return 1

    code = None
    if args:
        if len(args) > 1:
            print(usage, file=sys.stderr)
            return 2
        if '-s' in opts:
            print('Error: -s option not usable when input file specified', file=sys.stderr)
            return 2
        infn = args[0]
        try:
            with open(infn, 'rb') as (infp):
                code = infp.read()
        except Exception as err:
            print('Error: cannot read infile:', err, file=sys.stderr)
            return 1

        if not inencoding:
            code, inencoding = guess_decode(code)
        if not lexer:
            try:
                lexer = get_lexer_for_filename(infn, code, **parsed_opts)
            except ClassNotFound as err:
                if '-g' in opts:
                    try:
                        lexer = guess_lexer(code, **parsed_opts)
                    except ClassNotFound:
                        lexer = TextLexer(**parsed_opts)

                else:
                    print('Error:', err, file=sys.stderr)
                    return 1
            except OptionError as err:
                print('Error:', err, file=sys.stderr)
                return 1

    else:
        if '-s' not in opts:
            if sys.version_info > (3, ):
                code = sys.stdin.buffer.read()
            else:
                code = sys.stdin.read()
            if not inencoding:
                code, inencoding = guess_decode_from_terminal(code, sys.stdin)
            if not lexer:
                try:
                    lexer = guess_lexer(code, **parsed_opts)
                except ClassNotFound:
                    lexer = TextLexer(**parsed_opts)

        else:
            if not lexer:
                print('Error: when using -s a lexer has to be selected with -l', file=sys.stderr)
                return 2
            for fname, fopts in F_opts:
                try:
                    lexer.add_filter(fname, **fopts)
                except ClassNotFound as err:
                    print('Error:', err, file=sys.stderr)
                    return 1

            outfn = opts.pop('-o', None)
            fmter = opts.pop('-f', None)
    if fmter:
        try:
            fmter = get_formatter_by_name(fmter, **parsed_opts)
        except (OptionError, ClassNotFound) as err:
            print('Error:', err, file=sys.stderr)
            return 1

    if outfn:
        if not fmter:
            try:
                fmter = get_formatter_for_filename(outfn, **parsed_opts)
            except (OptionError, ClassNotFound) as err:
                print('Error:', err, file=sys.stderr)
                return 1

            try:
                outfile = open(outfn, 'wb')
            except Exception as err:
                print('Error: cannot open outfile:', err, file=sys.stderr)
                return 1

    else:
        if not fmter:
            fmter = TerminalFormatter(**parsed_opts)
        if sys.version_info > (3, ):
            outfile = sys.stdout.buffer
        else:
            outfile = sys.stdout
        if not outencoding:
            if outfn:
                fmter.encoding = inencoding
            else:
                fmter.encoding = terminal_encoding(sys.stdout)
            if not outfn and sys.platform in ('win32', 'cygwin') and fmter.name in ('Terminal',
                                                                                    'Terminal256'):
                if sys.version_info > (3, ):
                    from pygments.util import UnclosingTextIOWrapper
                    outfile = UnclosingTextIOWrapper(outfile, encoding=fmter.encoding)
                    fmter.encoding = None
                try:
                    import colorama.initialise
                except ImportError:
                    pass
                else:
                    outfile = colorama.initialise.wrap_stream(outfile, convert=None, strip=None, autoreset=False, wrap=True)
                escapeinside = parsed_opts.get('escapeinside', '')
    if len(escapeinside) == 2 and isinstance(fmter, LatexFormatter):
        left = escapeinside[0]
        right = escapeinside[1]
        lexer = LatexEmbeddedLexer(left, right, lexer)
    if '-s' not in opts:
        highlight(code, lexer, fmter, outfile)
        return 0
    try:
        while 1:
            if sys.version_info > (3, ):
                line = sys.stdin.buffer.readline()
            else:
                line = sys.stdin.readline()
            if not line:
                break
            if not inencoding:
                line = guess_decode_from_terminal(line, sys.stdin)[0]
            highlight(line, lexer, fmter, outfile)
            if hasattr(outfile, 'flush'):
                outfile.flush()

        return 0
    except KeyboardInterrupt:
        return 0


def main(args=sys.argv):
    """
    Main command line entry point.
    """
    usage = USAGE % ((args[0],) * 6)
    try:
        popts, args = getopt.getopt(args[1:], 'l:f:F:o:O:P:LS:a:N:vhVHgs')
    except getopt.GetoptError:
        print(usage, file=sys.stderr)
        return 2

    try:
        return main_inner(popts, args, usage)
    except Exception:
        if '-v' in dict(popts):
            print(file=sys.stderr)
            print('*' * 65, file=sys.stderr)
            print('An unhandled exception occurred while highlighting.', file=sys.stderr)
            print('Please report the whole traceback to the issue tracker at', file=sys.stderr)
            print('<https://bitbucket.org/birkenfeld/pygments-main/issues>.', file=sys.stderr)
            print('*' * 65, file=sys.stderr)
            print(file=sys.stderr)
            raise
        import traceback
        info = traceback.format_exception(*sys.exc_info())
        msg = info[(-1)].strip()
        if len(info) >= 3:
            msg += '\n   (f%s)' % info[(-2)].split('\n')[0].strip()[1:]
        print(file=sys.stderr)
        print('*** Error while highlighting:', file=sys.stderr)
        print(msg, file=sys.stderr)
        print('*** If this is a bug you want to report, please rerun with -v.', file=sys.stderr)
        return 1