# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/swaggerpy/codegen.py
# Compiled at: 2016-11-21 09:01:44
# Size of source mod 2**32: 921 bytes
__doc__ = 'Main entry point for codegen command line app.\n'
import sys
from optparse import OptionParser
USAGE = 'usage: %prog [options] template-dir output-dir'

def main(argv=None):
    """Main method, as invoked by setuptools launcher script.

    :param argv: Command line argument list.
    """
    if argv is None:
        argv = sys.argv
    parser = OptionParser(usage=USAGE)
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False, help='Verbose output')
    options, args = parser.parse_args(argv)
    if len(args) < 3:
        parser.error('Missing arguments')
    elif len(args) > 3:
        parser.error('Too many arguments')
    template_dir = args[1]
    output_dir = args[2]


if __name__ == '__main__':
    sys.exit(main() or 0)