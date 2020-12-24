# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/comet/comet.py
# Compiled at: 2017-04-23 10:30:41
from __future__ import print_function
import getpass, hashlib, json, os, random, signal, string, sys, time, webbrowser
from builtins import input
from pprint import pprint
import requests
from requests.auth import HTTPBasicAuth
from httpsig.requests_auth import HTTPSignatureAuth
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.util import banner
from cloudmesh_client.shell.console import Console
requests.packages.urllib3.disable_warnings()

class Comet(object):
    endpoint = ''
    base_uri = ''
    api_version = ''
    local_base_uri = 'https://localhost:8443/nucleus'
    auth_uri = ('{}/rest-auth').format(base_uri)
    local_auth_uri = ('{}/rest-auth').format(local_base_uri)
    tunnelled = False
    auth_provider = None
    token = None
    api_key = None
    api_secret = None
    api_auth = None
    HEADER = {'content-type': 'application/json'}
    AUTH_HEADER = {'content-type': 'application/json'}
    verify = False

    @staticmethod
    def set_endpoint(endpoint):
        Comet.endpoint = endpoint

    @staticmethod
    def set_base_uri(uri):
        Comet.base_uri = uri
        Comet.auth_uri = Comet.base_uri + '/rest-auth'

    @staticmethod
    def set_api_version(api_version):
        Comet.api_version = '/%s' % api_version

    @staticmethod
    def url(path):
        if Comet.tunnelled:
            url = Comet.local_base_uri + Comet.api_version + '/' + path
        else:
            url = Comet.base_uri + Comet.api_version + '/' + path
        return url

    def __init__(self):
        pass

    @staticmethod
    def docs():
        webbrowser.open(('{}/docs/#!/v1').format(Comet.base_uri))

    @staticmethod
    def tunnel(start):
        if start:
            Comet.tunnelled = True
            command = 'ssh -L 8443:localhost:443 nucleus'
            os.system(command)
        else:
            Comet.kill_tunnel()

    @staticmethod
    def kill_tunnel():
        pid = Comet.find_tunnel()
        if pid is None:
            Console.error('No tunnel to comet found')
        else:
            Console.ok('Killing the tunnel to comet')
            os.kill(pid, signal.SIGTERM)
        return

    @staticmethod
    def state():
        pid = Comet.find_tunnel()
        Console.ok(('Comet tunnel: {:}').format(pid))

    @staticmethod
    def is_tunnel():
        pid = Comet.find_tunnel()
        return pid is not None

    @staticmethod
    def find_tunnel():
        r = Shell.execute('ps', ['-ax']).split('\n')
        pid = None
        info = None
        for line in r:
            if 'localhost' in line and 'nucleus' in line or 'comet' in line and 'tunnel' in line and 'status' not in line:
                info = line.strip()
                break

        if info:
            pid = int(info.split(' ', 1)[0])
        return pid

    @staticmethod
    def get_nonce():
        nonce = ('').join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        return nonce

    @classmethod
    def set_auth_provider(cls, auth_provider=None):
        if not auth_provider:
            config = ConfigDict('cloudmesh.yaml')
            cometConf = config['cloudmesh.comet']
            auth_provider = cometConf['endpoints'][cls.endpoint]['auth_provider'].upper()
            if not auth_provider:
                auth_provider = 'USERPASS'
        cls.auth_provider = auth_provider

    @classmethod
    def logon(cls, endpoint=None, username=None, password=None):
        config = ConfigDict('cloudmesh.yaml')
        cometConf = config['cloudmesh.comet']
        if endpoint:
            cls.set_endpoint(endpoint)
        else:
            cls.set_endpoint(cometConf['active'])
        cls.set_base_uri(cometConf['endpoints'][cls.endpoint]['nucleus_base_url'])
        cls.set_api_version(cometConf['endpoints'][cls.endpoint]['api_version'])
        if not cls.auth_provider:
            cls.set_auth_provider()
        ret = False
        if 'USERPASS' == cls.auth_provider:
            if username is None:
                username = cometConf['endpoints'][cls.endpoint]['userpass']['username']
                if username == '' or username == 'TBD':
                    username = cometConf['username']
            if password is None:
                password = cometConf['endpoints'][cls.endpoint]['userpass']['password']
                if password.lower() == 'readline':
                    password = getpass.getpass()
                elif password.lower() == 'env':
                    password = os.environ.get('COMET_PASSWORD', getpass.getpass())
            if cls.token is None:
                if cls.auth_uri:
                    if cls.tunnelled:
                        authuri = '%s/login/' % cls.local_auth_uri
                    else:
                        authuri = '%s/login/' % cls.auth_uri
                    data = {'username': username, 'password': password}
                    r = requests.post(authuri, data=json.dumps(data), headers=cls.HEADER, verify=cls.verify)
                    try:
                        cls.token = r.json()['key']
                        cls.AUTH_HEADER['Authorization'] = ('Token {:}').format(cls.token)
                    except:
                        ret = False

                    ret = cls.token
            else:
                ret = cls.token
        elif 'APIKEY' == cls.auth_provider:
            cls.api_key = cometConf['endpoints'][cls.endpoint]['apikey']['api_key']
            cls.api_secret = cometConf['endpoints'][cls.endpoint]['apikey']['api_secret']
            cls.api_auth = HTTPSignatureAuth(secret=cls.api_secret, headers=['nonce', 'timestamp'])
            if cls.api_key and cls.api_secret and cls.api_auth:
                ret = True
        else:
            print('The specified AUTH Provider Not Currently Supported')
        return ret

    @classmethod
    def logoff(cls):
        ret = True
        if 'USERPASS' == cls.auth_provider:
            if cls.token:
                if cls.auth_uri:
                    authuri = '%s/logout/' % cls.auth_uri
                    header = dict(cls.HEADER)
                    header['Authorization'] = 'Token %s' % cls.token
                    r = requests.post(authuri, headers=header, verify=cls.verify)
                    cls.token = None
                    cls.AUTH_HEADER = cls.HEADER
                else:
                    ret = False
        return ret

    @classmethod
    def status(cls):
        ret = True
        if 'USERPASS' == cls.auth_provider and cls.token is None:
            ret = False
        return ret

    @staticmethod
    def get(url, headers=None, allow_redirects=True, data=None, authuser=None, authpass=None):
        return Comet.http(url, action='get', headers=headers, data=data, authuser=authuser, authpass=authpass, allow_redirects=allow_redirects)

    @staticmethod
    def post(url, headers=None, data=None, md5=None, files=None, cacert=True, allow_redirects=True):
        return Comet.http(url, action='post', headers=headers, data=data, files=files, md5=md5, cacert=cacert, allow_redirects=allow_redirects)

    @staticmethod
    def put(url, headers=None, data=None, allow_redirects=True):
        return Comet.http(url, action='put', headers=headers, data=data, allow_redirects=allow_redirects)

    @staticmethod
    def http(url, action='get', headers=None, data=None, authuser=None, authpass=None, files=None, md5=None, cacert=True, allow_redirects=True):
        ret = None
        if Comet.tunnelled:
            cacert = False
        if 'USERPASS' == Comet.auth_provider:
            if headers is None:
                headers = Comet.AUTH_HEADER
            if 'post' == action:
                if files:
                    del headers['content-type']
                    headers['md5'] = md5
                    r = requests.post(url, headers=headers, files=files, allow_redirects=allow_redirects, verify=cacert)
                else:
                    r = requests.post(url, headers=headers, data=json.dumps(data), allow_redirects=allow_redirects, verify=cacert)
            elif 'put' == action:
                r = requests.put(url, headers=headers, data=json.dumps(data), allow_redirects=allow_redirects, verify=cacert)
            elif data:
                if authuser and authpass:
                    r = requests.get(url, headers=headers, params=data, auth=(
                     authuser, authpass), allow_redirects=allow_redirects, verify=cacert)
                else:
                    r = requests.get(url, headers=headers, params=data, allow_redirects=allow_redirects, verify=cacert)
            elif authuser and authpass:
                r = requests.get(url, headers=headers, auth=(
                 authuser, authpass), allow_redirects=allow_redirects, verify=cacert)
            else:
                r = requests.get(url, headers=headers, allow_redirects=allow_redirects, verify=cacert)
            if r.status_code == 303:
                ret = r.headers['Location']
            elif r.status_code == 200:
                try:
                    ret = r.json()
                except:
                    ret = r.text

            elif r.status_code == 204:
                ret = ''
            elif r.status_code == 201:
                finished = False
                newurl = r.headers['Location']
                while not finished:
                    ret = requests.get(newurl, headers=headers)
                    try:
                        ret = ret.json()
                    except:
                        pass

                    if 'status' not in ret:
                        finished = True
                    else:
                        time.sleep(1)

            elif r.status_code == 401:
                ret = {'error': 'Not Authenticated'}
            elif r.status_code == 403:
                ret = {'error': 'Permission denied'}
            elif r.status_code == 400:
                ret = {'error': '%s' % r.text}
        elif 'APIKEY' == Comet.auth_provider:
            headers = {'content-type': 'application/json', 'timestamp': str(int(time.time())), 'nonce': Comet.get_nonce(), 
               'X-Api-Key': Comet.api_key}
            if 'post' == action:
                if files:
                    headers = {'timestamp': str(int(time.time())), 'nonce': Comet.get_nonce(), 'X-Api-Key': Comet.api_key, 
                       'md5': md5}
                    r = requests.post(url, auth=Comet.api_auth, headers=headers, files=files, allow_redirects=allow_redirects, verify=cacert)
                else:
                    r = requests.post(url, auth=Comet.api_auth, headers=headers, data=json.dumps(data), allow_redirects=allow_redirects, verify=cacert)
            elif 'put' == action:
                r = requests.put(url, auth=Comet.api_auth, headers=headers, data=json.dumps(data), allow_redirects=allow_redirects, verify=cacert)
            elif data:
                r = requests.get(url, auth=Comet.api_auth, headers=headers, params=data, allow_redirects=allow_redirects, verify=cacert)
            else:
                r = requests.get(url, auth=Comet.api_auth, headers=headers, allow_redirects=allow_redirects, verify=cacert)
            ret = None
            if r.status_code == 303:
                ret = r.headers['Location']
            elif r.status_code == 200:
                try:
                    ret = r.json()
                except:
                    ret = r.text

            elif r.status_code == 204:
                ret = ''
            elif r.status_code == 201:
                finished = False
                newurl = r.headers['Location']
                headers['timestamp'] = str(int(time.time()))
                headers['nonce'] = Comet.get_nonce()
                while not finished:
                    ret = requests.get(newurl, auth=Comet.api_auth, headers=headers)
                    try:
                        ret = ret.json()
                    except:
                        pass

                    if 'status' not in ret:
                        finished = True
                    else:
                        time.sleep(1)

            elif r.status_code == 401:
                try:
                    ret = r.json()
                    ret = {'error': ret}
                except:
                    pass

                if not ret:
                    ret = {'error': 'Not Authenticated'}
            elif r.status_code == 403:
                try:
                    ret = r.json()
                    ret = {'error': ret}
                except:
                    pass

                if not ret:
                    ret = {'error': 'Permission denied'}
            elif r.status_code == 400:
                try:
                    ret = r.json()
                    ret = {'error': ret}
                except:
                    pass

                if not ret:
                    ret = {'error': '%s' % r.text}
        return ret

    @staticmethod
    def get_computeset(id=None, state=None):
        if not id:
            if not state:
                state = 'running'
            params = {'state': state}
            geturl = Comet.url('computeset/')
            r = Comet.get(geturl, data=params)
        else:
            geturl = Comet.url(('computeset/{}/').format(id))
            r = Comet.get(geturl)
        return r

    @staticmethod
    def console_url(clusterid, nodeid=None):
        config = ConfigDict('cloudmesh.yaml')
        cometConf = config['cloudmesh.comet']
        defaultUser = cometConf['username']
        user = None
        if defaultUser and 'TBD' != defaultUser:
            user = defaultUser
        else:
            user = input('Enter comet nucleus username: ')
        password = getpass.getpass('Enter comet nucleus password: ')
        return_url = None
        Comet.set_auth_provider(auth_provider='USERPASS')
        Comet.logon()
        if not nodeid:
            url = Comet.url(('cluster/{}/frontend/console/').format(clusterid))
        else:
            url = Comet.url(('cluster/{}/compute/{}/console/').format(clusterid, nodeid))
        return_url = Comet.get(url, authuser=user, authpass=password, allow_redirects=False)
        auth_provider = cometConf['endpoints'][Comet.endpoint]['auth_provider'].upper()
        Comet.set_auth_provider(auth_provider=auth_provider)
        Comet.logon()
        return return_url

    @staticmethod
    def console(clusterid, nodeid=None, linkonly=False):
        url = Comet.console_url(clusterid, nodeid)
        if url:
            if 'error' in url:
                Console.error(url['error'], traceflag=False)
            else:
                newurl_esc = url.replace('&', '\\&')
                print(('Console URL: {}').format(url))
                if not linkonly:
                    if 'darwin' == sys.platform:
                        os.system(('open {}').format(newurl_esc))
                    elif 'linux2' == sys.platform:
                        os.system(('firefox {} &').format(newurl_esc))
                    else:
                        Console.error('No supportted OS/browser detected!Use the above url manually in your brower:\n', traceflag=False)
        else:
            Console.error('Console URL not available.Please make sure the node is running and try again!', traceflag=False)

    @staticmethod
    def md5(fname):
        hash = hashlib.md5()
        with open(fname, 'rb') as (f):
            for chunk in iter(lambda : f.read(4096), ''):
                hash.update(chunk)

        return hash.hexdigest()

    @staticmethod
    def list_iso():
        ret = ''
        url = Comet.url('image')
        r = Comet.get(url)
        if r is not None:
            ret = r
        return ret

    @staticmethod
    def upload_iso(filename, filepath):
        ret = ''
        posturl = Comet.url('image')
        r = None
        md5 = Comet.md5(filepath)
        with open(filepath, 'rb') as (fh):
            files = {'file': (filename, fh)}
            print('File to be uploaded: %s' % filename)
            r = Comet.post(posturl, files=files, md5=md5)
            if r is not None:
                ret = r
        return ret

    @staticmethod
    def get_apikey(endpoint):
        config = ConfigDict('cloudmesh.yaml')
        cometConf = config['cloudmesh.comet']
        defaultUser = cometConf['username']
        user = input('Comet nucleus username [%s]: ' % defaultUser)
        if not user:
            user = defaultUser
        password = getpass.getpass()
        keyurl = '%s/getkey' % cometConf['endpoints'][endpoint]['nucleus_base_url']
        headers = {'ACCEPT': 'application/json'}
        try:
            r = requests.get(keyurl, headers=headers, auth=HTTPBasicAuth(user, password))
            if r.status_code == 200:
                keyobj = r.json()
                api_key = keyobj['key_name']
                api_secret = keyobj['key']
                config = ConfigDict('cloudmesh.yaml')
                config.data['cloudmesh']['comet']['endpoints'][endpoint]['auth_provider'] = 'apikey'
                config.data['cloudmesh']['comet']['endpoints'][endpoint]['apikey']['api_key'] = api_key
                config.data['cloudmesh']['comet']['endpoints'][endpoint]['apikey']['api_secret'] = api_secret
                config.save()
                Console.ok('api key retrieval and set was successful!')
            else:
                Console.error('Error getting api key. Please check your username/password', traceflag=False)
        except ConnectionError:
            Console.error('Error getting api key. The nucleus service may be unvailable', traceflag=False)


