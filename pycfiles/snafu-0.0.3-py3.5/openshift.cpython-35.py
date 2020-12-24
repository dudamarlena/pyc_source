# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/executors/openshift.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 1255 bytes
import requests, os, configparser, subprocess
container = 'jszhaw/snafu'
endpoints = {}

def executecontrol(flaskrequest, tenant):
    if tenant not in endpoints:
        username = os.getenv('OPENSHIFT_USERNAME')
        password = os.getenv('OPENSHIFT_PASSWORD')
        password = os.getenv('OPENSHIFT_PROJECT')
        if not username or not password or not project:
            return
        os.system('oc login https://console.appuio.ch/ --username={} --password={}'.format(username, password))
        os.system('oc project {}'.format(project))
        os.system('oc new-app --name snafu-{} jszhaw/snafu'.format(tenant))
        p = subprocess.run('oc status | grep svc/snafu-{} | cut -d  -f 3'.format(tenant), shell=True, stdout=subprocess.PIPE)
        endpoints[tenant] = 'http://{}'.format(p.decode('utf-8'))
    endpoint = endpoints[tenant]
    headers = {}
    headers['X-Amz-Date'] = flaskrequest.headers.get('X-Amz-Date')
    data = flaskrequest.data.decode('utf-8')
    reply = requests.post(endpoint + flaskrequest.path, data=data, headers=headers)
    if reply.status_code == 200:
        return reply.content.decode('utf-8')
    else:
        return