# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylxca/pylxca_api/lxca_connection.py
# Compiled at: 2020-03-12 01:38:00
# Size of source mod 2**32: 5631 bytes
__doc__ = '\n@since: 4 Sep 2015\n@author: Prashant Bhosale <pbhosale@lenovo.com>\n@license: Lenovo License\n@copyright: Copyright 2016, Lenovo\n@organization: Lenovo\n@summary: This module is for creating a connection session object for given xHMC.\n\n'
import requests, logging, json, os, platform, base64, pkg_resources
from _socket import timeout
from requests.sessions import session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
logger = logging.getLogger(__name__)

class lxcaAdapter(HTTPAdapter):

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize,
          block=block)


class Error(Exception):
    """Error"""
    pass


class ConnectionError(Error):
    """ConnectionError"""
    pass


class lxca_connection(object):
    """lxca_connection"""

    def __init__(self, url, user=None, passwd=None, verify_callback=True, retries=3):
        self.url = url
        self.user = user
        self.passwd = base64.b16encode(passwd.encode())
        self.retires = retries
        self.debug = False
        self.session = None
        if verify_callback:
            self.verify_callback = os.environ['REQUESTS_CA_BUNDLE']
        else:
            self.verify_callback = verify_callback

    def __repr__(self):
        return '%s(%s, %s, debug=%s)' % (self.__class__.__name__, repr(self.url), self.user, repr(self.debug))

    def connect(self):
        """
        connection function
        """
        try:
            logger.debug('Establishing Connection')
            self.session = requests.session()
            self.session.verify = self.verify_callback
            pylxca_version = pkg_resources.require('pylxca')[0].version
            self.session.headers.update({'content-type':'application/json; charset=utf-8',  'User-Agent':'LXCA via Python Client / ' + pylxca_version})
            payload = dict(UserId=(self.user), password=(base64.b16decode(self.passwd).decode()))
            pURL = self.url + '/sessions'
            self.session.mount(self.url, lxcaAdapter(max_retries=(self.retires)))
            r = self.session.post(pURL, data=(json.dumps(payload)), headers=dict(Referer=pURL), verify=(self.verify_callback), timeout=3)
            r.raise_for_status()
        except ConnectionError as e:
            logger.debug('Connection Exception as ConnectionError: Exception = %s', e)
            return False
        except requests.exceptions.HTTPError as e:
            logger.debug('Connection Exception as HttpError: Exception = %s', e.response.text)
            return False
        except Exception as e:
            logger.debug('Connection Exception: Exception = %s', e)
            return False

        if r.status_code == requests.codes['ok']:
            self.session.headers.update({'X-Csrf-Token': self.session.cookies.get('csrf')})
        return True

    def test_connection(self):
        """
        Test Connection from requests module
        """
        try:
            test_url = self.url + '/aicc'
            resp = self.session.get(test_url, verify=(self.session.verify), timeout=3)
            py_obj = json.loads(resp.text)
        except Exception as e:
            raise ConnectionError('Invalid connection')

    def get_url(self):
        return self.url

    def get_session(self):
        return self.session

    def disconnect(self):
        """
        session Disconnection
        """
        result = False
        try:
            delete_url = self.url + '/sessions'
            resp = self.session.delete(delete_url, verify=False, timeout=3)
            py_obj = json.loads(resp.text)
            logger.debug('Deleted session on lxca = %s', py_obj)
            result = True
        except Exception as e:
            logger.debug('Unable to delete session on lxca = %s', e)
            raise ConnectionError('Invalid connection: Connection is not Initialized')

        self.url = None
        self.user = None
        self.passwd = None
        self.debug = False
        try:
            self.session.close()
        except Exception as e:
            logger.debug('Connection with invalid session = %s', e)
            raise Exception('Invalid connection: Connection is not Initialized')

        self.session = None
        return result

    def ping(self, host):
        """
        Returns True if host responds to a ping request
        """
        ping_str = '-n 1' if platform.system().lower() == 'windows' else '-c 1'
        return os.system('ping ' + ping_str + ' ' + host) == 0