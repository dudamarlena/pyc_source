# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/eidanagios/check_EIDA_alparray.py
# Compiled at: 2020-02-10 06:48:30
# Size of source mod 2**32: 9086 bytes
"""Nagios plugin to check if Alparray data is accessible

   :Platform:
       Linux
   :Copyright:
       GEOFON, Helmholtz-Zentrum Potsdam - Deutsches GeoForschungsZentrum GFZ
       <geofon@gfz-potsdam.de>
   :License:
       GNU General Public License, Version 3, 29 June 2007

   This program is free software; you can redistribute it and/or modify it
   under the terms of the GNU General Public License as published by the Free
   Software Foundation; either version 3, or (at your option) any later
   version. For more information, see http://www.gnu.org/

.. moduleauthor:: Javier Quinteros <javier@gfz-potsdam.de>, GEOFON, GFZ Potsdam
"""
import requests, os, sys, time, datetime, random, argparse
from requests.auth import HTTPDigestAuth

def nagios_output(service, status, message, perfvalues, multiline=None, verbose=0):
    if multiline is None or not len(multiline) or not verbose:
        print('%s %s: %s | %s' % (service, status, message, perfvalues))
    else:
        print('%s %s: %s | %s\n%s' % (service, status, message, perfvalues, multiline))


def check_EIDA_Alparray(url, payload, timeout=9, token=None, verbose=0):
    """ Check if Alparray data is accessible at the node specified by url

        A file containing a token is expected in the home folder
        of the user running this script with filename '.eidatoken'
        Return 0: OK; 1: WARNING; 2: CRITICAL
    """
    if token is None:
        token = os.path.expanduser('~/.eidatoken')
    start_time = time.time()
    try:
        username, password = authenticate(url, timeout=timeout, token=token)
    except Exception as e:
        multiline = str(e) if verbose else None
        nagios_output('ALPARRAY', 'WARNING', 'Authentication failed', 'time=%fs;bytes=0B' % (time.time() - start_time), multiline)
        return 1

    urlreq = url.replace('/auth', '/queryauth').replace('https://', 'http://')
    r = requests.get(urlreq, payload, auth=(HTTPDigestAuth(username, password)))
    if r.status_code != 200:
        if verbose:
            multiline = "User: '{}'; Password: '{}'\nPayload: '{}'".format(username, password, payload)
        else:
            multiline = None
        nagios_output('ALPARRAY', 'FAILED', '%s returned a %s HTTP error code' % (urlreq, r.status_code), 'time=%fs;bytes=0B' % (time.time() - start_time), multiline)
        return 2
    else:
        nagios_output('ALPARRAY', 'OK', '%s returned %d bytes' % (urlreq, len(r.content)), 'time=%fs;bytes=%dB' % (time.time() - start_time, len(r.content)))
        return 0


def authenticate(url, timeout=9, token=None):
    """ Use the token passed in the parameter to get a username and password

        A file containing a token is expected in the home folder
        of the user running this script with filename '.eidatoken'
        Return a tuple of strings (username, password)
        Throws an Exception in case it cannot authenticate
    """
    if token is None:
        token = os.path.expanduser('~/.eidatoken')
    else:
        files = {'file': open(token, 'rb')}
        r = requests.post(url, files=files, timeout=timeout)
        if r.status_code != 200:
            raise Exception('Authentication returned a %s HTTP Error code' % r.status_code)
        resp = r.text.split(':')
        if len(resp) != 2:
            raise Exception('Authentication returned a wrong response format:\n%s' % r.text)
    return resp


def main():
    """Nagios plugin to check if Alparray data is accessible

    Following Nagios specifications, the value returned can be
    0: OK
    1: WARNING
    2: CRITICAL
    3: UNKNOWN
    and the output line is something like

    ALPARRAY OK: https://eida.bgr.de/fdsnws/dataselect/1/queryauth | time=0.133321s
    """
    version = '0.1a6'
    urls = dict()
    urls['ETH'] = 'https://eida.ethz.ch/fdsnws/dataselect/1/auth'
    urls['GFZ'] = 'https://geofon.gfz-potsdam.de/fdsnws/dataselect/1/auth'
    urls['INGV'] = 'https://webservices.ingv.it/fdsnws/dataselect/1/auth'
    urls['LMU'] = 'https://erde.geophysik.uni-muenchen.de/fdsnws/dataselect/1/auth'
    urls['ODC'] = 'https://www.orfeus-eu.org/fdsnws/dataselect/1/auth'
    urls['RESIF'] = 'https://ws.resif.fr/fdsnws/dataselect/1/auth'
    reqs = dict()
    reqs['ETH'] = {'net':'Z3',  'sta':'A291A',  'start':datetime.datetime(2018, 1, 1)}
    reqs['GFZ'] = {'net':'Z3',  'sta':'A434A',  'start':datetime.datetime(2017, 10, 1)}
    reqs['INGV'] = {'net':'Z3',  'sta':'A319A',  'start':datetime.datetime(2018, 1, 1)}
    reqs['LMU'] = {'net':'Z3',  'sta':'A369A',  'start':datetime.datetime(2018, 1, 1)}
    reqs['ODC'] = {'net':'Z3',  'sta':'A339A',  'start':datetime.datetime(2018, 1, 1)}
    reqs['RESIF'] = {'net':'Z3',  'sta':'A429A',  'start':datetime.datetime(2017, 10, 1)}
    desc = 'Nagios plugin to check if Alparray data is accessible from endpoints.\n\nIf no arguments are passed all EIDA nodes are tested.'
    parser = argparse.ArgumentParser(description=desc)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-H', '--hostname', default=None, help=('Hostname providing the "auth" and "queryauth" method at the default location. Valid values are domain names (e.g. geofon.gfz-potsdam.de) or the data centre ID (%s)' % ', '.join(reqs.keys())))
    parser.add_argument('-t', '--timeout', default=9, type=int, help='Number of seconds to be used as a timeout for the HTTP calls.')
    parser.add_argument('-a', '--authentication', default=(os.path.expanduser('~/.eidatoken')), help='File containing the token to use during the authentication process')
    parser.add_argument('-V', '--version', action='version', version=('%(prog)s ' + version), help='Show version information.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Under verbose mode more lines with details will follow the expected one-line message')
    args = parser.parse_args()
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    offset = random.sample(range(168), 1)[0]
    if args.hostname is not None:
        node = None
        if args.hostname in urls.keys():
            node = args.hostname
        else:
            for dc, url in urls.items():
                if args.hostname in url:
                    node = dc
                    break

        if node is None:
            nagios_output('ALPARRAY', 'FAILED', '%s is an unknown node' % args.hostname, 'time=0s;bytes=0B')
            sys.exit(3)
        payload = reqs[node].copy()
        auxstart = payload['start'] + datetime.timedelta(hours=offset)
        payload['start'] = auxstart.isoformat()
        payload['end'] = (auxstart + datetime.timedelta(minutes=10)).isoformat()
        sys.exit(check_EIDA_Alparray((urls[node]), payload, timeout=(args.timeout),
          token=(args.authentication),
          verbose=(args.verbose)))
    retcode = 0
    for dc, url in urls.items():
        payload = reqs[dc].copy()
        auxstart = payload['start'] + datetime.timedelta(hours=offset)
        payload['start'] = auxstart.isoformat()
        payload['end'] = (auxstart + datetime.timedelta(minutes=10)).isoformat()
        retcode = max(retcode, check_EIDA_Alparray(url, payload=payload, timeout=(args.timeout), token=(args.authentication)))

    sys.exit(retcode)


if __name__ == '__main__':
    main()