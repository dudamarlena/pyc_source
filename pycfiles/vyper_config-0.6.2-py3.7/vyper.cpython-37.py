# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/vyper/vyper.py
# Compiled at: 2020-03-25 12:55:41
# Size of source mod 2**32: 24278 bytes
import argparse, logging, os, pprint
from . import constants, errors, remote, util, watch
log = logging.getLogger('vyper')

class Vyper(object):
    __doc__ = 'Vyper is a prioritized configuration registry. It maintains a set of\n    configuration sources, fetches values to populate those, and provides\n    them according to the source\'s priority.\n    The priority of the sources is the following:\n        1. overrides\n        2. args\n        3. env. variables\n        4. config file\n        5. key/value store\n        6. defaults\n\n    For example, if values from the following sources were loaded:\n\n    defaults: {\n        "secret": "",\n        "user": "default",\n        "endpoint": "https://localhost"\n        }\n\n    config: {\n        "user": "root"\n        "secret": "defaultsecret"\n        }\n\n    env: {\n        "secret": "somesecretkey"\n        }\n\n    The resulting config will have the following values:\n        {\n            "secret": "somesecretkey",\n            "user": "root",\n            "endpoint": "https://localhost"\n        }\n    '

    def __init__(self, config_name='config', key_delimiter='.'):
        self._key_delimiter = key_delimiter
        self._config_paths = []
        self._remote_providers = []
        self._config_name = config_name
        self._config_file = ''
        self._config_type = ''
        self._env_prefix = ''
        self._automatic_env_applied = False
        self._env_key_replacer = None
        self._aliases = {}
        self._override = {}
        self._args = {}
        self._env = {}
        self._config = {}
        self._kvstore = {}
        self._defaults = {}
        self._on_config_change = None
        self._on_remote_config_change = None
        self.parse_argv_disabled = False

    def on_config_change(self, func, *args, **kwargs):
        self._on_config_change = lambda : func(*args, **kwargs)

    def watch_config(self):
        config_file = self._get_config_file()
        watcher = watch.get_watcher(config_file, self)
        watcher.start()

    def set_config_file(self, file_):
        """Explicitly define the path, name and extension of the config file
        Vyper will use this and not check any of the config paths.
        """
        self._config_file = file_

    def set_env_prefix(self, prefix):
        """Define a prefix that ENVIRONMENT variables will use.
        e.g. if your prefix is "spf", the env registry will look
        for env. variables that start with "SPF_"
        """
        self._env_prefix = prefix

    def _merge_with_env_prefix(self, key):
        if self._env_prefix != '':
            return '{0}_{1}'.format(self._env_prefix, key).upper()
        return key.upper()

    def _get_env(self, key):
        """Wrapper around os.getenv() which replaces characters
        in the original key. This allows env vars which have different keys
        than the config object keys.
        """
        if self._env_key_replacer is not None:
            key = (key.replace)(*self._env_key_replacer)
        return os.getenv(key)

    def config_file_used(self):
        """Return the file used to populate the config registry."""
        return self._config_file

    def add_config_path(self, path):
        """Add a path for Vyper to search for the config file in.
        Can be called multiple times to define multiple search paths.
        """
        abspath = util.abs_pathify(path)
        if abspath not in self._config_paths:
            log.info('Adding {0} to paths to search'.format(abspath))
            self._config_paths.append(abspath)

    def add_remote_provider(self, provider, client, path):
        """Adds a remote configuration source.
        Remote Providers are searched in the order they are added.
        provider is a string value, "etcd", "consul" and "zookeeper" are
        currently supported.
        client is a client object
        path is the path in the k/v store to retrieve configuration
        To retrieve a config file called myapp.json from /configs/myapp.json
        you should set path to /configs and set config name (set_config_name)
        to "myapp"
        """
        if provider not in constants.SUPPORTED_REMOTE_PROVIDERS:
            raise errors.UnsupportedRemoteProviderError(provider)
        host = ''
        if provider == 'etcd':
            host = '{0}://{1}:{2}'.format(client.protocol, client.host, client.port)
        else:
            if provider == 'consul':
                host = '{0}://{1}:{2}'.format(client.http.scheme, client.http.host, client.http.port)
            else:
                if provider == 'zookeeper':
                    host = ','.join((str('{0}:{1}'.format(h[0], h[1])) for h in client.hosts))
                else:
                    log.info('Adding {0}:{1} to remote provider list'.format(provider, host))
                    rp = remote.RemoteProvider(provider, client, path, self)
                    self._provider_path_exists(rp) or self._remote_providers.append(rp)

    def _provider_path_exists(self, rp):
        for p in self._remote_providers:
            if p.path == rp.path:
                return True

        return False

    def _search_dict(self, d, keys):
        if not keys:
            return d
        for key in keys:
            if key in d:
                if not isinstance(d[key], dict):
                    return d[key]
            if key in d:
                return self._search_dict(d[key], keys[1:])
            return

    def get(self, key):
        """Vyper is essentially repository for configurations.
        `get` can retrieve any value given the key to use.
        `get` has the behavior of returning the value associated with the first
        place from where it is set. Viper will check in the following order:
        override, arg, env, config file, key/value store, default.
        """
        path = key.split(self._key_delimiter)
        lowercase_key = key.lower()
        val = self._find(lowercase_key)
        if val is None:
            source = self._find(path[0].lower())
            if source is not None:
                if isinstance(source, dict):
                    val = self._search_dict(source, path[1:])
        if val is None:
            return
        return val

    def get_string(self, key):
        val = self.get(key)
        if val is not None:
            return str(val)
        return ''

    def get_bool(self, key):
        val = self.get(key)
        if isinstance(val, str):
            if val.lower() == 'false':
                return False
        return bool(val)

    def get_int(self, key):
        val = self.get(key)
        if val is not None:
            return int(val)
        return 0

    def get_float(self, key):
        val = self.get(key)
        if val is not None:
            return float(val)
        return 0.0

    def get_bytes(self, key):
        return (b'{0}').format(self.get(key))

    def sub(self, key):
        """Returns new Vyper instance representing a sub tree of this instance.
        """
        subv = Vyper()
        data = self.get(key)
        if isinstance(data, dict):
            subv._config = data
            return subv
        return

    def unmarshall_key(self, key, cls):
        """Takes a single key and unmarshalls it into a class."""
        return setattr(cls, key, self.get(key))

    def unmarshall(self, cls):
        """Unmarshalls the config into a class. Make sure that the tags on
        the attributes of the class are properly set.
        """
        for k, v in self.all_settings().items():
            setattr(cls, k, v)

        return cls

    def bind_args(self, parser):
        if isinstance(parser, argparse.ArgumentParser):
            return self._bind_parser_values(parser)
        return self.bind_arg_values(parser)

    def bind_arg(self, key, arg):
        return self.bind_arg_value(key, arg)

    def _parse_args(self, parser, overrides=None):
        if overrides:
            return vars(parser.parse_args(overrides))
        else:
            return self.parse_argv_disabled or vars(parser.parse_args())
        return vars(parser.parse_args([]))

    def _bind_parser_values(self, parser, overrides=None):
        args = self._parse_args(parser, overrides)
        defaults = {k:parser.get_default(k) for k in args.keys()}
        for k, v in defaults.items():
            self.set_default(k, v)
            if args[k] != defaults[k]:
                self.bind_arg(k, args[k])

    def bind_arg_values(self, args):
        for k, v in args.items():
            try:
                self.bind_arg_value(k, v)
            except ValueError:
                pass

    def bind_arg_value(self, key, arg):
        if arg is None:
            raise ValueError('arg for {0} is None'.format(key))
        self._args[key.lower()] = arg

    def bind_env(self, *input_):
        """Binds a Vyper key to a ENV variable.
        ENV variables are case sensitive.
        If only a key is provided, it will use the env key matching the key,
        uppercased.
        `env_prefix` will be used when set when env name is not provided.
        """
        if len(input_) == 0:
            return 'bind_env missing key to bind to'
            key = input_[0].lower()
            if len(input_) == 1:
                env_key = self._merge_with_env_prefix(key)
            else:
                env_key = input_[1]
            self._env[key] = env_key
            if self._key_delimiter in key:
                parts = input_[0].split(self._key_delimiter)
                env_info = {'path':parts[1:-1],  'final_key':parts[-1],  'env_key':env_key}
                if self._env.get(parts[0]) is None:
                    self._env[parts[0]] = [
                     env_info]
        else:
            self._env[parts[0]].append(env_info)

    def _find_real_key(self, key, source):
        return next((real for real in source.keys() if real.lower() == key.lower()), None)

    def _find_insensitive(self, key, source):
        real_key = self._find_real_key(key, source)
        return source.get(real_key)

    def _set_insensitive(self, key, val, source):
        if source:
            real_key = self._find_real_key(key, source)
            if real_key is None:
                msg = 'No case insensitive variant of {0} found.'.format(key)
                raise KeyError(msg)
            source[real_key] = val
            return True

    def _find(self, key):
        """Given a key, find the value
        Vyper will check in the following order:
        override, arg, env, config file, key/value store, default
        Vyper will check to see if an alias exists first.
        """
        key = self._real_key(key)
        val = self._override.get(key)
        if val is not None:
            log.debug('{0} found in override: {1}'.format(key, val))
            return val
        val = self._args.get(key)
        if val is not None:
            log.debug('{0} found in args: {1}'.format(key, val))
            return val
        if self._automatic_env_applied:
            val = self._get_env(self._merge_with_env_prefix(key))
            if val is None:
                if '.' in key:
                    val = self._get_env(self._merge_with_env_prefix(key.replace('.', '_')))
        elif val is not None:
            log.debug('{0} found in environment: {1}'.format(key, val))
            return val
        else:
            env_key = self._find_insensitive(key, self._env)
            log.debug('Looking for {0} in env'.format(key))
            if isinstance(env_key, list):
                parent = self._find_insensitive(key, self._config)
                found_in_env = False
                log.debug('Found env key parent {0}: {1}'.format(key, parent))
                for item in env_key:
                    log.debug('{0} registered as env var parent {1}:'.format(key, item['env_key']))
                    val = self._get_env(item['env_key'])
                    if val is not None:
                        log.debug('{0} found in environment: {1}'.format(item['env_key'], val))
                        temp = parent
                        for path in item['path']:
                            real_key = self._find_real_key(path, temp)
                            temp = temp[real_key]

                        if self._set_insensitive(item['final_key'], val, temp):
                            found_in_env = True
                    else:
                        log.debug('{0} env value unset'.format(item['env_key']))

                if found_in_env:
                    return parent
            elif env_key is not None:
                log.debug('{0} registered as env var: {1}'.format(key, env_key))
                val = self._get_env(env_key)
                if val is not None:
                    log.debug('{0} found in environment: {1}'.format(env_key, val))
                    return val
                log.debug('{0} env value unset'.format(env_key))
        val = self._find_insensitive(key, self._config)
        if val is not None:
            log.debug('{0} found in config: {1}'.format(key, val))
            return val
        if self._key_delimiter in key:
            path = key.split(self._key_delimiter)
            source = self._find(path[0])
            if source is not None and isinstance(source, dict):
                val = self._search_dict(source, path[1:])
                if val is not None:
                    log.debug('{0} found in nested config: {1}'.format(key, val))
                    return val
        val = self._kvstore.get(key)
        if val is not None:
            log.debug('{0} found in key/value store: {1}'.format(key, val))
            return val
        val = self._defaults.get(key)
        if val is not None:
            log.debug('{0} found in defaults: {1}'.format(key, val))
            return val

    def is_set(self, key):
        """Check to see if the key has been set in any of the data locations.
        """
        path = key.split(self._key_delimiter)
        lower_case_key = key.lower()
        val = self._find(lower_case_key)
        if val is None:
            source = self._find(path[0].lower())
            if source is not None:
                if isinstance(source, dict):
                    val = self._search_dict(source, path[1:])
        return val is not None

    def automatic_env(self):
        """Have Vyper check ENV variables for all keys set in
        config, default & args.
        """
        self._automatic_env_applied = True

    def set_env_key_replacer(self, old, new):
        """Sets the strings.Replacer on the Vyper object.
        Useful for mapping an environment variable to a key that does
        not match it.
        """
        self._env_key_replacer = (
         old, new)

    def register_alias(self, alias, key):
        """Aliases provide another accessor for the same key.
        This enables one to change a name without breaking the application.
        """
        alias = alias.lower()
        key = key.lower()
        if alias != key and alias != self._real_key(key):
            exists = self._aliases.get(alias)
            if exists is None:
                val = self._config.get(alias)
                if val:
                    self._config.pop(alias)
                    self._config[key] = val
                val = self._kvstore.get(alias)
                if val:
                    self._kvstore.pop(alias)
                    self._kvstore[key] = val
                val = self._defaults.get(alias)
                if val:
                    self._defaults.pop(alias)
                    self._defaults[key] = val
                val = self._override.get(alias)
                if val:
                    self._override.pop(alias)
                    self._override[key] = val
                self._aliases[alias] = key
        else:
            log.warning('Creating circular reference alias {0} {1} {2}'.format(alias, key, self._real_key(key)))

    def _real_key(self, key):
        new_key = self._aliases.get(key)
        if new_key is not None:
            return self._real_key(new_key)
        return key

    def in_config(self, key):
        """Check to see if the given key (or an alias) is in the config file.
        """
        key = self._real_key(key)
        exists = self._config.get(key)
        return exists

    def set_default(self, key, value):
        """Set the default value for this key.
        Default only used when no value is provided by the user via
        arg, config or env.
        """
        k = self._real_key(key.lower())
        self._defaults[k] = value

    def set(self, key, value):
        """Sets the value for the key in the override register.
        Will be used instead of values obtained via
        args, config file, env, defaults or key/value store.
        """
        k = self._real_key(key.lower())
        self._override[k] = value

    def read_in_config(self):
        """Vyper will discover and load the configuration file from disk
        and key/value stores, searching in one of the defined paths.
        """
        log.info('Attempting to read in config file')
        if self._get_config_type() not in constants.SUPPORTED_EXTENSIONS:
            raise errors.UnsupportedConfigError(self._get_config_type())
        with open(self._get_config_file()) as (fp):
            f = fp.read()
        self._config = {}
        return self._unmarshall_reader(f, self._config)

    def merge_in_config(self):
        log.info('Attempting to merge in config file')
        if self._get_config_type() not in constants.SUPPORTED_EXTENSIONS:
            raise errors.UnsupportedConfigError(self._get_config_type())
        with open(self._get_config_file()) as (fp):
            f = fp.read()
        return self.merge_config(f)

    def read_config(self, f):
        """Vyper will read a configuration file, setting existing keys to
        `None` if the key does not exist in the file.
        """
        self._unmarshall_reader(f, self._config)

    def merge_config(self, f):
        if self._config is None:
            self._config = {}
        cfg = {}
        cfg = self._unmarshall_reader(f, cfg)
        self._merge_dicts(cfg, self._config)

    def _merge_dicts(self, src, target):
        for k, v in src.items():
            if isinstance(v, dict) and k in target:
                self._merge_dicts(v, target[k])
            else:
                target[k] = v

    def read_remote_config(self):
        """Attempts to get configuration from a remote source
        and read it in the remote configuration registry.
        """
        return self._get_key_value_config()

    def _unmarshall_reader(self, f, d):
        """Unmarshall a file into a `dict`."""
        return util.unmarshall_config_reader(f, d, self._get_config_type())

    def _get_key_value_config(self):
        """Retrieves the first found remote configuration."""
        for rp in self._remote_providers:
            val = self._get_remote_config(rp)
            self._kvstore = val
            return

        raise errors.RemoteConfigError('No Files Found')

    def _get_remote_config(self, provider):
        reader = provider.get()
        self._unmarshall_reader(reader, self._kvstore)
        return self._kvstore

    def on_remote_config_change(self, func, *args, **kwargs):
        self._on_remote_config_change = lambda x: func(*args, **kwargs)
        for rp in self._remote_providers:
            rp.add_listener(self._on_remote_config_change)
            return

    def watch_remote_config(self):
        for rp in self._remote_providers:
            rp.add_listener()
            return

        raise errors.RemoteConfigError('No Files Found')

    def all_keys(self, uppercase_keys=False):
        """Return all keys regardless where they are set."""
        d = {}
        for k in self._override.keys():
            d[k.upper() if uppercase_keys else k.lower()] = {}

        for k in self._args.keys():
            d[k.upper() if uppercase_keys else k.lower()] = {}

        for k in self._env.keys():
            d[k.upper() if uppercase_keys else k.lower()] = {}

        for k in self._config.keys():
            d[k.upper() if uppercase_keys else k.lower()] = {}

        for k in self._kvstore.keys():
            d[k.upper() if uppercase_keys else k.lower()] = {}

        for k in self._defaults.keys():
            d[k.upper() if uppercase_keys else k.lower()] = {}

        for k in self._aliases.keys():
            d[k.upper() if uppercase_keys else k.lower()] = {}

        return d.keys()

    def all_settings(self, uppercase_keys=False):
        """Return all settings as a `dict`."""
        d = {}
        for k in self.all_keys(uppercase_keys):
            d[k] = self.get(k)

        return d

    def set_config_name(self, name):
        """Name for the config file. Does not include extension."""
        self._config_name = name
        self._config_file = ''

    def set_config_type(self, type_):
        """Sets the type of the configuration returned by the
        remote source, e.g. "json".
        """
        self._config_type = type_

    def _get_config_type(self):
        if self._config_type != '':
            return self._config_type
        cf = self._get_config_file()
        ext = os.path.splitext(cf)
        if len(ext) > 1:
            return ext[1][1:]
        return ''

    def _get_config_file(self):
        if self._config_file == '':
            try:
                cf = self._find_config_file()
                self._config_file = cf
            except errors.ConfigFileNotFoundError:
                return ''

        return self._config_file

    def _search_in_path(self, path):
        log.debug('Searching for config in: {0}'.format(path))
        for ext in constants.SUPPORTED_EXTENSIONS:
            full_path = '{0}/{1}.{2}'.format(path, self._config_name, ext)
            log.debug('Checking for {0}'.format(full_path))
            if util.exists(full_path):
                log.debug('Found: {0}'.format(full_path))
                return full_path

        return ''

    def _find_config_file(self):
        """Search all `config_paths` for any config file.
        Returns the first path that exists (and is a config file).
        """
        log.info('Searching for config in: {0}'.format(', '.join((str(p) for p in self._config_paths))))
        for cp in self._config_paths:
            f = self._search_in_path(cp)
            if f != '':
                return f

        raise errors.ConfigFileNotFoundError(self._config_name, self._config_paths)

    def debug(self):
        """Prints all configuration registries for debugging purposes."""
        print('Aliases:')
        pprint.pprint(self._aliases)
        print('Override:')
        pprint.pprint(self._override)
        print('Args:')
        pprint.pprint(self._args)
        print('Env:')
        pprint.pprint(self._env)
        print('Config:')
        pprint.pprint(self._config)
        print('Key/Value Store:')
        pprint.pprint(self._kvstore)
        print('Defaults:')
        pprint.pprint(self._defaults)