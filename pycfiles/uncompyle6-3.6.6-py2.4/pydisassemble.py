# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/uncompyle6/bin/pydisassemble.py
# Compiled at: 2020-04-20 22:50:15
import sys, os, getopt
from uncompyle6.disas import disassemble_file
from uncompyle6.version import VERSION
(program, ext) = os.path.splitext(os.path.basename(__file__))
__doc__ = "\nUsage:\n  %s [OPTIONS]... FILE\n  %s [--help | -h | -V | --version]\n\nDisassemble FILE with the instruction mangling that is done to\nassist uncompyle6 in parsing the instruction stream. For example\ninstructions with variable-length arguments like CALL_FUNCTION and\nBUILD_LIST have argument counts appended to the instruction name, and\nCOME_FROM instructions are inserted into the instruction stream.\n\nExamples:\n  %s foo.pyc\n  %s foo.py    # same thing as above but find the file\n  %s foo.pyc bar.pyc  # disassemble foo.pyc and bar.pyc\n\nSee also `pydisasm' from the `xdis' package.\n\nOptions:\n  -V | --version     show version and stop\n  -h | --help        show this message\n\n" % ((program,) * 5)
PATTERNS = ('*.pyc', '*.pyo')

def main():
    Usage_short = 'usage: %s FILE...\nType -h for for full help.' % program
    if len(sys.argv) == 1:
        sys.stderr.write('No file(s) given\n')
        sys.stderr.write(Usage_short)
        sys.exit(1)
    try:
        (opts, files) = getopt.getopt(sys.argv[1:], 'hVU', [
         'help', 'version', 'uncompyle6'])
    except getopt.GetoptError(e):
        sys.stderr.write('%s: %s' % (os.path.basename(sys.argv[0]), e))
        sys.exit(-1)

    for (opt, val) in opts:
        if opt in ('-h', '--help'):
            print __doc__
            sys.exit(1)
        elif opt in ('-V', '--version'):
            print '%s %s' % (program, VERSION)
            sys.exit(0)
        else:
            print opt
            sys.stderr.write(Usage_short)
            sys.exit(1)

    for file in files:
        if os.path.exists(files[0]):
            disassemble_file(file, sys.stdout)
        else:
            sys.stderr.write("Can't read %s - skipping\n" % files[0])


if __name__ == '__main__':
    main()