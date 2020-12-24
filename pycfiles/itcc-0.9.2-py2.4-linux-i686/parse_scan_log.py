# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tinker/parse_scan_log.py
# Compiled at: 2008-04-20 13:19:45
__all__ = [
 'parse_tinker_scan_log']

def parse_tinker_scan_log(ifile, ofile):
    results = []
    for line in ifile:
        if 'Potential Surface Map' in line:
            results.append(line)

    results.sort(key=lambda x: float(x.split()[(-1)]))
    ofile.writelines(results)


def _help(ofile):
    ofile.write('usage: parse_tinker_scan_log filename|-\nparse tinker scan log file\n')


def main():
    import sys
    if len(sys.argv) != 2:
        _help(sys.stderr)
        sys.exit(1)
    if sys.argv[1] == '-':
        ifile = sys.stdin
    else:
        ifile = file(sys.argv[1])
    parse_tinker_scan_log(ifile, sys.stdout)


if __name__ == '__main__':
    main()