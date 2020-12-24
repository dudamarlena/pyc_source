# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/luc_t_000/projects/freepybox/freepybox/freepybox.py
# Compiled at: 2018-04-25 17:31:21
# Size of source mod 2**32: 9062 bytes
import asyncio, hmac, ipaddress, os, json, logging, socket, ssl, time
from urllib.parse import urljoin
import aiohttp, freepybox
from freepybox.exceptions import *
from freepybox.access import Access
from freepybox.api.system import System
from freepybox.api.dhcp import Dhcp
from freepybox.api.switch import Switch
from freepybox.api.lan import Lan
from freepybox.api.wifi import Wifi
from freepybox.api.fs import Fs
from freepybox.api.call import Call
token_filename = 'app_auth'
token_dir = os.path.dirname(os.path.abspath(__file__))
token_file = os.path.join(token_dir, token_filename)
app_desc = {'app_id':'fpbx', 
 'app_name':'freepybox', 
 'app_version':freepybox.__version__, 
 'device_name':socket.gethostname()}
logger = logging.getLogger(__name__)

class Freepybox:

    def __init__(self, app_desc=app_desc, token_file=token_file, api_version='v3', timeout=10):
        self.token_file = token_file
        self.api_version = api_version
        self.timeout = timeout
        self.app_desc = app_desc

    async def open(self, host, port):
        """
        Open a session to the freebox, get a valid access module
        and instantiate freebox modules
        """
        if not self._is_app_desc_valid(self.app_desc):
            raise InvalidTokenError('invalid application descriptor')
        cert_path = os.path.join(os.path.dirname(__file__), 'freebox_root_ca.pem')
        ssl_ctx = ssl.create_default_context(cafile=cert_path)
        conn = aiohttp.TCPConnector(ssl_context=ssl_ctx)
        self.session = aiohttp.ClientSession(connector=conn)
        self._access = await self._get_freebox_access(host, port, self.api_version, self.token_file, self.app_desc, self.timeout)
        self.system = System(self._access)
        self.dhcp = Dhcp(self._access)
        self.switch = Switch(self._access)
        self.lan = Lan(self._access)
        self.wifi = Wifi(self._access)
        self.fs = Fs(self._access)
        self.call = Call(self._access)

    async def close(self):
        """
        Close the freebox session
        """
        if self._access is None:
            raise NotOpenError('Freebox is Not opened')
        await self._access.post('login/logout')
        await self.session.close()

    async def _get_freebox_access(self, host, port, api_version, token_file, app_desc, timeout=10):
        """
        Returns an access object used for HTTP requests.
        """
        base_url = self._get_base_url(host, port, api_version)
        logger.info('Read application authorization file')
        app_token, track_id, file_app_desc = self._readfile_app_token(token_file)
        if app_token is None or file_app_desc != app_desc:
            logger.info('No valid authorization file found')
            app_token, track_id = await self._get_app_token(base_url, app_desc, timeout)
            out_msg_flag = False
            status = None
            while status != 'granted':
                status = await self._get_authorization_status(base_url, track_id, timeout)
                if status == 'denied':
                    raise AuthorizationError('the app_token is invalid or has been revoked')
                elif status == 'pending':
                    if not out_msg_flag:
                        out_msg_flag = True
                        print('Please confirm the authentification on the freebox')
                    await asyncio.sleep(1)
                elif status == 'timeout':
                    raise AuthorizationError('timeout')

            logger.info('Application authorization granted')
            self._writefile_app_token(app_token, track_id, app_desc, token_file)
            logger.info('Application token file was generated : {0}'.format(token_file))
        session_token, session_permissions = await self._get_session_token(base_url, app_token, app_desc['app_id'], timeout)
        logger.info('Session opened')
        logger.info('Permissions: ' + str(session_permissions))
        fbx_access = Access(self.session, base_url, session_token, timeout)
        return fbx_access

    async def _get_authorization_status(self, base_url, track_id, timeout):
        """
        Get authorization status of the application token
        Returns:
            unknown     the app_token is invalid or has been revoked
            pending     the user has not confirmed the authorization request yet
            timeout     the user did not confirmed the authorization within the given time
            granted     the app_token is valid and can be used to open a session
            denied          the user denied the authorization request
        """
        url = urljoin(base_url, 'login/authorize/{0}'.format(track_id))
        r = await self.session.get(url, timeout=timeout)
        resp = await r.json()
        return resp['result']['status']

    async def _get_app_token(self, base_url, app_desc, timeout=10):
        """
        Get the application token from the freebox
        Returns (app_token, track_id)
        """
        url = urljoin(base_url, 'login/authorize/')
        data = json.dumps(app_desc)
        r = await self.session.post(url, data=data, timeout=timeout)
        resp = await r.json()
        if not resp.get('success'):
            raise AuthorizationError('authentification failed')
        app_token = resp['result']['app_token']
        track_id = resp['result']['track_id']
        return (
         app_token, track_id)

    def _writefile_app_token(self, app_token, track_id, app_desc, file):
        """
        Store the application token in g_app_auth_file file
        """
        d = app_desc
        d.update({'app_token':app_token,  'track_id':track_id})
        with open(file, 'w') as (f):
            json.dump(d, f)

    def _readfile_app_token(self, file):
        """
        Read the application token in g_app_auth_file file.
        Returns (app_token, track_id, app_desc)
        """
        try:
            with open(file, 'r') as (f):
                d = json.load(f)
                app_token = d['app_token']
                track_id = d['track_id']
                app_desc = {k:d[k] for k in ('app_id', 'app_name', 'app_version', 'device_name') if k in d}
                return (app_token, track_id, app_desc)
        except FileNotFoundError:
            return (None, None, None)

    async def _get_session_token(self, base_url, app_token, app_id, timeout=10):
        """
        Get session token from freebox.
        Returns (session_token, session_permissions)
        """
        challenge = await self._get_challenge(base_url, timeout)
        h = hmac.new(app_token.encode(), challenge.encode(), 'sha1')
        password = h.hexdigest()
        url = urljoin(base_url, 'login/session/')
        data = json.dumps({'app_id':app_id,  'password':password})
        r = await self.session.post(url, data=data, timeout=timeout)
        resp = await r.json()
        if not resp.get('success'):
            raise AuthorizationError('get_session_token failed')
        session_token = resp.get('result').get('session_token')
        session_permissions = resp.get('result').get('permissions')
        return (
         session_token, session_permissions)

    async def _get_challenge(self, base_url, timeout=10):
        """
        Return challenge from freebox API
        """
        url = urljoin(base_url, 'login')
        r = await self.session.get(url, timeout=timeout)
        resp = await r.json()
        if not resp.get('success'):
            raise AuthorizationError('get_challenge failed')
        return resp['result']['challenge']

    def _get_base_url(self, host, port, freebox_api_version):
        """
        Returns base url for HTTPS requests
        :return:
        """
        return 'https://{0}:{1}/api/{2}/'.format(host, port, freebox_api_version)

    def _is_app_desc_valid(self, app_desc):
        """
        Check validity of the application descriptor
        """
        return all(k in app_desc for k in ('app_id', 'app_name', 'app_version', 'device_name'))