def main():
    comet = Comet()
    print(comet.status())
    print(comet.logon())
    print(comet.status())
    print(comet.logoff())
    print(comet.status())
    print(comet.logoff())


def test_get_cluster_list():
    token = ''
    banner('TEST 1: Get without logon')
    authheader = {'content-type': 'application/json', 'Authorization': 'Token %s' % token}
    geturl = 'https://localhost:8443/nucleus/v1/cluster/'
    r = requests.get(geturl, headers=authheader, verify=False)
    pprint(r.json())
    banner('TEST 2: Auth and then get cluster list')
    comet = Comet()
    Comet.tunnelled = True
    token = comet.logon()
    authheader = {'content-type': 'application/json', 'Authorization': 'Token %s' % token}
    geturl = 'https://localhost:8443/nucleus/v1/'
    geturl1 = ('{}cluster/').format(geturl)
    r = Comet.get(geturl1, headers=authheader)
    pprint(r)
    banner("TEST 3a: Get cluster 'OSG'")
    geturl1 = '%scluster/%s' % (geturl, 'osg/')
    r1 = Comet.get(geturl1, headers=authheader)
    pprint(r1)
    banner("\nTEST 3b: Get cluster 'vc2' via tunnel")
    geturl1 = '%scluster/%s' % (geturl, 'vc2/')
    r1 = Comet.get(geturl1, headers=authheader)
    pprint(r1)
    banner("\nTEST 3c: Get cluster 'vc2' directly")
    Comet.tunnelled = False
    geturl1 = Comet.url('cluster/vc2/')
    r1 = Comet.get(geturl1, headers=authheader)
    pprint(r1)
    banner('TEST 4: Get compute nodes sets')
    Comet.tunnelled = True
    r1 = Comet.get_computeset()
    pprint(r1)
    banner('TEST 4a: Get compute nodes set with id')
    r1 = Comet.get_computeset(46)
    pprint(r1)
    banner('TEST 10: logoff and get cluster list again')
    comet.logoff()
    authheader = {'content-type': 'application/json', 'Authorization': 'Token %s' % token}
    geturl = 'https://localhost:8443/nucleus/v1/cluster/'
    r = requests.get(geturl, headers=authheader, verify=False)
    pprint(r.json())


