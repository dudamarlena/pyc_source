# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/out2arch.py
# Compiled at: 2008-04-20 13:19:45
"""
out2arch.py

output Gaussian's output file's arch info to stdout with format.

Usage: out2arch.py [options] outfname

Options:
    -f           output full data
    -h, --help   show help message
"""
import sys
__all__ = [
 'out2arch']
__revision__ = '$Rev$'
if sys.hexversion < 33619968:
    raise ImportError, 'This file only for python 2.1 or later'

def out2arch(ifile, full=0):
    """out2arch(ifile, full = 0) -> None
    output Gaussian's output file's arch info to stdout with format
    @ifile: file object of Gaussian log(out) file
    @full:
       full = 0: output is a standard gjf input
       full = 1: all information in arch
    output is directly to sys.stdout
    """
    lines = ifile.readlines()
    idx = 0
    while idx < len(lines) and lines[idx][:5] != ' 1\\1\\':
        idx = idx + 1

    if idx == len(lines):
        print >> sys.stderr, 'Invalid gaussian outfile'
        return False
    result = ''
    while result[-3:] != '\\\\@' and idx < len(lines):
        result = result + lines[idx][1:-1]
        idx = idx + 1

    if not full:
        pos1 = result.find('\\\\#')
        if pos1 != -1:
            result = result[pos1 + 2:]
        pos2 = result.find('\\\\Version=')
        if pos2 != -1:
            result = result[:pos2 + 1]
    result = result.split('\\')
    for x in result:
        print x

    return True


def usage(ofile):
    import os.path
    ofile.write('Usage: %s [options] outfname\n' % os.path.basename(sys.argv[0]))
    ofile.write('\n')
    ofile.write('Options:\n')
    ofile.write('    -a, -f       output all data\n')
    ofile.write('    -h, --help   show help message\n')


def main():
    import getopt
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'afh', ['help'])
    except getopt.GetoptError:
        usage(sys.stderr)
        sys.exit(2)

    full = 0
    for (o, _) in opts:
        if o in ('-h', '--help'):
            usage(sys.stdout)
            sys.exit()
        if o in ('-f', '-a'):
            full = 1

    if len(args) != 1:
        usage(sys.stderr)
        sys.exit(2)
    ifile = open(args[0])
    sys.exit(out2arch(ifile, full) == False)


if __name__ == '__main__':
    main()