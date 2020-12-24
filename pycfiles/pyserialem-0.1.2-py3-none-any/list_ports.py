# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./build/lib.linux-x86_64-2.7/serial/tools/list_ports.py
# Compiled at: 2015-08-30 15:56:23
__doc__ = 'This module will provide a function called comports that returns an\niterable (generator or list) that will enumerate available com ports. Note that\non some systems non-existent ports may be listed.\n\nAdditionally a grep function is supplied that can be used to search for ports\nbased on their descriptions or hardware ID.\n'
import sys, os, re
if os.name == 'nt':
    from serial.tools.list_ports_windows import comports
elif os.name == 'posix':
    from serial.tools.list_ports_posix import comports
else:
    raise ImportError("Sorry: no implementation for your platform ('%s') available" % (os.name,))

def grep(regexp):
    """    Search for ports using a regular expression. Port name, description and
    hardware ID are searched. The function returns an iterable that returns the
    same tuples as comport() would do.
    """
    r = re.compile(regexp, re.I)
    for port, desc, hwid in comports():
        if r.search(port) or r.search(desc) or r.search(hwid):
            yield (
             port, desc, hwid)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Serial port enumeration')
    parser.add_argument('regexp', nargs='?', help='only show ports that match this regex')
    parser.add_argument('-v', '--verbose', action='store_true', help='show more messages')
    parser.add_argument('-q', '--quiet', action='store_true', help='suppress all messages')
    parser.add_argument('-n', type=int, help='only output the N-th entry')
    args = parser.parse_args()
    hits = 0
    if args.regexp:
        sys.stderr.write('Filtered list with regexp: %r\n' % (args.regexp,))
        iterator = sorted(grep(args.regexp))
    else:
        iterator = sorted(comports())
    for n, (port, desc, hwid) in enumerate(iterator, 1):
        if args.n is None or args.n == n:
            sys.stdout.write(('{:20}\n').format(port))
            if args.verbose:
                sys.stdout.write(('    desc: {}\n').format(desc))
                sys.stdout.write(('    hwid: {}\n').format(hwid))
        hits += 1

    if not args.quiet:
        if hits:
            sys.stderr.write(('{} ports found\n').format(hits))
        else:
            sys.stderr.write('no ports found\n')
    return


if __name__ == '__main__':
    main()