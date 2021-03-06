# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gordo/.virtualenvs/coffer/lib/python2.7/site-packages/coffer/client.py
# Compiled at: 2015-01-05 12:24:33
__doc__ = '\nThis module contains functions for discovery, downloading, etc\n'
import logging, socket, requests
from zeroconf_utils import discover

def get_auth(password=None):
    if password is not None:
        return ('user', password)
    else:
        return


def get_offers(password=None):
    peers = discover()
    for p in peers:
        base = 'http://%s:%s' % (socket.inet_ntoa(p.address), p.port)
        try:
            response = requests.get('%s/offers' % base, timeout=5, auth=get_auth(password))
        except:
            logging.warning('Failure for %s' % base)
            continue

        if response.status_code == 401:
            logging.warning('Wrong password for %s' % base)
            continue
        else:
            if response.status_code != 200:
                logging.warning('Failure (%d) for %s' % (
                 response.status_code, base))
                continue
            peer_offers = response.json()['offers']
            for offer_id in peer_offers:
                url = '%s/offers/%s' % (base, offer_id)
                logging.debug('Selecting %s as candidate' % url)
                yield (offer_id, url)


def dl_offer(url, password=None):
    return requests.get(url, auth=get_auth(password), timeout=5)