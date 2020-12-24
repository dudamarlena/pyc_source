# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redis_sniffer/sniffer.py
# Compiled at: 2015-03-18 20:53:01
""" A redis query sniffer
"""
import re, socket
from collections import defaultdict
import pcap, dpkt
from log import Log

class Sniffer:
    re_args = re.compile('\\*\\d+')
    re_lens = re.compile('\\$\\d+')

    def __init__(self):
        pass

    @staticmethod
    def sniff(interface, port=6379, src_ip=None, dst_ip=None, debug=False):
        pc = pcap.pcap(interface)
        _filter = 'tcp port %s' % port
        if src_ip:
            _filter += ' and src %s' % src_ip
        if dst_ip:
            _filter += ' and dst %s' % dst_ip
        pc.setfilter(_filter)
        if debug:
            logger = Log('debug', './', {'debug': 'rs_debug'})
        receiving = False
        receiving_partials = {}
        request_sizes = defaultdict(int)
        sessions = {}
        if debug:
            logger.write_debug('<=============== Checking for Ethernet Packets ==============>')
        for ptime, pdata in pc:
            ether_pkt = dpkt.ethernet.Ethernet(pdata)
            ip_pkt = ether_pkt.data
            tcp_pkt = ip_pkt.data
            tcp_data = tcp_pkt.data
            if debug:
                logger.write_debug('Checking the length of the tcp packet')
            if len(tcp_data) == 0:
                if debug:
                    logger.write_debug('TCP Packet is empty')
                continue
            if debug:
                logger.write_debug('TCP Packet has data')
            src = socket.inet_ntoa(ip_pkt.src)
            sport = tcp_pkt.sport
            dst = socket.inet_ntoa(ip_pkt.dst)
            dport = tcp_pkt.dport
            src_addr = '%s:%s' % (src, sport)
            dst_addr = '%s:%s' % (dst, dport)
            if debug:
                logger.write_debug('Checking to see if the data is being sent or received')
            if sport == port:
                if debug:
                    logger.write_debug('Data is being sent')
                receiving = False
                client = dst_addr
            else:
                if debug:
                    logger.write_debug('Data is being received')
                receiving = True
                client = src_addr
            if receiving:
                if not tcp_data:
                    continue
                _parts = tcp_data.splitlines()
                _receiving_partial = receiving_partials.get(client, [])
                _parts = _receiving_partial + _parts
                request_sizes[client] += len(pdata)
                request_size = request_sizes[client]
                n_parts = len(_parts)
                if debug:
                    logger.write_debug('Check to ensure the packets contain valid redis commands')
                try:
                    n_args = int(_parts[0][1:])
                except ValueError:
                    continue

                if n_args * 2 + 1 == n_parts and int(_parts[(-2)][1:]) == len(_parts[(-1)]):
                    command = (' ').join([ c for i, c in enumerate(_parts[1:]) if i % 2 == 1 ])
                    receiving_partials.pop(client, None)
                    request_sizes.pop(client, None)
                elif _parts[2] == 'MULTI':
                    if _parts[(-1)] == 'EXEC':
                        _multi_parts = _parts[2:]
                        _partial = []
                        _n_args = 1
                        for _part in _multi_parts:
                            if re_args.match(_part):
                                _n_args = int(_part[1:])
                                continue
                            if re_lens.match(_part):
                                continue
                            if _n_args > 0:
                                _partial.append(_part)
                                _n_args -= 1
                                if _n_args == 0 and _part != 'EXEC':
                                    _partial.append('/')
                                continue

                        command = (' ').join(_partial)
                        receiving_partials.pop(client, None)
                        request_sizes.pop(client, None)
                    else:
                        receiving_partials[client] = _parts
                        continue
                else:
                    receiving_partials[client] = _parts
                    continue
                stat = sessions.pop(client, None)
                if stat:
                    _request_size = stat.get('request_size', 0)
                    _response_size = stat.get('response_size', 0)
                    _command = stat['command']
                    yield (ptime, client, _request_size, _response_size, _command)
                sessions[client] = {'command': command, 'request_size': request_size}
            else:
                session = sessions.get(client)
                if not session:
                    continue
                if session.get('response_size'):
                    session['response_size'] += len(pdata)
                else:
                    session['response_size'] = len(pdata)

        return