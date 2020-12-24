# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sk/seckiss/rfw/rfw/cmdparse.py
# Compiled at: 2014-03-26 11:08:28
import sys, logging, urlparse, re, iputil, timeutil, iptables
from iptables import Rule
log = logging.getLogger('rfw.cmdparse')

def convert_iface(iface):
    """Convert iface string like 'any', 'eth', 'eth0' to iptables iface naming like *, eth+, eth0. 
    """
    if iface == 'any':
        return '*'
    else:
        if not iface[(-1)].isdigit():
            iface += '+'
        return iface


class PathError(Exception):

    def __init__(self, path, msg=''):
        Exception.__init__(self, ('Incorrect path: {}. {}').format(path, msg))


def parse_command_path(path):

    def path_parts(path):
        path = path.strip().lower()
        if len(path) < 1 or path[0] != '/':
            raise PathError(path)
        if path[(-1)] == '/':
            path = path[:-1]
        p = map(str.strip, path.split('/'))
        p = tuple(p[1:])
        return p

    p = path_parts(path)
    if not p:
        return ('help', None)
    else:
        action = p[0]
        if action.upper() in iptables.RULE_TARGETS:
            try:
                return (
                 action, build_rule(p))
            except ValueError as e:
                raise PathError(path, e.message)

        if action == 'list':
            if len(p) == 1:
                return (action, None)
            if len(p) == 2:
                chain = p[1].upper()
                if chain in iptables.RULE_CHAINS:
                    return (action, chain)
                raise PathError(path, 'Wrong chain name for list command')
            else:
                raise PathError(path, 'Too many details for the list command')
        raise PathError(path)
        return


def build_rule(p):
    if len(p) < 4:
        raise ValueError('Not enough details to construct the rule')
    target = p[0].upper()
    if target not in iptables.RULE_TARGETS:
        raise ValueError(('The action should be one of {}').format(iptables.RULE_TARGETS))
    chain = p[1].upper()
    if chain not in iptables.RULE_CHAINS:
        raise ValueError(('The chain should be one of {}').format(iptables.RULE_CHAINS))
    iface1 = p[2]
    if len(iface1) > 16:
        raise ValueError('Interface name too long. Max 16 characters')
    iface1 = convert_iface(iface1)
    ip1 = iputil.validate_ip(p[3])
    if not ip1:
        raise ValueError('Incorrect IP address')
    mask1 = None
    iface2 = None
    ip2 = None
    mask2 = None
    if len(p) > 4:
        i = 4
        if p[i].isdigit():
            if iputil.validate_mask_limit(p[i]):
                mask1 = p[i]
                i = i + 1
            else:
                raise ValueError('Netmask must be in range from 9 to 32')
        if len(p) > i:
            iface2 = p[i]
            i = i + 1
            if len(iface2) > 16:
                raise ValueError('Interface name too long. Max 16 characters')
            iface2 = convert_iface(iface2)
            if len(p) > i:
                ip2 = iputil.validate_ip(p[i])
                i = i + 1
                if not ip2:
                    raise ValueError('Incorrect IP address or netmask')
                if len(p) > i:
                    if iputil.validate_mask_limit(p[i]):
                        mask2 = p[i]
                    else:
                        raise ValueError('Incorrect netmask value')
    if chain in ('INPUT', 'OUTPUT'):
        if len(p) > 5:
            raise ValueError(('Too many details for the {} chain').format(chain))
        if len(p) > 4 and not mask1:
            raise ValueError('Incorrect netmask value')
    if chain in ('FORWARD', ):
        if len(p) > 8:
            raise ValueError(('Too many details for the {} chain').format(chain))
        if len(p) > 7 and (not mask1 or not mask2):
            raise ValueError('Incorrect netmask value')
        if len(p) > 6 and not mask1 and not mask2:
            raise ValueError('Incorrect netmask value')
    if chain == 'INPUT':
        inp = iface1
        out = '*'
        source = ip1
        if mask1:
            source = ('{}/{}').format(source, mask1)
        destination = '0.0.0.0/0'
    elif chain == 'OUTPUT':
        inp = '*'
        out = iface1
        source = '0.0.0.0/0'
        destination = ip1
        if mask1:
            destination = ('{}/{}').format(destination, mask1)
    elif chain == 'FORWARD':
        inp = iface1
        if iface2:
            out = iface2
        else:
            out = '*'
        source = ip1
        print ('mask1: ').format(mask1)
        if mask1:
            source = ('{}/{}').format(ip1, mask1)
        destination = '0.0.0.0/0'
        if ip2:
            destination = ip2
        if mask2:
            destination = ('{}/{}').format(destination, mask2)
    else:
        assert 'Should not happen'
    return Rule({'target': target, 'chain': chain, 'inp': inp, 'out': out, 'source': source, 'destination': destination})


def parse_command_query(query):
    params = dict(urlparse.parse_qsl(query))
    ret = {}
    expire = params.get('expire')
    if expire:
        interval = timeutil.parse_interval(expire)
        if interval is None:
            raise ValueError('Incorrect expire parameter value')
        ret['expire'] = str(interval)
    wait = params.get('wait')
    if wait:
        wait = wait.lower()
        if wait == 'true':
            ret['wait'] = wait
        else:
            raise ValueError('Incorrect wait parameter value')
    modify = params.get('modify')
    if modify:
        modify = modify.lower()
        if modify in ('insert', 'delete'):
            ret['modify'] = modify
        else:
            raise ValueError('Incorrect modify parameter value')
    return ret


def parse_command(url):
    """
    return dict with command elements like:
    {'chain': 'input', 'iface1': 'eth', 'ip1': '11.22.33.44', 'expire': '3600'}
    chain == input implies that ip1 is a source address
    chain == output implies that ip1 is a destination address
    """
    parsed = urlparse.urlparse(url)
    path, query = parsed.path, parsed.query
    action, rule = parse_command_path(path)
    directives = parse_command_query(query)
    return (
     action, rule, directives)