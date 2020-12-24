# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pybitbucket/main.py
# Compiled at: 2016-12-28 18:40:02
# Size of source mod 2**32: 1282 bytes
from __future__ import print_function, unicode_literals
import argparse, sys
from pybitbucket import metadata

def main(argv):
    """Program entry point.

    :param argv: command-line arguments
    :type argv: :class:`list`
    """
    author_strings = []
    for name, email in zip(metadata.authors, metadata.emails):
        author_strings.append('Author: {0} <{1}>'.format(name, email))

    epilog = '\n{project} {version}\n\n{authors}\nURL: <{url}>\n'.format(project=(metadata.project),
      version=(metadata.version),
      authors=('\n'.join(author_strings)),
      url=(metadata.url))
    arg_parser = argparse.ArgumentParser(prog=(argv[0]),
      formatter_class=(argparse.RawDescriptionHelpFormatter),
      description=(metadata.description),
      epilog=epilog)
    arg_parser.add_argument('-V',
      '--version', action='version',
      version=('{0} {1}'.format(metadata.project, metadata.version)))
    arg_parser.parse_args(args=(argv[1:]))
    print(epilog)
    return 0


def entry_point():
    """Zero-argument entry point for use with setuptools/distribute."""
    raise SystemExit(main(sys.argv))


if __name__ == '__main__':
    entry_point()