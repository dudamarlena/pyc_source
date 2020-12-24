# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/twine/twine/utils.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 10629 bytes
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import os, os.path, functools, getpass, sys, argparse, warnings, collections
from requests.exceptions import HTTPError
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

try:
    from urlparse import urlparse, urlunparse
except ImportError:
    from urllib.parse import urlparse, urlunparse

try:
    import keyring
except ImportError:
    pass

from twine import exceptions
if sys.version_info > (3, ):
    input_func = input
else:
    input_func = raw_input
DEFAULT_REPOSITORY = 'https://upload.pypi.org/legacy/'
TEST_REPOSITORY = 'https://test.pypi.org/legacy/'

def get_config(path='~/.pypirc'):
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


def get_repository_from_config(config_file, repository, repository_url=None):
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

def normalize_repository_url(url):
    parsed = urlparse(url)
    if parsed.netloc in _HOSTNAMES:
        return urlunparse(('https', ) + parsed[1:])
    else:
        return urlunparse(parsed)


def check_status_code(response, verbose):
    """
    Shouldn't happen, thanks to the UploadToDeprecatedPyPIDetected
    exception, but this is in case that breaks and it does.
    """
    if response.status_code == 410:
        if response.url.startswith(('https://pypi.python.org', 'https://testpypi.python.org')):
            print("It appears you're uploading to pypi.python.org (or testpypi.python.org). You've received a 410 error response. Uploading to those sites is deprecated. The new sites are pypi.org and test.pypi.org. Try using https://upload.pypi.org/legacy/ (or https://test.pypi.org/legacy/) to upload your packages instead. These are the default URLs for Twine now. More at https://packaging.python.org/guides/migrating-to-pypi-org/ ")
    try:
        response.raise_for_status()
    except HTTPError as err:
        if response.text:
            if verbose:
                print('Content received from server:\n{}'.format(response.text))
            else:
                print('NOTE: Try --verbose to see response content.')
        raise err


def get_userpass_value(cli_value, config, key, prompt_strategy=None):
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


def get_username_from_keyring(system):
    if 'keyring' not in sys.modules:
        return
    try:
        getter = sys.modules['keyring'].get_credential
    except AttributeError:
        return
    else:
        try:
            creds = getter(system, None)
            if creds:
                return creds.username
        except Exception as exc:
            warnings.warn(str(exc))


def password_prompt(prompt_text):
    prompt = prompt_text
    if os.name == 'nt':
        if sys.version_info < (3, 0):
            prompt = prompt_text.encode('utf8')
    return getpass.getpass(prompt)


def get_password_from_keyring(system, username):
    if 'keyring' not in sys.modules:
        return
    try:
        return sys.modules['keyring'].get_password(system, username)
    except Exception as exc:
        warnings.warn(str(exc))


def username_from_keyring_or_prompt(system):
    return get_username_from_keyring(system) or input_func('Enter your username: ')


def password_from_keyring_or_prompt(system, username):
    return get_password_from_keyring(system, username) or password_prompt('Enter your password: ')


def get_username(system, cli_value, config):
    return get_userpass_value(cli_value,
      config,
      key='username',
      prompt_strategy=(functools.partial(username_from_keyring_or_prompt, system)))


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
        (super(EnvironmentDefault, self).__init__)(default=default, 
         required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def get_password(system, username, cli_value, config):
    return get_userpass_value(cli_value,
      config,
      key='password',
      prompt_strategy=(functools.partial(password_from_keyring_or_prompt, system, username)))


def no_positional(allow_self=False):
    """A decorator that doesn't allow for positional arguments.

    :param bool allow_self:
        Whether to allow ``self`` as a positional argument.
    """

    def reject_positional_args(function):

        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            allowed_positional_args = 0
            if allow_self:
                allowed_positional_args = 1
            received_positional_args = len(args)
            if received_positional_args > allowed_positional_args:
                function_name = function.__name__
                verb = 'were' if received_positional_args > 1 else 'was'
                raise TypeError('{}() takes {} positional arguments but {} {} given'.format(function_name, allowed_positional_args, received_positional_args, verb))
            return function(*args, **kwargs)

        return wrapper

    return reject_positional_args