def test_power_nodes(action='on'):
    banner('TEST: power on/off a list of nodes')
    banner('Authenticating...')
    comet = Comet()
    Comet.tunnelled = True
    token = comet.logon()
    authheader = {'content-type': 'application/json', 'Authorization': 'Token %s' % token}
    url = 'https://localhost:8443/nucleus/v1/'
    vcname = 'vc2'
    vmnames = ['vm-vc2-0', 'vm-vc2-1']
    vmhosts = {vmnames[0]: 'comet-01-05', 
       vmnames[1]: 'comet-01-06'}
    data = {'computes': [ {'name': vm, 'host': vmhosts[vm]} for vm in vmnames ], 'cluster': '%s' % vcname}
    if 'on' == action:
        banner('Issuing request to poweron nodes...')
        posturl = ('{}/computeset/').format(url)
        r = Comet.http(posturl, action='post', headers=authheader, data=data)
        banner('RETURNED RESULTS:')
        print(r)
    elif 'off' == action:
        computesetid = 33
        banner('Issuing request to poweroff nodes...')
        puturl = '%s/computeset/%s/poweroff' % (url, computesetid)
        r = Comet.http(puturl, action='put', headers=authheader)
        banner('RETURNED RESULTS:')
        print(r)
    else:
        print('The Specified Power Action NOT Supported!')


if __name__ == '__main__':
    test_get_cluster_list()
    test_power_nodes('off')
    test_power_nodes()