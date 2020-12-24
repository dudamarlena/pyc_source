# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/executors/proxy.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 1068 bytes
import requests, os, configparser

def executecontrol(flaskrequest, tenant):
    endpoint = None
    if tenant:
        c = configparser.ConfigParser()
        try:
            accdb = os.path.expanduser('~/.snafu-accounts')
            if os.getenv('HOME') == '/':
                accdb = '/root/.snafu-accounts'
            c.read(accdb)
        except:
            return

        sections = c.sections()
        for section in sections:
            ckeyid = c.get(section, 'access_key_id')
            if ckeyid == tenant:
                endpoint = c.get(section, 'endpoint')
                break

    else:
        config = configparser.ConfigParser()
        config.read('snafu.ini')
    if 'snafu' in config and 'executor.proxy' in config['snafu']:
        endpoint = config['snafu']['executor.proxy']
    if not endpoint:
        return
    else:
        headers = {}
        headers['X-Amz-Date'] = flaskrequest.headers.get('X-Amz-Date')
        data = flaskrequest.data.decode('utf-8')
        reply = requests.post(endpoint + flaskrequest.path, data=data, headers=headers)
        if reply.status_code == 200:
            return reply.content.decode('utf-8')
        return