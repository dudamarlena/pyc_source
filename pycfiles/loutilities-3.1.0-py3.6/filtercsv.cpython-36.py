# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\filtercsv.py
# Compiled at: 2019-11-25 16:48:13
# Size of source mod 2**32: 4592 bytes
"""
filtercsv - filter a csv file based on indicated filter
===============================================================

Usage::

    TBA
                            
    
"""
import argparse, csv, textwrap, json, sys
from . import version

class invalidParameter(Exception):
    pass


def main():
    """
    filter standard input to standard output
    """
    descr = textwrap.dedent('            reads stdin and applies FILTER argument to produce stdout\n    \n            FILTER is a string representing a dict or list of dicts.\n            \n            The keys of each dict are column headers for which all of the values\n            of the dict must be matched for the filter to pass a row in the input\n            file (AND function)\n            \n            If the filter needs to test that a value of the filter and the row NOT\n            match, TBD\n            \n            if a list of dicts is provided, the row passes if any of the dicts match\n            (OR function)\n            ')
    parser = argparse.ArgumentParser(prog='filtercsv', description=descr,
      formatter_class=(argparse.RawDescriptionHelpFormatter),
      version=('{0} {1}'.format('loutilities', version.__version__)))
    parser.add_argument('filter', help='list of dicts or single dict. All items within dict must match for any dict in the list to pass filter')
    args = parser.parse_args()
    if sys.platform == 'win32':
        import os, msvcrt
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    filt = json.loads(args.filter)
    if not isinstance(filt, list):
        filt = [
         filt]
    for f in filt:
        if not isinstance(f, dict):
            raise invalidParameter('FILTER must be dict or list of dicts')

    hdr = next(sys.stdin)
    sys.stdout.write(hdr)
    H = csv.reader([hdr])
    hdrlist = next(H)
    IN = csv.DictReader((sys.stdin), fieldnames=hdrlist)
    OUT = csv.DictWriter(sys.stdout, hdrlist)
    for line in IN:
        for f in filt:
            match = True
            for col in list(f.keys()):
                if f[col] != line[col]:
                    match = False
                    break

            if match:
                break

        if match:
            OUT.writerow(line)

    sys.stdin.close()
    sys.stdout.close()


if __name__ == '__main__':
    main()