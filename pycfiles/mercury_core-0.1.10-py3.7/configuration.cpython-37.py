# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/common/configuration.py
# Compiled at: 2019-02-07 12:47:28
# Size of source mod 2**32: 18314 bytes
import argparse, ast, logging, os, shlex, yaml
from box import Box
from mercury.common.exceptions import MercuryConfigurationError
from mercury.common.log import log_format
LOG = logging.getLogger(__name__)
DEFAULT_SEARCH_DIRS = [
 '.', '~/.mercury', '/etc/mercury']

def find_config(filename, dirs=None):
    """Searches for configuration files. Setting the environment variable:
        ```
            MERCURY_SEARCH_DIRS
        ```
        can be used to extend the search paths as well

    :param filename: The configuration file path or a filename to search for
    :param dirs: A list of filesystem directories to search for the
        configuration file. Parameter defaults to None, which means a set
        of default locations will be searched.
    :returns: string or None -- The full path of the configuration file if
        found.  None otherwise.
    """
    if os.path.isfile(filename):
        return filename
    dirs = dirs or list() + DEFAULT_SEARCH_DIRS
    if 'MERCURY_SEARCH_DIRS' in os.environ:
        dirs = dirs + os.environ.get('MERCURY_SEARCH_DIRS')
    for directory in dirs:
        full_path = os.path.join(os.path.expanduser(directory), filename)
        if os.path.isfile(full_path):
            return full_path


def configuration_from_yaml(filename):
    """Loads a YAML configuration file.

    :param filename: The filename of the file to load.
    :returns: dict -- A dictionary representing the YAML configuration file
        loaded. If the file can't be loaded, then the empty dict is returned.
    """
    try:
        with open(filename) as (infile):
            return yaml.load(infile.read())
    except IOError:
        return {}


def get_configuration(filename):
    """Gets and returns the contents of the configuration file as a dict.

    :param filename: The filename of the configuration file to load.
    :returns: dict -- A dictionary representing the YAML configuration file
        loaded. If the file was not found or loaded, then returns an empty
        dict.
    """
    config_file = find_config(filename)
    if not config_file:
        LOG.warning('%s not found' % filename)
        return {}
    return configuration_from_yaml(config_file)


