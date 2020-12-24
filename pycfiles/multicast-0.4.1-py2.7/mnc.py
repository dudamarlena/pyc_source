# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mnc.py
# Compiled at: 2013-09-07 17:21:40
import logging
logging.basicConfig(level=logging.DEBUG)
import multicast

def argmain():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('-p', '--port', default=4242, help='Port to listen on/send to')
    p.add_argument('-a', '--addr', default='224.0.42.42', help='Multicast group/address to join')
    p.add_argument('-s', '--server', action='store_true', help='Listen for and dump multicast packets on the specified address and port')
    args = p.parse_args()
    logger = logging.getLogger('mcast')
    if args.server:

        def packet_handler(packet, addr):
            print addr, packet

        multicast.listen(packet_handler, args.addr, args.port)
    else:

        def packet_generator():
            import sys
            for line in sys.stdin:
                yield line.strip()

        print 'Ready to send... send EOF twice to quit.'
        multicast.sendto(packet_generator(), args.addr, args.port)


argmain()