# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pti7pv2_/pip/pip/_internal/network/session.py
# Compiled at: 2020-02-14 17:24:43
# Size of source mod 2**32: 14702 bytes
"""PipSession and supporting code, containing all pip-specific
network request configuration and behavior.
"""
import email.utils, json, logging, mimetypes, os, platform, sys, warnings
from pip._vendor import requests, six, urllib3
from pip._vendor.cachecontrol import CacheControlAdapter
from pip._vendor.requests.adapters import BaseAdapter, HTTPAdapter
from pip._vendor.requests.models import Response
from pip._vendor.requests.structures import CaseInsensitiveDict
import pip._vendor.six.moves.urllib as urllib_parse
from pip._vendor.urllib3.exceptions import InsecureRequestWarning
from pip import __version__
from pip._internal.network.auth import MultiDomainBasicAuth
from pip._internal.network.cache import SafeFileCache
from pip._internal.utils.compat import has_tls, ipaddress
from pip._internal.utils.glibc import libc_ver
from pip._internal.utils.misc import build_url_from_netloc, get_installed_version, parse_netloc
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.utils.urls import url_to_path
if MYPY_CHECK_RUNNING:
    from typing import Iterator, List, Optional, Tuple, Union
    from pip._internal.models.link import Link
    SecureOrigin = Tuple[(str, str, Optional[Union[(int, str)]])]
logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore', category=InsecureRequestWarning)
SECURE_ORIGINS = [
 ('https', '*', '*'),
 ('*', 'localhost', '*'),
 ('*', '127.0.0.0/8', '*'),
 ('*', '::1/128', '*'),
 ('file', '*', None),
 ('ssh', '*', '*')]
CI_ENVIRONMENT_VARIABLES = ('BUILD_BUILDID', 'BUILD_ID', 'CI', 'PIP_IS_CI')

def looks_like_ci():
    """
    Return whether it looks like pip is running under CI.
    """
    return any((name in os.environ for name in CI_ENVIRONMENT_VARIABLES))


def user_agent():
    """
    Return a string representing the user agent.
    """
    data = {'installer':{'name':'pip', 
      'version':__version__}, 
     'python':platform.python_version(), 
     'implementation':{'name': platform.python_implementation()}}
    if data['implementation']['name'] == 'CPython':
        data['implementation']['version'] = platform.python_version()
    else:
        if data['implementation']['name'] == 'PyPy':
            if sys.pypy_version_info.releaselevel == 'final':
                pypy_version_info = sys.pypy_version_info[:3]
            else:
                pypy_version_info = sys.pypy_version_info
            data['implementation']['version'] = '.'.join([str(x) for x in pypy_version_info])
        else:
            if data['implementation']['name'] == 'Jython':
                data['implementation']['version'] = platform.python_version()
            else:
                if data['implementation']['name'] == 'IronPython':
                    data['implementation']['version'] = platform.python_version()
                elif sys.platform.startswith('linux'):
                    from pip._vendor import distro
                    distro_infos = dict(filter(lambda x: x[1], zip(['name', 'version', 'id'], distro.linux_distribution())))
                    libc = dict(filter(lambda x: x[1], zip(['lib', 'version'], libc_ver())))
                    if libc:
                        distro_infos['libc'] = libc
                    if distro_infos:
                        data['distro'] = distro_infos
                if sys.platform.startswith('darwin'):
                    if platform.mac_ver()[0]:
                        data['distro'] = {'name':'macOS', 
                         'version':platform.mac_ver()[0]}
                if platform.system():
                    data.setdefault('system', {})['name'] = platform.system()
                if platform.release():
                    data.setdefault('system', {})['release'] = platform.release()
                if platform.machine():
                    data['cpu'] = platform.machine()
                if has_tls():
                    import _ssl as ssl
                    data['openssl_version'] = ssl.OPENSSL_VERSION
                setuptools_version = get_installed_version('setuptools')
                if setuptools_version is not None:
                    data['setuptools_version'] = setuptools_version
                data['ci'] = True if looks_like_ci() else None
                user_data = os.environ.get('PIP_USER_AGENT_USER_DATA')
                if user_data is not None:
                    data['user_data'] = user_data
                return '{data[installer][name]}/{data[installer][version]} {json}'.format(data=data,
                  json=json.dumps(data, separators=(',', ':'), sort_keys=True))


