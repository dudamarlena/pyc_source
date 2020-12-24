# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/init/config.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 5960 bytes
import copy, logging, os, pkg_resources
from configobj import ConfigObj, flatten_errors
from validate import Validator
_log = logging.getLogger(__name__)
CONFIG_SPEC_PATH = pkg_resources.resource_filename('mediagoblin', 'config_spec.ini')

def _setup_defaults(config, config_path, extra_defaults=None):
    """
    Setup DEFAULTS in a config object from an (absolute) config_path.
    """
    extra_defaults = extra_defaults or {}
    config.setdefault('DEFAULT', {})
    config['DEFAULT']['here'] = os.path.dirname(config_path)
    config['DEFAULT']['__file__'] = config_path
    for key, value in extra_defaults.items():
        config['DEFAULT'].setdefault(key, value)


def read_mediagoblin_config(config_path, config_spec_path=CONFIG_SPEC_PATH):
    """
    Read a config object from config_path.

    Does automatic value transformation based on the config_spec.
    Also provides %(__file__)s and %(here)s values of this file and
    its directory respectively similar to paste deploy.

    Also reads for [plugins] section, appends all config_spec.ini
    files from said plugins into the general config_spec specification.

    This function doesn't itself raise any exceptions if validation
    fails, you'll have to do something

    Args:
     - config_path: path to the config file
     - config_spec_path: config file that provides defaults and value types
       for validation / conversion.  Defaults to mediagoblin/config_spec.ini

    Returns:
      A tuple like: (config, validation_result)
      ... where 'conf' is the parsed config object and 'validation_result'
      is the information from the validation process.
    """
    config_path = os.path.abspath(config_path)
    config = ConfigObj(config_path, interpolation='ConfigParser')
    _setup_defaults(config, config_path)
    config_spec = ConfigObj(config_spec_path, encoding='UTF8', list_values=False, _inspec=True)
    mainconfig_defaults = copy.copy(config_spec.get('DEFAULT', {}))
    mainconfig_defaults.update(config['DEFAULT'])
    plugins = config.get('plugins', {}).keys()
    plugin_configs = {}
    for plugin in plugins:
        try:
            plugin_config_spec_path = pkg_resources.resource_filename(plugin, 'config_spec.ini')
            if not os.path.exists(plugin_config_spec_path):
                continue
            plugin_config_spec = ConfigObj(plugin_config_spec_path, encoding='UTF8', list_values=False, _inspec=True)
            _setup_defaults(plugin_config_spec, config_path, mainconfig_defaults)
            if 'plugin_spec' not in plugin_config_spec:
                continue
            plugin_configs[plugin] = plugin_config_spec['plugin_spec']
        except ImportError:
            _log.warning("When setting up config section, could not import '%s'" % plugin)

    config_spec['plugins'] = plugin_configs
    _setup_defaults(config_spec, config_path, mainconfig_defaults)
    config = ConfigObj(config_path, configspec=config_spec, interpolation='ConfigParser')
    _setup_defaults(config, config_path, mainconfig_defaults)
    validator = Validator()
    validation_result = config.validate(validator, preserve_errors=True)
    return (
     config, validation_result)


REPORT_HEADER = 'There were validation problems loading this config file:\n--------------------------------------------------------\n'

def generate_validation_report(config, validation_result):
    """
    Generate a report if necessary of problems while validating.

    Returns:
      Either a string describing for a user the problems validating
      this config or None if there are no problems.
    """
    report = []
    for entry in flatten_errors(config, validation_result):
        section_list, key, error = entry
        if key is not None:
            section_list.append(key)
        else:
            section_list.append('[missing section]')
        section_string = ':'.join(section_list)
        if error == False:
            continue
        report.append('%s = %s' % (section_string, error))

    if report:
        return REPORT_HEADER + '\n'.join(report)
    else:
        return