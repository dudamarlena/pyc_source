# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/formic/command.py
# Compiled at: 2012-08-15 02:40:35
"""The command-line glue-code for :command:`formic`. Call :func:`~formic.command.main()`
with the command-line arguments.

Full usage of the command is::

  usage: formic [-i [INCLUDE [INCLUDE ...]]] [-e [EXCLUDE [EXCLUDE ...]]]
               [--no-default-excludes] [--no-symlinks] [-r] [-h] [--usage]
               [--version]
               [directory]

  Search the file system using Apache Ant globs

  Directory:
    directory             The directory from which to start the search (defaults
                          to current working directory)

  Globs:
    -i [INCLUDE [INCLUDE ...]], --include [INCLUDE [INCLUDE ...]]
                          One or more Ant-like globs in include in the search.If
                          not specified, then all files are implied
    -e [EXCLUDE [EXCLUDE ...]], --exclude [EXCLUDE [EXCLUDE ...]]
                          One or more Ant-like globs in include in the search
    --no-default-excludes
                          Do not include the default excludes
    --no-symlinks         Do not include symlinks

  Output:
     -r, --relative       Print file paths relative to directory.

  Information:
    -h, --help            Prints this help and exits
    --usage               Prints additional help on globs and exits
    --version             Prints the version of formic and exits

"""
from argparse import ArgumentParser, SUPPRESS, RawDescriptionHelpFormatter
from sys import argv, stdout
from os import path
from pkg_resources import resource_string
from formic import FileSet, FormicError, get_version
DESCRIPTION = 'Search the file system using Apache Ant globs'
EPILOG = 'For documentation, source code and other information, please visit:\nhttp://www.aviser.asia/formic\n\nThis program comes with ABSOLUTELY NO WARRANTY. See license for details.\n\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; for details, run\n> formic --license\n\nFormic is Copyright (C) 2012, Aviser LLP, Singapore'

def create_parser():
    """Creates and returns the command line parser, an
     :class:`argparser.ArgumentParser` instance."""
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter, description=DESCRIPTION, epilog=EPILOG, add_help=False)
    directory = parser.add_argument_group('Directory')
    directory.add_argument(dest='directory', action='store', default=None, nargs='?', help='The directory from which to start the search (defaults to current working directory)')
    globs = parser.add_argument_group('Globs')
    globs.add_argument('-i', '--include', action='store', nargs='*', help='One or more Ant-like globs in include in the search.If not specified, then all files are implied')
    globs.add_argument('-e', '--exclude', action='store', nargs='*', help='One or more Ant-like globs in include in the search')
    globs.add_argument('--no-default-excludes', dest='default_excludes', action='store_false', default=True, help='Do not include the default excludes')
    globs.add_argument('--no-symlinks', action='store_true', default=False, help='Do not include symlinks')
    output = parser.add_argument_group('Output')
    output.add_argument('-r', '--relative', action='store_true', default=False, help='Print file paths relative to directory.')
    info = parser.add_argument_group('Information')
    info.add_argument('-h', '--help', action='store_true', default=False, help='Prints this help and exits')
    info.add_argument('--usage', action='store_true', default=False, help='Prints additional help on globs and exits')
    info.add_argument('--version', action='store_true', default=False, help='Prints the version of formic and exits')
    info.add_argument('--license', action='store_true', help=SUPPRESS)
    return parser


def main(*kw):
    """Command line entry point; arguments must match those defined in
    in :meth:`create_parser()`; returns 0 for success, else 1.

    Example::

      command.main("-i", "**/*.py", "--no-default-excludes")

    Runs formic printing out all .py files in the current working directory
    and its children to ``sys.stdout``.

    If *kw* is None, :func:`main()` will use ``sys.argv``."""
    parser = create_parser()
    args = parser.parse_args(kw if kw else None)
    if args.help:
        parser.print_help()
    elif args.usage:
        print 'Ant Globs\n=========\n\nApache Ant fileset is documented at the Apache Ant project:\n\n* http://ant.apache.org/manual/dirtasks.html#patterns\n\nExamples\n--------\n\nAnt Globs are like simple file globs (they use ? and * in the same way), but\ninclude powerful ways for selecting directories. The examples below use the\nAnt glob naming, so a leading slash represents the top of the search, *not* the\nroot of the file system.\n\n    *.py\n            Selects every matching file anywhere in the whole tree\n                Matches /foo.py and /bar/foo.py\n                but not /foo.pyc or /bar/foo.pyc/\n\n    /*.py\n            Selects every matching file in the root of the directory (but no\n            deeper).\n\n            Matches /foo.py but not /bar/foo.py\n\n    /myapp/**\n            Matches all files under /myapp and below.\n\n    /myapp/**/__init__.py\n            Matches all __init__.py files /myapp and below.\n\n    dir1/__init__.py\n            Selects every __init__.py in directory dir1. dir1\n            directory can be anywhere in the directory tree\n\n            Matches /dir1/file.py, /dir3/dir1/file.py and\n            /dir3/dir2/dir1/file.py but not /dir1/another/__init__.py.\n\n    **/dir1/__init__.py\n            Same as above.\n\n    /**/dir1/__init__.py\n            Same as above.\n\n    /myapp/**/dir1/__init__.py\n            Selects every __init__.py in dir1 in the directory tree\n            /myapp under the root.\n\n            Matches /myapp/dir1/__init__.py and /myapp/dir2/dir1/__init__.py\n            but not /myapp/file.txt and /dir1/file.txt\n\nDefault excludes\n----------------\n\nAnt FileSet (and Formic) has built-in patterns to screen out a lot of\ndevelopment \'noise\', such as hidden VCS files and directories. The full list is\nat:\n\n    * http://www.aviser.asia/formic/api.html#formic.formic.get_initial_default_excludes\n\nDefault excludes can be simply switched off on both the command line and the\nAPI, for example::\n\n    $ formic -i "*.py" -e "__init__.py" "**/*test*/" "test_*" --no-default-excludes\n'
    elif args.version:
        print 'formic', get_version(), 'http://www.aviser.asia/formic'
    elif args.license:
        print resource_string(__name__, 'LICENSE.txt')
    else:
        try:
            fileset = FileSet(directory=args.directory, include=args.include if args.include else ['*'], exclude=args.exclude, default_excludes=args.default_excludes, symlinks=not args.no_symlinks)
        except FormicError as exception:
            parser.print_usage()
            print exception.message
            return 1

        prefix = fileset.get_directory()
        for directory, file_name in fileset.files():
            if args.relative:
                stdout.write('.')
            else:
                stdout.write(prefix)
            if dir:
                stdout.write(path.sep)
                stdout.write(directory)
            stdout.write(path.sep)
            stdout.write(file_name)
            stdout.write('\n')

    return 0


def entry_point():
    """Entry point for command line; calls :meth:`~formic.command.main()` and then
    :func:`sys.exit()` with the return value."""
    result = main()
    exit(result)


if __name__ == '__main__':
    main(*argv[1:])