# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/sandbox_api/sandbox.py
# Compiled at: 2020-05-04 08:09:32
# Size of source mod 2**32: 7676 bytes
import io, json, os
from typing import BinaryIO, Optional, Union
import requests
from .exceptions import status_exceptions

class Sandbox:
    __doc__ = "Interface a Sandbox server.\n    \n    Attribute other than 'url' are retrieved from the sandbox at first access, attribute are\n    separated in two categories, specifications and libraries. Every attribute of one category are\n    retrieved the first time an attribute of the corresponding category is accessed.\n    \n    These attributes are fetch through HTTP requests, this can take some times (should be no more\n    than seconds), especially for the libraries category.\n    \n    Note that attributes are cached (except for 'containers'), and subsequent access to one category\n    are instantaneous.\n    \n    Attributes:\n        url (str): URL of the sandbox\n        \n        # Specifications\n        sandbox_version (str): Version of the sandbox formatted as 'MAJOR.MINOR.PATCH'.\n        docker_version (str): Version of docker used by the sandbox formatted as 'MAJOR.MINOR.PATCH'\n        containers (dict): Dict containing the status of the containers running on the sandbox.\n        memory (dict): Memory limits for each containers on the sandbox.\n        cpu (dict): CPU information for each containers on the sandbox.\n        environ (dict): Environments variables use in the containers.\n        execute_timeout (Union[int, float]): Time in seconds before an 'execute/' request timeout.\n        expiration (int): Time in before an environment expire on the sandbox.\n        \n        # Libraries\n        python3 (str): Version of python3 used by the sandbox formatted as 'MAJOR.MINOR.PATCH'.\n        python2 (str): Version of python2 used by the sandbox formatted as 'MAJOR.MINOR.PATCH'.\n        java (str): Version of java used by the sandbox formatted as 'JDK MAJOR.MINOR'.\n        gcc (str): Version of gcc used by the sandbox formatted as 'MAJOR.MINOR.PATCH'.\n        gpp (str): Version of g++ used by the sandbox formatted as 'MAJOR.MINOR.PATCH'.\n        perl (str): Version of perl used by the sandbox formatted as 'MAJOR.MINOR.PATCH'.\n        postgres (str): Version of postgres used by the sandbox formatted as 'MAJOR.MINOR'.\n        libraries (dict): Dict containing :\n            system (dict): The installed packages (dpkg).\n            c (dict): The installed libraries and their version.\n            python (dict): The installed python modules.\n            perl (dict): The installed perl modules.\n        bin (dict): Every command available in PATH on the sandbox\n    "
    sandbox_version: str
    sandbox_version: str
    docker_version: str
    containers: dict
    memory: dict
    cpu: dict
    environ: dict
    execute_timeout: Union[(int, float)]
    expiration: int
    python3: str
    python2: str
    java: str
    gcc: str
    gpp: str
    perl: str
    postgres: str
    libraries: dict
    bin: dict
    _endpoints = {'specs':'specifications/', 
     'libs':'libraries/', 
     'environments':'environments/%s/', 
     'files':'files/%s/%s/', 
     'execute':'execute/'}
    _specs = [
     'sandbox_version',
     'docker_version',
     'containers',
     'cpu',
     'memory',
     'environ',
     'execute_timeout',
     'expiration']
    _libs = [
     'python3',
     'python2',
     'java',
     'gcc',
     'gpp',
     'perl',
     'postgres',
     'libraries',
     'bin']

    def __init__(self, url: str):
        self.url = url
        for prop in self._specs + self._libs:
            setattr(self.__class__, prop, self._property(prop))

    @staticmethod
    def _property(attribute: str):
        """Wraps specification's and libraries' attribute to be fetch from the Sandbox at first
        access.
        
        'containers' attribute is also refreshed every time."""

        def getter(self):
            if attribute == 'containers':
                self._fetch('specs')
            else:
                if (hasattr(self, '_' + attribute) or attribute) in self._libs:
                    self._fetch('libs')
                else:
                    self._fetch('specs')
            return getattr(self, '_' + attribute)

        def setter(self, value):
            setattr(self, '_' + attribute, value)

        def deleter(self):
            delattr(self, '_' + attribute)

        if attribute == 'containers':
            docstring = 'Fetch containers from the sandbox.'
        else:
            docstring = 'Fetch %s from the sandbox the first time it is accessed.' % attribute
        return property(getter, setter, deleter, docstring)

    def _build_url(self, endpoint: str, *args: str):
        """Build the url corresponding to <endpoint> with the given <args>."""
        return os.path.join(self.url, self._endpoints[endpoint] % tuple(args))

    def _fetch(self, endpoint: str):
        """Retrieve the json of <endpoint> and set attributes of self according to the json."""
        response = requests.get(self._build_url(endpoint))
        if response.status_code != 200:
            raise status_exceptions(response)
        for k, v in response.json().items():
            if k == 'g++':
                k = 'gpp'
            setattr(self, '_' + k, v)

    def usage(self) -> float:
        """Returns a float between 0 and 1, indicating the current charge on the sandbox.
        
        0 means that the sandbox is currently unused, 1 means that it is used a full capacity and
        an 'execute/' request will probably be delayed."""
        return self.containers['running'] / self.containers['total']

    def download(self, uuid: str, path: str=None) -> BinaryIO:
        """Download an environment or a specific file inside an environment."""
        if path is None:
            url = self._build_url('environments', uuid)
        else:
            url = self._build_url('files', uuid, path)
        response = requests.get(url)
        if response.status_code != 200:
            raise status_exceptions(response)
        return io.BytesIO(response.content)

    def check(self, uuid: str, path: str=None) -> bool:
        """Check if an environment or a specific file inside an environment exists."""
        if path is None:
            url = self._build_url('environments', uuid)
        else:
            url = self._build_url('files', uuid, path)
        response = requests.head(url)
        if response.status_code not in (200, 404):
            raise status_exceptions(response)
        return response.status_code == 200

    def execute(self, config: Union[dict], environ: Optional[BinaryIO]=None) -> dict:
        """Execute commands on the sandbox according to <config> and <environment>, returning
        the response's json as a dict."""
        files = {'environment': environ} if environ is not None else None
        response = requests.post((self._build_url('execute')),
          data={'config': json.dumps(config)},
          files=files)
        if response.status_code != 200:
            raise status_exceptions(response)
        return response.json()