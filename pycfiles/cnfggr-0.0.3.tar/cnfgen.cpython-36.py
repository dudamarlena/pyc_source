# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cnfformula/cnfgen.py
# Compiled at: 2019-10-28 05:33:57
# Size of source mod 2**32: 9529 bytes
__doc__ = 'Utilities to build CNF formulas interesting for proof complexity.\n\nThe module `cnfgen`  contains facilities to generate  cnf formulas, in\norder to  be printed  in dimacs  or LaTeX  formats. Such  formulas are\nready to be  fed to sat solvers.  In particular  the module implements\nboth a library of CNF generators and a command line utility.\n\nCreate the CNFs:\n\n>>> from . import CNF\n>>> c=CNF([ [(True,"x1"),(True,"x2"),(False,"x3")],           [(False,"x2"),(True,"x4")] ])\n>>> print( c.dimacs(export_header=False) )\np cnf 4 2\n1 2 -3 0\n-2 4 0\n\nYou can add clauses later in the process:\n\n>>> c.add_clause( [(False,"x3"),(True,"x4"),(False,"x5")] )\n>>> print( c.dimacs(export_header=False))\np cnf 5 3\n1 2 -3 0\n-2 4 0\n-3 4 -5 0\n\n'
import os, sys, random, argparse, signal, io
from .prjdata import __version__

def setup_command_line_args(parser):
    """Setup general command line options

    Setup options
    - query version
    - verbosity/silence
    - outputfile
    - outputformat
    - random seed

    Arguments:
    - `parser`: parser to fill with options
    """
    parser.add_argument('-V', '--version', action='version',
      version=('%(prog)s (' + __version__ + ')'))
    parser.add_argument('--output', '-o', type=argparse.FileType('w', encoding='utf-8'),
      metavar='<output>',
      default='-',
      help="Save the formula to <output>. Setting '<output>' to '-' sends the\n                        formula to standard output. (default: -)\n                        ")
    parser.add_argument('--output-format', '-of', choices=[
     'latex', 'dimacs'],
      default='dimacs',
      help="\n                        Output format of the formulas. 'latex' is\n                        convenient to insert formulas into papers, and\n                        'dimacs' is the format used by sat solvers.\n                        (default: dimacs)\n                        ")
    parser.add_argument('--seed', '-S', metavar='<seed>',
      default=None,
      type=str,
      action='store',
      help='Seed for any random process in the\n                        program. (default: current time)\n                        ')
    g = parser.add_mutually_exclusive_group()
    g.add_argument('--verbose', '-v', action='store_true', default=True, help='Output formula header and comments.')
    g.add_argument('--quiet', '-q', action='store_false', dest='verbose', help='Output just the formula with no header.')


def signal_handler(insignal, frame):
    """Manage program interruptions

    It has to be registered as signal handler.
    """
    print('Program interrupted', file=(sys.stderr))
    sys.exit(-1)


signal.signal(signal.SIGINT, signal_handler)

def search_cmdline_input_file(list_args):
    """Look for input file arguments in the command line

    Parameters
    ----------
    list_args : list of parsed command lines
    """
    for l in list_args:
        data = iter(vars(l).items())
        data = [v for k, v in data if not k.startswith('_')]
        data = [f for f in data if isinstance(f, io.IOBase)]
        data = [f for f in data if f != sys.stdin if f.mode == 'r']

    return data


