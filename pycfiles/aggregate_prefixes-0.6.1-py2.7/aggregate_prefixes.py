# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aggregate_prefixes/aggregate_prefixes.py
# Compiled at: 2019-06-24 08:29:08
"""
Provides core functions for package aggregate-prefixes
"""
from __future__ import print_function
import sys, ipaddress

def aggregate_prefixes(prefixes, max_length=128, truncate=False, debug=False):
    """
    Aggregates IPv4 or IPv6 prefixes.

    Gets a list of unsorted IPv4 or IPv6 prefixes and returns a sorted iterable of aggregates.

    Parameters
    ----------
    prefixes : list
        Unsorted list of IPv4 or IPv6 prefixes serialized as strings or ipaddr objects
    max_length: int
        Discard longer prefixes prior to processing
    truncate:
        Truncate IP/mask to network/mask
    debug: bool
        Write debug information on STDOUT

    Returns
    -------
    generator
        Sorted iterable of IPv4 or IPv6 aggregated prefixes serialized as strings

    """
    prefixes = sorted([ p for p in [ ipaddress.ip_network(p, False) for p in prefixes ] if p.prefixlen <= max_length
                      ], key=lambda p: (
     p.network_address, p.prefixlen))
    if debug:
        print('PREFIXES: %s\n' % (', ').join([ str(_) for _ in prefixes ]), file=sys.stderr)
    _id = 0
    total_prefixes = len(prefixes)
    while _id < total_prefixes:
        prefix = prefixes[_id]
        if debug:
            print('LOOP START -->\n', file=sys.stderr)
            print('PREFIX: %s (Network: %s, Broadcast: %s)' % (
             prefix, prefix.network_address, prefix.broadcast_address), file=sys.stderr)
        if truncate and prefix.prefixlen > truncate:
            prefix = ipaddress.ip_network('%s/%d' % (prefix.network_address, truncate), False)
            if debug:
                print('TRUNCATED: %s (Network: %s, Broadcast: %s to )' % (
                 prefix, prefix.network_address, prefix.broadcast_address), file=sys.stderr)
        contigous_prefixes = [
         prefix]
        last_contigous = prefix
        next_id = _id + 1
        while next_id < total_prefixes:
            last_contigous = contigous_prefixes[(-1)]
            next_prefix = prefixes[next_id]
            if debug:
                print('NEXT: %s (Network: %s, Broadcast: %s)' % (
                 next_prefix, next_prefix.network_address, next_prefix.broadcast_address), file=sys.stderr)
            if truncate and next_prefix.prefixlen > truncate:
                next_prefix = ipaddress.ip_network('%s/%d' % (next_prefix.network_address, truncate), False)
                if debug:
                    print('TRUNCATED: %s (Network: %s, Broadcast: %s to )' % (
                     next_prefix, next_prefix.network_address, next_prefix.broadcast_address), file=sys.stderr)
            if last_contigous.broadcast_address >= next_prefix.broadcast_address:
                next_id += 1
                continue
            if last_contigous.broadcast_address + 1 != next_prefix.network_address:
                break
            contigous_prefixes.append(next_prefix)
            next_id += 1

        last_contigous = contigous_prefixes[(-1)]
        _id = next_id
        contigous_id = 0
        total_contigous = len(contigous_prefixes)
        while contigous_id < total_contigous:
            first_contigous = contigous_prefixes[contigous_id]
            if debug:
                print('\nCONTIGOUS: %s' % (', ').join([ str(_) for _ in contigous_prefixes[contigous_id:] ]), file=sys.stderr)
                print('FIRST: %s (Network: %s, Broadcast: %s)' % (
                 first_contigous,
                 first_contigous.network_address,
                 first_contigous.broadcast_address), file=sys.stderr)
                print('LAST: %s (Network: %s, Broadcast: %s)' % (
                 last_contigous,
                 last_contigous.network_address,
                 last_contigous.broadcast_address), file=sys.stderr)
            aggregate = first_contigous
            tentative_len = first_contigous.prefixlen
            while tentative_len > 0:
                tentative_len -= 1
                tentative = ipaddress.ip_network('%s/%d' % (first_contigous.network_address, tentative_len), False)
                if debug:
                    print('TENTATIVE: %s (Network: %s, Broadcast: %s)' % (
                     tentative, tentative.network_address, tentative.broadcast_address), file=sys.stderr)
                if tentative.network_address != first_contigous.network_address or tentative.broadcast_address > last_contigous.broadcast_address:
                    break
                aggregate = tentative

            if debug:
                print('AGGREGATE: %s (Network: %s, Broadcast: %s)' % (
                 aggregate, aggregate.network_address, aggregate.broadcast_address), file=sys.stderr)
            covered_id = contigous_id + 1
            while covered_id < total_contigous:
                if debug:
                    print('TESTING: %s (Network: %s, Broadcast: %s)' % (
                     contigous_prefixes[covered_id],
                     contigous_prefixes[covered_id].network_address,
                     contigous_prefixes[covered_id].broadcast_address), file=sys.stderr)
                if aggregate.broadcast_address < contigous_prefixes[covered_id].network_address:
                    break
                covered_id += 1

            if debug:
                print('COVERED: %s\n' % (', ').join([ str(_) for _ in contigous_prefixes[contigous_id:covered_id] ]), file=sys.stderr)
            contigous_id = covered_id
            yield '%s/%d' % (aggregate.network_address, aggregate.prefixlen)

        if debug:
            print('<-- LOOP END', file=sys.stderr)

    if debug:
        print('', file=sys.stderr)