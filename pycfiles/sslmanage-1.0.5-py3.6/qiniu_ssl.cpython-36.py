# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sslmanage/qiniu_ssl.py
# Compiled at: 2019-07-05 04:18:46
# Size of source mod 2**32: 2778 bytes
import time, qiniu, requests
from sslmanage.base import BaseSsl, log_info

class QnCertManager(BaseSsl):
    __doc__ = '\n    上传SLL证书到七牛\n    '
    HOST = 'api.qiniu.com'

    def __init__(self, root_domain, domain, cert_file, key_file, access_key, secret_key):
        super().__init__(cert_file, key_file)
        if isinstance(domain, str):
            domain = [
             domain]
        self.domain = domain
        self.root_domain = root_domain
        self.cert_file = cert_file
        self.key_file = key_file
        self.access_key = access_key
        self.secret_key = secret_key

    def handle(self, *args, **options):
        certid, ok = self.upload_ssl()
        domains = self.domain
        print(certid, ok)
        if not ok:
            log_info('upload ssl error: %s' % certid)
            return
        log_info('upload ssl success, certID: %s' % certid)
        for domain in domains:
            resp = self.replace_ssl(domain=domain, certid=certid)
            log_info('replace ssl result: %s' % resp.content)

    def upload_ssl(self):
        session = requests.Session()
        auth = qiniu.Auth(access_key=(self.access_key), secret_key=(self.secret_key))
        url = 'https://{}{}'.format(self.HOST, '/sslcert')
        token = auth.token_of_request(url)
        headers = {'Authorization':'QBox {0}'.format(token), 
         'Content-Type':'application/json', 
         'Host':self.HOST}
        self._get_ssl()
        resp = session.post(url, json={'name':'ssl{}new'.format(time.strftime('%Y%m%d', time.localtime())), 
         'common_name':self.root_domain, 
         'ca':self.cert, 
         'pri':self.cert_key},
          headers=headers)
        if resp.status_code != 200:
            return ('', False)
        else:
            cert_id = resp.json().get('certID', '')
            code = resp.json().get('code', 0)
            if cert_id:
                if code == 200:
                    return (
                     cert_id, True)
            return (
             resp.content, False)

    def replace_ssl(self, domain, certid):
        session = requests.Session()
        auth = qiniu.Auth(access_key=(self.access_key), secret_key=(self.secret_key))
        url = 'https://{}/domain/{}/httpsconf'.format(self.HOST, domain)
        token = auth.token_of_request(url)
        headers = {'Authorization':'QBox {0}'.format(token), 
         'Content-Type':'application/json', 
         'Host':self.HOST}
        resp = session.put(url, json={'certid':certid, 
         'forceHttps':False},
          headers=headers)
        return resp