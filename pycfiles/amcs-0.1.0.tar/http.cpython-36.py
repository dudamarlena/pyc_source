# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/phil/repos/python-amcrest/src/amcrest/http.py
# Compiled at: 2019-06-02 12:41:46
# Size of source mod 2**32: 6574 bytes
import logging, re, threading, requests
from .exceptions import CommError, LoginError
from .utils import clean_url, pretty
from .audio import Audio
from .event import Event
from .log import Log
from .motion_detection import MotionDetection
from .nas import Nas
from .network import Network
from .ptz import Ptz
from .record import Record
from .snapshot import Snapshot
from .special import Special
from .storage import Storage
from .system import System
from .user_management import UserManagement
from .video import Video
from .config import TIMEOUT_HTTP_PROTOCOL, MAX_RETRY_HTTP_CONNECTION
_LOGGER = logging.getLogger(__name__)

class Http(System, Network, MotionDetection, Snapshot, UserManagement, Event, Audio, Record, Video, Log, Ptz, Special, Storage, Nas):

    def __init__(self, host, port, user, password, verbose=True, protocol='http', retries_connection=None, timeout_protocol=None):
        self._token_lock = threading.Lock()
        self._host = clean_url(host)
        self._port = port
        self._user = user
        self._password = password
        self._verbose = verbose
        self._protocol = protocol
        self._base_url = self._Http__base_url()
        self._retries_default = retries_connection if retries_connection is not None else MAX_RETRY_HTTP_CONNECTION
        self._timeout_default = timeout_protocol or TIMEOUT_HTTP_PROTOCOL
        self._token = None
        self._name = None
        self._serial = None
        try:
            self._generate_token()
        except CommError:
            pass

    def _generate_token(self):
        """Create authentation to use with requests."""
        cmd = 'magicBox.cgi?action=getMachineName'
        _LOGGER.debug('%s Trying Basic Authentication', self)
        self._token = requests.auth.HTTPBasicAuth(self._user, self._password)
        try:
            resp = self._command(cmd).content.decode('utf-8')
        except LoginError:
            _LOGGER.debug('%s Trying Digest Authentication', self)
            self._token = requests.auth.HTTPDigestAuth(self._user, self._password)
            try:
                resp = self._command(cmd).content.decode('utf-8')
            except LoginError as error:
                self._token = None
                raise error

        result = resp.lower()
        if 'invalid' in result or 'error' in result:
            _LOGGER.debug('%s Result from camera: %s', self, resp.strip().replace('\r\n', ': '))
            self._token = None
            raise LoginError('Invalid credentials')
        self._name = pretty(resp.strip())
        _LOGGER.debug('%s Retrieving serial number', self)
        self._serial = pretty(self._command('magicBox.cgi?action=getSerialNo').content.decode('utf-8').strip())

    def __repr__(self):
        """Default object representation."""
        return '<{0}:{1}>'.format(self._name, self._serial)

    def as_dict(self):
        """Callback for __dict__."""
        cdict = self.__dict__.copy()
        redacted = '**********'
        cdict['_token'] = redacted
        cdict['_password'] = redacted
        return cdict

    def __base_url(self, param=''):
        return '%s://%s:%s/cgi-bin/%s' % (self._protocol, self._host,
         str(self._port), param)

    def get_base_url(self):
        return self._base_url

    def command(self, cmd, retries=None, timeout_cmd=None, stream=False):
        """
        Args:
            cmd - command to execute via http
            retries - maximum number of retries each connection should attempt
            timeout_cmd - timeout
            stream - if True do not download entire response immediately
        """
        with self._token_lock:
            if not self._token:
                self._generate_token()
        return self._command(cmd, retries, timeout_cmd, stream)

    def _command(self, cmd, retries=None, timeout_cmd=None, stream=False):
        session = requests.Session()
        url = self._Http__base_url(cmd)
        if retries is None:
            retries = self._retries_default
        for loop in range(1, 2 + retries):
            _LOGGER.debug('%s Running query attempt %s', self, loop)
            try:
                resp = session.get(url,
                  auth=(self._token),
                  stream=stream,
                  timeout=(timeout_cmd or self._timeout_default))
                if resp.status_code == 401:
                    raise LoginError
                resp.raise_for_status()
            except requests.RequestException as error:
                msg = re.sub('at 0x[0-9a-fA-F]+', 'at ADDRESS', repr(error))
                if loop > retries:
                    _LOGGER.debug('%s Query failed due to error: %s', self, msg)
                    raise CommError(error)
                _LOGGER.warning('%s Trying again due to error: %s', self, msg)
                continue

            break

        _LOGGER.debug('%s Query worked. Exit code: <%s>', self, resp.status_code)
        return resp

    def command_audio(self, cmd, file_content, http_header, timeout=None):
        with self._token_lock:
            if not self._token:
                self._generate_token()
        url = self._Http__base_url(cmd)
        try:
            requests.post(url,
              files=file_content,
              auth=(self._token),
              headers=http_header,
              timeout=(timeout or self._timeout_default))
        except requests.exceptions.ReadTimeout:
            pass