class MercuryConfiguration(object):

    def __init__(self, program_name, configuration_file, description=None, config_search_dirs=None):
        """Mercury Configuration helper which simplifies cli arguments,
        environment variables, and configuration file merging

        :param program_name:
        :param configuration_file: The name of the configuration file
        :param description:
        """
        self.program_name = program_name
        self.argument_parser = argparse.ArgumentParser(prog=(self.program_name),
          description=description,
          formatter_class=(argparse.ArgumentDefaultsHelpFormatter))
        self.config_search_dirs = config_search_dirs or []
        self.master_configuration = Box()
        self.argparse_namespace = None
        self.options = []
        self.configuration_file = configuration_file
        self.configuration = {}
        self.argument_parser.add_argument('-c', '--configuration',
          default=(self.configuration_file),
          help='Path to the configuration file')
        self.add_option('logging.level', '--log-level',
          'MERCURY_LOG_LEVEL',
          'logging.level',
          default='INFO',
          help_string='Log level, INFO | DEBUG | ERROR | WARNING')
        self.add_option('logging.format', '--log-format',
          'MERCURY_LOG_FORMAT',
          'logging.format',
          default=log_format,
          help_string='Desired logging format')

    def set_configuration(self):
        """ Parse the configuration """
        if self.argparse_namespace.configuration != self.configuration_file:
            self.configuration = configuration_from_yaml(self.argparse_namespace.configuration)
        else:
            config_file = find_config(self.configuration_file, self.config_search_dirs)
            if config_file:
                self.configuration = configuration_from_yaml(config_file)
        self.master_configuration.update(self.configuration)

    @staticmethod
    def get_by_namespace(dictionary, namespace):
        """
        Used to access a dictionary values using dot notation

        For instance:

        .. code-block::

            {'one': {'two': 'three'}}

            >> d['one']['two']
            'three'
            >> get_by_namespace('one.two')
            'three'
        :param dictionary: The dictionary we are searching
        :param namespace: Dot notated namespace specifier
        :type namespace: str
        :return: The value the namespace resolves to or None
        """
        value = dictionary
        for k in namespace.split('.'):
            try:
                value = value[k]
            except KeyError:
                return

        return value

    @staticmethod
    def set_by_namespace(dictionary, namespace, value):
        """
        Like get_by_namespace, but set a value rather than returning it
        :param dictionary: The dictionary we are modifying
        :param namespace:
        :param value:
        :return:
        """
        expanded = namespace.split('.')
        for k in expanded[:-1]:
            dictionary = dictionary[k]

        dictionary[expanded[(-1)]] = value

    @staticmethod
    def convert_argparse_destination(argument_name):
        """ Converts underscores to dashes, for a deterministic mechanism
         to name (and recall) argparse destinations"""
        return argument_name.lstrip('-').replace('-', '_')

    def parse_args(self):
        """ Add option arguments and parse_args """
        for opt in self.options:
            if not opt['added_to_parser']:
                (self.argument_parser.add_argument)(opt['cli_argument']), *(opt['args'], dest=self.convert_argparse_destination(opt['cli_argument']), help=opt['help'], **opt['kwargs'])
                opt['added_to_parser'] = True

        self.argparse_namespace = self.argument_parser.parse_args()

    @staticmethod
    def format_type(value, special_type):
        """
        Since argparse (by default) and os.environ can only be strings, we allow
        options to specify a type
        :param value: The value we are transforming
        :param special_type: The 'type' we are transforming to
        :type special_type: list, int, float, bool
        :return: None
        """
        if type(special_type) is not type:
            raise MercuryConfigurationError(f"{special_type} must be a type, not an object")
        else:
            if special_type not in [list, int, float, bool]:
                raise MercuryConfigurationError(f"{special_type} is not support for conversion")
            else:
                if isinstance(value, special_type):
                    return value
                assert isinstance(value, str), 'Only string types are converted'
            if special_type is list:
                return value.split(',')
            if special_type is bool:
                return value.lower() not in ('0', 'false')
            try:
                return special_type(value)
            except ValueError:
                raise MercuryConfigurationError(f"{value} cannot be converted to {special_type}")

    @staticmethod
    def expand_option(namespace, option):
        """ Expand an option, usually expressed in dotted notation, to a
        namespace path. All but the last element, the value element, are
        considered containers. For the option: nest1.nest2.nest3, nest1 and
        nest2 would be initialized as new boxes, if they did not exist already.
        nest3 would be initialized with the default value of the option
        :param namespace: self.namespace reference
        :param option: The option we are expanding
        """
        expanded_name = option['name'].split('.')
        for container in expanded_name[:-1]:
            if container not in namespace:
                namespace[container] = Box()
            else:
                if not isinstance(namespace[container], dict):
                    raise MercuryConfigurationError(f"{container} exists and is not a container, {option['name']} is invalid")
            namespace = namespace[container]

        namespace[expanded_name[(-1)]] = option['default']

    def override_value(self, name, value, special_type):
        """
        DRY override method replacing a value from a given source
        :param name: The name of the value
        :param value: The value
        :param special_type: type to convert the value to
        """
        if value:
            if special_type:
                value = self.format_type(value, special_type)
            self.set_by_namespace(self.master_configuration, name, value)

    def override_with_configuration(self, option):
        """
        Overrides option with a value in the configuration file
        :param option: an option from self.options
        """
        self.override_value(option['name'], self.get_by_namespace(self.configuration, option['config_address']), option['special_type'])

    def override_with_environment(self, option):
        """
        Overrides option with the value found in an environment variable
        :param option: an option from self.options
        :return:
        """
        self.override_value(option['name'], os.environ.get(option['env_variable']), option['special_type'])

    def override_with_cli_options(self, option):
        """
        Override option with a value passed in as a command line argument
        :param option: an option from self.options
        """
        self.override_value(option['name'], vars(self.argparse_namespace).get(self.convert_argparse_destination(option['cli_argument'])), option['special_type'])

    def override_with_proc_cmdline(self, option):
        """
        Attempt to read option from /proc/cmdline
        """
        try:
            with open('/proc/cmdline') as (fp):
                cmdline_options = shlex.split(fp.read())
        except OSError:
            LOG.info('/proc/cmdline is not available for parsing')
            return
        else:
            for cmdline_option in cmdline_options:
                item = cmdline_option.split('=', 1)
                if len(item) > 1:
                    k, v = item
                    if k == option['proc_cmdline_argument']:
                        self.override_value(k, v, option['special_type'])
                        break

    def scan_options(self):
        """
        :return: The master configuration
        """
        self.parse_args()
        self.set_configuration()
        for option in self.options:
            self.expand_option(self.master_configuration, option)
            self.override_with_configuration(option)
            self.override_with_environment(option)
            if option['proc_cmdline_argument']:
                self.override_with_proc_cmdline(option)
            self.override_with_cli_options(option)
            value = self.get_by_namespace(self.master_configuration, option['name'])
            if option['required']:
                if not value:
                    raise MercuryConfigurationError(f"Option {option['name']} has not been provided")
            if option['one_of'] and value in 'one_of':
                raise MercuryConfigurationError(f"Option {option['name']} is {value} but must be one of {','.join(str(option['one_of']))}")

        return self.master_configuration

    @staticmethod
    def check_name(name):
        """
        Validator of the argument name, enforces python namespace rules

        :param name: The option name
        :return: None
        :raises: MercuryConfigurationError
        """
        try:
            ast.parse(name)
        except SyntaxError:
            raise MercuryConfigurationError(f"{name} is not a valid name")

    @staticmethod
    def auto_format_cli_argument(name):
        """ It is a popular convention for arguments to have dashes rather than
        underscores, they should also be prepended with dashes

        .. note::

            Switches (-s) are not supported

        :param name: The option name
        :return: The formatted name
        """
        return '--' + name.replace('.', '-').replace('_', '-')

    @staticmethod
    def auto_format_env_variable(name):
        """ It is convention that environment variable use underscores and be
        upper case

        :param name: The option name.
        :return: The formatted name
        """
        return name.replace('.', '_').upper()

    def add_option(self, name, cli_argument=None, env_variable=None, config_address=None, proc_cmdline_argument=None, default=None, help_string=None, special_type=None, required=False, one_of=None, *args, **kwargs):
        """
        Allows us to define options which can be defined on the command line,
        from an environment variable, or from the configuration file.

        :param name: The option namespace
        :param cli_argument: The name argument name
        :param env_variable: The environment variable
        :param config_address: The 'address' of the option's configuration key.
         Configuration files are yaml. For the configuration:

        .. code-block: yaml

            nest1:
              nest2:
                nest3: My Value

        nest1.nest2.nest3 == 'My Value'

        :param proc_cmdline_argument: If available (linux) search /proc/cmdline for the
            specified argument.
        :param default: The default value of the option
        :param help_string: Description of what the option does and how to use
            it
        :param special_type: Allows us to specify a type conversion for the
            value. Supported type conversions are int, float, and list
        :param required: An exception will be raised if the namespace is not
        populated by some source
        :param one_of:
        :param args: Additional args to pass to argparse
        :param kwargs: Additional kwargs to pass to argparse
        :return: None
        """
        self.check_name(name)
        self.options.append(dict(name=name,
          cli_argument=(cli_argument or self.auto_format_cli_argument(name)),
          env_variable=(env_variable or self.auto_format_env_variable(name)),
          config_address=(config_address or name),
          proc_cmdline_argument=proc_cmdline_argument,
          default=default,
          help=help_string,
          special_type=special_type,
          required=required,
          one_of=(one_of or []),
          args=args,
          kwargs=kwargs,
          added_to_parser=False))