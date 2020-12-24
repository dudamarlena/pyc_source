# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/experiments/turkey.py
# Compiled at: 2015-09-30 11:20:13
import base64, centinel.primitives.http as http, centinel.primitives.dnslib as dns
from centinel.experiment import Experiment
GOOGLE_DNS = '8.8.8.8'
SEARCH_STRING = 'home network testbed will appear at'

class TurkeyExperiment(Experiment):
    name = 'turkey'

    def __init__(self, input_file):
        self.input_file = input_file
        self.results = []
        self.host = 'twitter.com'
        self.path = '/feamster/status/452889624541921280'

    def run(self):
        ips = dns.get_ips(self.host)
        if 'response1-ips' in ips:
            ips = ips['response1-ips']
        else:
            raise Exception("DNS resolution didn't yield any IP addresses.")
        blocked_ips = filter(self.is_blocked, ips)
        if not blocked_ips:
            return
        ips = dns.get_ips(self.host, nameserver=GOOGLE_DNS)
        if 'response1-ips' in ips:
            ips = ips['response1-ips']
        else:
            raise Exception("DNS resolution didn't yield any IP addresses.")
        blocked_ips = filter(self.is_blocked, ips)
        if not blocked_ips:
            return

    def is_blocked(self, ip):
        headers = {'Host': self.host}
        blocked = True
        result = http.get_request(host=ip, path=self.path, headers=headers, ssl=True)
        body = None
        if 'response' in result:
            if 'body' in result['response']:
                body = result['response']['body']
            elif 'body.b64' in result['response']:
                body = base64.b64decode(result['response']['body.b64'])
            else:
                raise Exception('HTTP GET result did not return a body.')
        else:
            raise Exception("HTTP GET results didn't contain a response.")
        blocked = SEARCH_STRING not in body
        result['blocked'] = blocked
        self.results.append(result)
        return blocked