def command_line_utility(argv=sys.argv):
    """CNFgen main command line interface

    This function provide the main interface to CNFgen. It sets up the
    command line, parses the command line arguments, builds the
    appropriate formula and outputs its representation.

    It **must not** raise exceptions, but fail with error messages for
    the user.

    Parameters
    ----------
    argv: list, optional
        The list of token with the command line arguments/options.
    """
    from . import families
    from . import transformations
    from .cmdline import is_cnfgen_subcommand
    from .cmdline import is_cnf_transformation_subcommand
    from .cmdline import find_methods_in_package
    t_parser = argparse.ArgumentParser(usage=(os.path.basename(argv[0]) + ' ...' + ' [-T <transformation> <params> -T <transformation> <params> ...]'),
      epilog="\n        Each <transformation> has its own command line arguments and options.\n        For more info type 'cnfgen ... -T <transformation> [--help | -h]'\n        ")
    t_subparsers = t_parser.add_subparsers(title='Available formula transformation', metavar='<transformation>')
    for sc in find_methods_in_package(transformations, is_cnf_transformation_subcommand,
      sortkey=(lambda x: x.name)):
        p = t_subparsers.add_parser((sc.name), help=(sc.description))
        sc.setup_command_line(p)
        p.set_defaults(transformation=sc)

    parser = argparse.ArgumentParser(prog=(os.path.basename(argv[0])), formatter_class=(argparse.RawDescriptionHelpFormatter),
      epilog=("\nEach <formula type> has its own command line arguments and options.\nFor more information type 'cnfgen <formula type> [--help | -h ]'.\nFurthermore it is possible to postprocess the formula by applying\na sequence of transformations.\n\n" + t_parser.format_help()))
    setup_command_line_args(parser)
    subparsers = parser.add_subparsers(title='Available formula types', metavar='<formula type>')
    for sc in find_methods_in_package(families, is_cnfgen_subcommand,
      sortkey=(lambda x: x.name)):
        p = subparsers.add_parser((sc.name), help=(sc.description))
        sc.setup_command_line(p)
        p.set_defaults(generator=sc)

    def splitlist(L, key):
        argbuffer = []
        for e in L:
            if e == key:
                yield argbuffer
                argbuffer = []
            else:
                argbuffer.append(e)

        yield argbuffer

    cmd_chunks = list(splitlist(argv, '-T'))
    generator_cmd = cmd_chunks[0][1:]
    transformation_cmds = cmd_chunks[1:]
    args = parser.parse_args(generator_cmd)
    t_args = []
    for cmd in transformation_cmds:
        t_args.append(t_parser.parse_args(cmd))

    if hasattr(args, 'seed'):
        if args.seed:
            random.seed(args.seed)
    if not hasattr(args, 'generator'):
        print('ERROR: The formula name to generate is missing\n', file=(sys.stderr))
        print((parser.format_help()), file=(sys.stderr))
        sys.exit(os.EX_DATAERR)
    else:
        for argdict in t_args:
            if not hasattr(argdict, 'transformation'):
                print('ERROR: The specification of some transformations are missing\n', file=(sys.stderr))
                print((t_parser.format_help()), file=(sys.stderr))
                sys.exit(os.EX_DATAERR)

        try:
            cnf = args.generator.build_cnf(args)
            for argdict in t_args:
                cnf = argdict.transformation.transform_cnf(cnf, argdict)

        except ValueError as e:
            print(e, file=(sys.stderr))
            sys.exit(os.EX_DATAERR)

        if args.output_format == 'latex':
            cmdline_descr = [
             '\\noindent\\textbf{Command line:}',
             '\\begin{lstlisting}[breaklines]',
             '$ cnfgen ' + ' '.join(argv[1:]),
             '\\end{lstlisting}']
            if hasattr(args.generator, 'docstring'):
                cmdline_descr += ['\\noindent\\textbf{Docstring:}',
                 '\\begin{lstlisting}[breaklines,basicstyle=\\small]',
                 args.generator.docstring,
                 '\\end{lstlisting}']
            for f in search_cmdline_input_file([args] + t_args):
                f.seek(0, 0)
                cmdline_descr += [
                 '\\noindent\\textbf{Input file} \\verb|%s|' % f.name, '\\begin{lstlisting}[breaklines,basicstyle=\\small]'] + f.readlines() + [
                 '\\end{lstlisting}']

            output = cnf.latex(export_header=(args.verbose), extra_text=('\n'.join(cmdline_descr + ['\n'])),
              full_document=True)
        else:
            if args.output_format == 'dimacs':
                output = cnf.dimacs(export_header=(args.verbose),
                  extra_text=('COMMAND LINE: cnfgen ' + ' '.join(argv[1:]) + '\n'))
            else:
                output = cnf.dimacs(export_header=(args.verbose),
                  extra_text=('COMMAND LINE: cnfgen ' + ' '.join(argv[1:]) + '\n'))
    print(output, file=(args.output))
    if args.output != sys.stdout:
        args.output.close()


if __name__ == '__main__':
    command_line_utility(sys.argv)