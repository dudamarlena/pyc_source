# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/haproxy_cfg.py
# Compiled at: 2019-05-16 13:41:33
"""
HaproxyCfg - file ``/etc/haproxy/haproxy.cfg``
==============================================

Contents of the `haproxy.cfg` file look like::

    global
        daemon
        group       haproxy
        log         /dev/log local0
        user        haproxy
        maxconn     20480
        pidfile     /var/run/haproxy.pid

    defaults
        retries     3
        maxconn     4096
        log         global
        timeout     http-request 10s
        timeout     queue 1m
        timeout     connect 10s

If there are duplicate key items, merge them in to one. Like::

    option  tcpka
                            }--->    option: ["tcpka","tcplog"]
    option  tcplog

Examples:
    >>> cfg = shared[HaproxyCfg]
    >>> cfg.data['global']
    {"daemon": "", "group": "haproxy", "log": " /dev/log local0",
     "user": "haproxy", "maxconn": "20480", "pidfile": "/var/run/haproxy.pid"}
    >>> cfg.data['global']['group']
    "haproxy"
    >>> 'global' in cfg.data
    True
    >>> 'user' in cfg.data.get('global')
    True
    """
from .. import Parser, parser
from insights.specs import Specs

def _parse_content(content):
    SECTION_NAMES = ('global', 'defaults', 'frontend', 'backend', 'listen')
    haproxy_dict = {}
    section_dict = {}
    for line in content:
        line = line.strip()
        if line.startswith('#') or line == '':
            continue
        values = line.split(None, 1)
        if values[0] in SECTION_NAMES:
            section_dict = {}
            i_key = values[0] if len(values) == 1 else values[0] + ' ' + values[1]
            haproxy_dict.update({i_key: section_dict})
        elif len(values) == 1:
            section_dict[line] = ''
        else:
            attr_key = values[0]
            attr_value = values[1]
            if attr_key in section_dict:
                if not isinstance(section_dict[attr_key], list):
                    section_dict[attr_key] = [
                     section_dict[attr_key]]
                section_dict[attr_key].append(attr_value)
            else:
                section_dict[attr_key] = attr_value

    return haproxy_dict


@parser(Specs.haproxy_cfg)
class HaproxyCfg(Parser):
    """Class to parse file ``haproxy.cfg``."""

    def parse_content(self, content):
        self.data = _parse_content(content)