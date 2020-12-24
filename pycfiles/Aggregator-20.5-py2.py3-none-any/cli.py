# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aggregate_prefixes/cli.py
# Compiled at: 2019-06-24 08:29:27
__doc__ = b'\nProvides CLI interface for package aggregate-prefixes\n'
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import argparse, sys
from aggregate_prefixes import aggregate_prefixes
from aggregate_prefixes import __version__ as VERSION

def main():
    """
    Aggregates IPv4 or IPv6 prefixes from file or STDIN.

    Reads a list of unsorted IPv4 or IPv6 prefixes from a file or STDIN.
    Returns a sorted list of aggregates to STDOUT.
    """
    parser = argparse.ArgumentParser(prog=b'aggregate-prefixes', description=b'Aggregates IPv4 or IPv6 prefixes from file or STDIN')
    parser.add_argument(b'prefixes', type=argparse.FileType(b'r'), help=b"Text file of unsorted list of IPv4 or IPv6 prefixes. Use '-' for STDIN.", default=sys.stdin)
    parser.add_argument(b'--max-length', b'-m', metavar=b'LENGTH', type=int, help=b'Discard longer prefixes prior to processing', default=128)
    parser.add_argument(b'--truncate', b'-t', metavar=b'MASK', type=int, help=b'Truncate IP/mask to network/mask', default=128)
    parser.add_argument(b'--verbose', b'-v', help=b'Display verbose information about the optimisations', action=b'store_true')
    parser.add_argument(b'--version', b'-V', action=b'version', version=b'%(prog)s ' + VERSION)
    args = parser.parse_args()
    prefixes = [ p for p in set([ p.strip() for line in args.prefixes for p in line.split(b' ') if not p.startswith(b'#') ]) if p
               ]
    try:
        aggregates = aggregate_prefixes(prefixes, args.max_length, args.truncate, args.verbose)
    except (ValueError, TypeError) as error:
        sys.exit(b'ERROR: %s' % error)

    print((b'\n').join(aggregates))


if __name__ == b'__main__':
    main()