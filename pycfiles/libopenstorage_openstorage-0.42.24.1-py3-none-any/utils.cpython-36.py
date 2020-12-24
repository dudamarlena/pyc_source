# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/twine/twine/utils.py
# Compiled at: 2020-01-10 16:25:25
# Size of source mod 2**32: 8926 bytes
from typing import Callable, DefaultDict, Dict, Optional
import os, os.path, functools, argparse, collections, configparser
from urllib.parse import urlparse, urlunparse
import requests
from twine import exceptions
input_func = input
DEFAULT_REPOSITORY = 'https://upload.pypi.org/legacy/'
TEST_REPOSITORY = 'https://test.pypi.org/legacy/'
RepositoryConfig = Dict[(str, Optional[str])]

def get_config(path: str='~/.pypirc') -> Dict[(str, RepositoryConfig)]:
    parser = configparser.RawConfigParser()
    index_servers = [
     'pypi', 'testpypi']
    defaults = {'username':None, 
     'password':None}
    path = os.path.expanduser(path)
    if os.path.isfile(path):
        parser.read(path)
        if parser.has_option('distutils', 'index-servers'):
            index_servers = parser.get('distutils', 'index-servers').split()
        for key in ('username', 'password'):
            if parser.has_option('server-login', key):
                defaults[key] = parser.get('server-login', key)

    config = collections.defaultdict(lambda : defaults.copy())
    config['pypi']['repository'] = DEFAULT_REPOSITORY
    if 'testpypi' in index_servers:
        config['testpypi']['repository'] = TEST_REPOSITORY
    for repository in index_servers:
        for key in ('username', 'repository', 'password', 'ca_cert', 'client_cert'):
            if parser.has_option(repository, key):
                config[repository][key] = parser.get(repository, key)

    return dict(config)


def get_repository_from_config(config_file: str, repository: str, repository_url: Optional[str]=None) -> RepositoryConfig:
    if repository_url:
        if '://' in repository_url:
            return {'repository':repository_url,  'username':None, 
             'password':None}
    else:
        if repository_url:
            if '://' not in repository_url:
                raise exceptions.UnreachableRepositoryURLDetected("Repository URL {} has no protocol. Please add 'https://'. \n".format(repository_url))
        try:
            return get_config(config_file)[repository]
        except KeyError:
            msg = "Missing '{repo}' section from the configuration file\nor not a complete URL in --repository-url.\nMaybe you have a out-dated '{cfg}' format?\nmore info: https://docs.python.org/distutils/packageindex.html#pypirc\n".format(repo=repository,
              cfg=config_file)
            raise exceptions.InvalidConfiguration(msg)


_HOSTNAMES = {'pypi.python.org', 'testpypi.python.org', 'upload.pypi.org',
 'test.pypi.org'}

def normalize_repository_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc in _HOSTNAMES:
        return urlunparse(('https', ) + parsed[1:])
    else:
        return urlunparse(parsed)


def check_status_code(response: requests.Response, verbose: bool) -> None:
    """Generate a helpful message based on the response from the repository.

    Raise a custom exception for recognized errors. Otherwise, print the
    response content (based on the verbose option) before re-raising the
    HTTPError.
    """
    if response.status_code == 410:
        if 'pypi.python.org' in response.url:
            raise exceptions.UploadToDeprecatedPyPIDetected(f"It appears you're uploading to pypi.python.org (or testpypi.python.org). You've received a 410 error response. Uploading to those sites is deprecated. The new sites are pypi.org and test.pypi.org. Try using {DEFAULT_REPOSITORY} (or {TEST_REPOSITORY}) to upload your packages instead. These are the default URLs for Twine now. More at https://packaging.python.org/guides/migrating-to-pypi-org/.")
        elif response.status_code == 405:
            if 'pypi.org' in response.url:
                raise exceptions.InvalidPyPIUploadURL(f"It appears you're trying to upload to pypi.org but have an invalid URL. You probably want one of these two URLs: {DEFAULT_REPOSITORY} or {TEST_REPOSITORY}. Check your --repository-url value.")
    else:
        try:
            response.raise_for_status()
        except requests.HTTPError as err:
            if response.text:
                if verbose:
                    print('Content received from server:\n{}'.format(response.text))
                else:
                    print('NOTE: Try --verbose to see response content.')
            raise err


def get_userpass_value(cli_value: Optional[str], config: RepositoryConfig, key: str, prompt_strategy: Optional[Callable]=None) -> Optional[str]:
    """Gets the username / password from config.

    Uses the following rules:

    1. If it is specified on the cli (`cli_value`), use that.
    2. If `config[key]` is specified, use that.
    3. If `prompt_strategy`, prompt using `prompt_strategy`.
    4. Otherwise return None

    :param cli_value: The value supplied from the command line or `None`.
    :type cli_value: unicode or `None`
    :param config: Config dictionary
    :type config: dict
    :param key: Key to find the config value.
    :type key: unicode
    :prompt_strategy: Argumentless function to return fallback value.
    :type prompt_strategy: function
    :returns: The value for the username / password
    :rtype: unicode
    """
    if cli_value is not None:
        return cli_value
    else:
        if config.get(key) is not None:
            return config[key]
        if prompt_strategy:
            return prompt_strategy()
        return


get_cacert = functools.partial(get_userpass_value,
  key='ca_cert')
get_clientcert = functools.partial(get_userpass_value,
  key='client_cert')

class EnvironmentDefault(argparse.Action):
    __doc__ = 'Get values from environment variable.'

    def __init__(self, env, required=True, default=None, **kwargs):
        default = os.environ.get(env, default)
        self.env = env
        if default:
            required = False
        (super().__init__)(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


class EnvironmentFlag(argparse.Action):
    __doc__ = 'Set boolean flag from environment variable.'

    def __init__(self, env, **kwargs):
        default = self.bool_from_env(os.environ.get(env))
        self.env = env
        (super().__init__)(default=default, nargs=0, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, True)

    @staticmethod
    def bool_from_env(val):
        """
        Allow '0' and 'false' and 'no' to be False
        """
        falsey = {
         '0', 'false', 'no'}
        return val and val.lower() not in falsey