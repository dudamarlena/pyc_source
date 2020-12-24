# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/lib/request_util.py
# Compiled at: 2007-10-25 20:13:17
""" This module is mostly there to avoid circular import in the model. """
from pylons import request, c, session, config
import urllib2, iplib
from datetime import timedelta

def get_client_ip():
    try:
        if config['nb_site_proxy'] == 0:
            return request.environ['REMOTE_ADDR']
        addr_lst = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ['REMOTE_ADDR'])
        return addr_lst.split(',')[(-config['nb_site_proxy'])].strip()
    except KeyError:
        return '127.0.0.1'
    except TypeError:
        return '127.0.0.1'


def get_client_int_ip():
    return int(iplib.convert(get_client_ip(), iplib.IP_DEC))


def site_base():
    return config['global_conf']['site_base']


def site_name():
    return config['global_conf']['site_name']


def taguri(date, namespace, id=None):
    """ Return a valid unique URI that is good for Atom feeds """
    domain = urllib2.urlparse.urlparse(site_base())[1].split(':')[0]
    datestr = date.date().isoformat()
    if id:
        return 'tag:%s,%s:%s-%s' % (domain, datestr, namespace, id)
    else:
        return 'tag:%s,%s:%s' % (domain, datestr, namespace)


def parse_timedelta(val):
    val = val.strip()
    if not val:
        return timedelta()
    days = 0
    if val.endswith('d'):
        days = float(val[:-1])
    secs = 0
    if val.endswith('h'):
        secs = float(val[:-1]) * 3600
    elif val.endswith('m'):
        secs = float(val[:-1]) * 60
    elif val.endswith('s'):
        secs = float(val[:-1])
    else:
        secs = float(val[:-1])
    return timedelta(days=days, seconds=secs)