class LocalFSAdapter(BaseAdapter):

    def send(self, request, stream=None, timeout=None, verify=None, cert=None, proxies=None):
        pathname = url_to_path(request.url)
        resp = Response()
        resp.status_code = 200
        resp.url = request.url
        try:
            stats = os.stat(pathname)
        except OSError as exc:
            try:
                resp.status_code = 404
                resp.raw = exc
            finally:
                exc = None
                del exc

        else:
            modified = email.utils.formatdate((stats.st_mtime), usegmt=True)
            content_type = mimetypes.guess_type(pathname)[0] or 'text/plain'
            resp.headers = CaseInsensitiveDict({'Content-Type':content_type, 
             'Content-Length':stats.st_size, 
             'Last-Modified':modified})
            resp.raw = open(pathname, 'rb')
            resp.close = resp.raw.close
        return resp

    def close(self):
        pass


class InsecureHTTPAdapter(HTTPAdapter):

    def cert_verify(self, conn, url, verify, cert):
        super(InsecureHTTPAdapter, self).cert_verify(conn=conn,
          url=url,
          verify=False,
          cert=cert)


class PipSession(requests.Session):
    timeout = None

    def __init__(self, *args, **kwargs):
        retries = kwargs.pop('retries', 0)
        cache = kwargs.pop('cache', None)
        trusted_hosts = kwargs.pop('trusted_hosts', [])
        index_urls = kwargs.pop('index_urls', None)
        (super(PipSession, self).__init__)(*args, **kwargs)
        self.pip_trusted_origins = []
        self.headers['User-Agent'] = user_agent()
        self.auth = MultiDomainBasicAuth(index_urls=index_urls)
        retries = urllib3.Retry(total=retries,
          status_forcelist=[
         500, 503, 520, 527],
          backoff_factor=0.25)
        if cache:
            secure_adapter = CacheControlAdapter(cache=(SafeFileCache(cache)),
              max_retries=retries)
        else:
            secure_adapter = HTTPAdapter(max_retries=retries)
        insecure_adapter = InsecureHTTPAdapter(max_retries=retries)
        self._insecure_adapter = insecure_adapter
        self.mount('https://', secure_adapter)
        self.mount('http://', insecure_adapter)
        self.mount('file://', LocalFSAdapter())
        for host in trusted_hosts:
            self.add_trusted_host(host, suppress_logging=True)

    def add_trusted_host(self, host, source=None, suppress_logging=False):
        """
        :param host: It is okay to provide a host that has previously been
            added.
        :param source: An optional source string, for logging where the host
            string came from.
        """
        if not suppress_logging:
            msg = 'adding trusted host: {!r}'.format(host)
            if source is not None:
                msg += ' (from {})'.format(source)
            logger.info(msg)
        else:
            host_port = parse_netloc(host)
            if host_port not in self.pip_trusted_origins:
                self.pip_trusted_origins.append(host_port)
            self.mount(build_url_from_netloc(host) + '/', self._insecure_adapter)
            host_port[1] or self.mount(build_url_from_netloc(host) + ':', self._insecure_adapter)

    def iter_secure_origins(self):
        for secure_origin in SECURE_ORIGINS:
            yield secure_origin

        for host, port in self.pip_trusted_origins:
            yield (
             '*', host, '*' if port is None else port)

    def is_secure_origin(self, location):
        parsed = urllib_parse.urlparse(str(location))
        origin_protocol, origin_host, origin_port = parsed.scheme, parsed.hostname, parsed.port
        origin_protocol = origin_protocol.rsplit('+', 1)[(-1)]
        for secure_origin in self.iter_secure_origins():
            secure_protocol, secure_host, secure_port = secure_origin
            if origin_protocol != secure_protocol:
                if secure_protocol != '*':
                    continue
            try:
                addr = ipaddress.ip_address(None if origin_host is None else six.ensure_text(origin_host))
                network = ipaddress.ip_network(six.ensure_text(secure_host))
            except ValueError:
                if origin_host:
                    if origin_host.lower() != secure_host.lower():
                        if secure_host != '*':
                            continue
            else:
                if addr not in network:
                    continue
                elif origin_port != secure_port:
                    if secure_port != '*' and secure_port is not None:
                        continue
                return True

        logger.warning("The repository located at %s is not a trusted or secure host and is being ignored. If this repository is available via HTTPS we recommend you use HTTPS instead, otherwise you may silence this warning and allow it anyway with '--trusted-host %s'.", origin_host, origin_host)
        return False

    def request(self, method, url, *args, **kwargs):
        kwargs.setdefault('timeout', self.timeout)
        return (super(PipSession, self).request)(method, url, *args, **kwargs)