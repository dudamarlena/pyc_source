# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snafulib/executors/docker.py
# Compiled at: 2018-07-01 01:56:00
# Size of source mod 2**32: 2480 bytes
import requests, os, configparser, time, random
container = 'jszhaw/snafu'
endpoints = {}
multi = 3
authorised = True

def launch(tenant, portnum):
    authmount = ''
    if authorised:
        accdb = os.path.expanduser('~/.snafu-accounts')
        accdir = os.path.expanduser('~/.snafu-accounts-tenants/{}'.format(tenant))
        if os.getenv('HOME') == '/':
            accdb = '/root/.snafu-accounts'
            accdir = '/root/.snafu-accounts-tenants/{}'.format(tenant)
        c = configparser.ConfigParser()
        try:
            c.read(accdb)
        except:
            pass
        else:
            sections = c.sections()
            secretkey = None
            for section in sections:
                ckeyid = c.get(section, 'access_key_id')
                if ckeyid == tenant:
                    secretkey = c.get(section, 'secret_access_key')
                    break

            if secretkey:
                authmount = '-v {}:/root/.aws'.format(accdir)
                os.makedirs(accdir, exist_ok=True)
                c = configparser.ConfigParser()
                acc = 'default'
                c.add_section(acc)
                c.set(acc, 'aws_access_key_id', tenant)
                c.set(acc, 'aws_secret_access_key', secretkey)
                f = open('{}/credentials'.format(accdir), 'w')
                c.write(f)
                f.close()
                c = configparser.ConfigParser()
                acc = 'default'
                c.add_section(acc)
                c.set(acc, 'region', 'invalid')
                f = open('{}/config'.format(accdir), 'w')
                c.write(f)
                f.close()
    dockercmd = 'docker run -d -p 127.0.0.1:{}:10000 -v /opt/functions-tenants/{}:/opt/functions-local {} {}'.format(portnum, tenant, authmount, container)
    os.system(dockercmd)


def executecontrol(flaskrequest, tenant):
    if tenant not in endpoints:
        if multi:
            endpoints[tenant] = []
            for i in range(multi):
                entries = sum([len(x) if type(x) == list else 1 for x in endpoints.values()])
                portnum = 10000 + entries + 1
                endpoints[tenant].append('http://localhost:{}'.format(portnum))
                launch(tenant, portnum)

        else:
            entries = len(endpoints)
            portnum = 10000 + entries + 1
            endpoints[tenant] = 'http://localhost:{}'.format(portnum)
            launch(tenant, portnum)
        time.sleep(2)
    endpoint = endpoints[tenant]
    if multi:
        endpoint = random.choice(endpoint)
    headers = {}
    headers['X-Amz-Date'] = flaskrequest.headers.get('X-Amz-Date')
    data = flaskrequest.data.decode('utf-8')
    reply = requests.post(endpoint + flaskrequest.path, data=data, headers=headers)
    if reply.status_code == 200:
        return reply.content.decode('utf-8')
    else:
        return