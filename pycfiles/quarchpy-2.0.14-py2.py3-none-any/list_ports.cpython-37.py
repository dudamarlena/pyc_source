# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\connection_specific\serial\tools\list_ports.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 3349 bytes
"""This module will provide a function called comports that returns an
iterable (generator or list) that will enumerate available com ports. Note that
on some systems non-existent ports may be listed.

Additionally a grep function is supplied that can be used to search for ports
based on their descriptions or hardware ID.
"""
import sys, os, re
if os.name == 'nt':
    from serial.tools.list_ports_windows import comports
else:
    if os.name == 'posix':
        from serial.tools.list_ports_posix import comports
    else:
        raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))

def grep(regexp, include_links=False):
    """    Search for ports using a regular expression. Port name, description and
    hardware ID are searched. The function returns an iterable that returns the
    same tuples as comport() would do.
    """
    r = re.compile(regexp, re.I)
    for info in comports(include_links):
        port, desc, hwid = info
        if r.search(port) or r.search(desc) or r.search(hwid):
            yield info


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Serial port enumeration')
    parser.add_argument('regexp',
      nargs='?',
      help='only show ports that match this regex')
    parser.add_argument('-v',
      '--verbose', action='store_true',
      help='show more messages')
    parser.add_argument('-q',
      '--quiet', action='store_true',
      help='suppress all messages')
    parser.add_argument('-n',
      type=int,
      help='only output the N-th entry')
    parser.add_argument('-s',
      '--include-links', action='store_true',
      help='include entries that are symlinks to real devices')
    args = parser.parse_args()
    hits = 0
    if args.regexp:
        if not args.quiet:
            sys.stderr.write('Filtered list with regexp: {!r}\n'.format(args.regexp))
        iterator = sorted(grep((args.regexp), include_links=(args.include_links)))
    else:
        iterator = sorted(comports(include_links=(args.include_links)))
    for n, (port, desc, hwid) in enumerate(iterator, 1):
        if not args.n is None:
            if args.n == n:
                sys.stdout.write('{:20}\n'.format(port))
                if args.verbose:
                    sys.stdout.write('    desc: {}\n'.format(desc))
                    sys.stdout.write('    hwid: {}\n'.format(hwid))
            hits += 1

    if not args.quiet:
        if hits:
            sys.stderr.write('{} ports found\n'.format(hits))
        else:
            sys.stderr.write('no ports found\n')


if __name__ == '__main__':
    main()