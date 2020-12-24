# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/moul/Git/moul/advanced-ssh-config/venv2.6/lib/python2.6/site-packages/advanced_ssh_config/config.py
# Compiled at: 2015-07-22 05:13:14
from collections import OrderedDict
import ConfigParser, glob, logging, os, re
from .exceptions import ConfigError

class ConfigHost(object):
    special_keys = ('hostname', 'gateways', 'reallocalcommand', 'remotecommand', 'includes',
                    'inherits', 'comment', 'password')
    key_translation = {'alias': 'hostname'}

    def __init__(self, c, host, config=None, extra=None, inherited_config=None, inherited_extra=None):
        self.c = c
        self.host = host
        self.config = config or {}
        self.extra = extra or {}
        self.inherited = None
        self.resolved = False
        return

    @classmethod
    def prepare_hostname(cls, host):
        host = re.sub('\\.\\*', '*', host)
        host = re.sub('\\\\\\.', '.', host)
        return host

    @classmethod
    def from_config_file(cls, c, host, entry):
        config = []
        extra_config = []
        for (key, value) in entry:
            if key in ConfigHost.key_translation:
                key = ConfigHost.key_translation.get(key)
            values = value.split('\n')
            values = map(str.strip, values)
            for line in values:
                if line.lstrip().find('$(') == 0 and line.rstrip()[(-1)] == ')':
                    extra_config.append((key, line))
                elif key in ConfigHost.special_keys:
                    extra_config.append((key, line))
                else:
                    config.append((key, line))

        return cls(c, host, config=config, extra=extra_config)

    def config_keys(self):
        return [ entry[0] for entry in self.config ]

    @property
    def config_dict(self):
        if not self.resolved:
            self.resolve()
        config = {}
        for entry in self.config:
            if entry[0] in config:
                config[entry[0]].append(entry[1])
            else:
                config[entry[0]] = [
                 entry[1]]

        return config

    @property
    def extra_dict(self, sort=True):
        extra = {}
        for entry in self.extra:
            if entry[0] in extra:
                extra[entry[0]].append(entry[1])
            else:
                extra[entry[0]] = [
                 entry[1]]

        if sort:
            return OrderedDict(sorted(extra.items()))
        return extra

    @property
    def clean_config(self, sort=True):
        config = self.config_dict
        if self.inherited:
            config = dict(self.inherited.items() + config.items())
        if self.host == 'default' and 'proxycommand' not in config:
            config['proxycommand'] = [
             'assh connect %h --port=%p']
        if sort:
            return OrderedDict(sorted(config.items()))
        return config

    def resolve(self, rec=10):
        if not rec:
            raise ConfigError('Maximum recursion deptch exceeded')
        if self.resolved:
            return
        for (key, value) in self.extra:
            if key == 'inherits':
                if value in self.c.full:
                    parent = self.c.full[value]
                    parent.resolve(rec - 1)
                    self.inherited = parent.clean_config
                else:
                    raise ConfigError(('Inheriting an unkonwn host: `{}`').format(value))

        self.resolved = True

    def get_prep_value(self):
        return {'config': self.config, 
           'extra': self.extra, 
           'inherited': self.inherited}

    def __repr__(self):
        max_len = 50
        dict_string = (', ').join([ '%s=%s' % (key, str(val)[:max_len - 2] + '..' if len(str(val)) > max_len else str(val)) for (key, val) in self.get_prep_value().items()
                                  ])
        return ('<{}.{} at {} - {}>').format(self.__class__.__module__, self.__class__.__name__, hex(id(self)), dict_string)

    def build_sshconfig(self):
        sub_config = []
        if self.host == 'default':
            host = '*'
        else:
            host = self.host
        sub_config.append(('Host {}').format(host))
        attrs = OrderedDict(sorted(self.clean_config.items()))
        for (key, values) in attrs.iteritems():
            for value in values:
                sub_config.append(('  {} {}').format(key, value))

        for (key, values) in self.extra_dict.iteritems():
            for value in values:
                sub_config.append(('  # {} {}').format(key, value))

        sub_config.append('')
        return sub_config


class Config(object):

    def __init__(self, configfiles):
        self.full_cache = None
        self.configfiles = map(os.path.expanduser, configfiles)
        self.loaded_files = []
        self.logger = logging.getLogger('assh.Config')
        self.parser = ConfigParser.ConfigParser()
        self.parser.SECTCRE = re.compile('\\[(?P<header>.+)\\]')
        self._read()
        for section in self.sections:
            if re.sub('[^a-zA-Z0-9\\\\\\.\\*_-]', '', section) != section:
                raise ConfigError(('Invalid characters used in section {}').format(section))

        return

    def debug(self, string=None):
        self.logger.debug(string and string or '')

    def _load_file(self, filename):
        if filename in self.loaded_files:
            return
        self.parser.read(filename)
        self.loaded_files.append(filename)

    def _read(self):
        for configfile in self.configfiles:
            self._load_file(configfile)

        includes = str(self.get('includes', 'default', '')).strip()
        for include in includes.split():
            for incpath in glob.glob(os.path.expanduser(include)):
                if os.path.exists(incpath):
                    self._load_file(incpath)
                else:
                    raise ConfigError(("'{}' include not found").format(incpath))

    @property
    def sections(self):
        return sorted(list(set(self.parser.sections() + ['default'])))

    def get_in_section(self, section, key, raw=False, vardct=None):
        if not self.parser.has_option(section, key):
            return False
        var = self.parser.get(section, key, raw, vardct)
        if key in ('identityfile', 'localforward', 'remoteforward', 'comment'):
            var = var.split('\n')
            var = map(str.strip, var)
        return var

    def get(self, key, host, default=None, vardct=None):
        for section in self.sections:
            if re.match(section, host):
                val = self.get_in_section(section, key, vardct=vardct)
                if val:
                    return val

        val = self.get_in_section('default', key)
        return val or default

    @property
    def full(self):
        if not self.full_cache:
            self.full_cache = {}
            for section in self.parser.sections():
                host = ConfigHost.prepare_hostname(section)
                config_file_entry = self.parser.items(section, False, {})
                conf = ConfigHost.from_config_file(self, host, config_file_entry)
                self.full_cache[host] = conf

            if 'default' not in self.full_cache:
                self.full_cache['default'] = ConfigHost(self, 'default')
        return self.full_cache