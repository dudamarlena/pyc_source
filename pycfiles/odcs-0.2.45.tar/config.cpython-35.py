# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/config.py
# Compiled at: 2017-09-21 02:38:08
# Size of source mod 2**32: 11324 bytes
import imp, os, sys
from odcs.server import logger

def init_config(app):
    """
    Configure ODCS
    """
    config_module = None
    config_file = '/etc/odcs/config.py'
    config_section = 'DevConfiguration'
    try:
        with open(config_file):
            config_section = 'ProdConfiguration'
    except (OSError, IOError) as e:
        sys.stderr.write('WARN: Cannot open %s: %s\n' % (
         config_file, e.strerror))
        sys.stderr.write('WARN: DevConfiguration will be used.\n')

    if 'ODCS_CONFIG_FILE' in os.environ:
        config_file = os.environ['ODCS_CONFIG_FILE']
    if 'ODCS_CONFIG_SECTION' in os.environ:
        config_section = os.environ['ODCS_CONFIG_SECTION']
    if any(['nosetests' in arg or 'noserunner.py' in arg or 'py.test' in arg or 'pytest.py' in arg for arg in sys.argv]):
        config_section = 'TestConfiguration'
        from conf import config
        config_module = config
    elif 'ODCS_DEVELOPER_ENV' in os.environ and os.environ['ODCS_DEVELOPER_ENV'].lower() in ('1',
                                                                                             'on',
                                                                                             'true',
                                                                                             'y',
                                                                                             'yes'):
        config_section = 'DevConfiguration'
        from conf import config
        config_module = config
    if not config_module:
        try:
            config_module = imp.load_source('odcs_runtime_config', config_file)
        except:
            raise SystemError('Configuration file {} was not found.'.format(config_file))

    config_section_obj = getattr(config_module, config_section)
    conf = Config(config_section_obj)
    app.config.from_object(config_section_obj)
    return conf


class Config(object):
    __doc__ = 'Class representing the odcs configuration.'
    _defaults = {'debug': {'type': bool, 
               'default': False, 
               'desc': 'Debug mode'}, 
     
     'log_backend': {'type': str, 
                     'default': None, 
                     'desc': 'Log backend'}, 
     
     'log_file': {'type': str, 
                  'default': '', 
                  'desc': 'Path to log file'}, 
     
     'log_level': {'type': str, 
                   'default': 0, 
                   'desc': 'Log level'}, 
     
     'net_timeout': {'type': int, 
                     'default': 120, 
                     'desc': 'Global network timeout for read/write operations, in seconds.'}, 
     
     'net_retry_interval': {'type': int, 
                            'default': 30, 
                            'desc': 'Global network retry interval for read/write operations, in seconds.'}, 
     
     'pdc_url': {'type': str, 
                 'default': '', 
                 'desc': 'PDC URL.'}, 
     
     'pdc_insecure': {'type': bool, 
                      'default': False, 
                      'desc': 'Allow insecure connection to PDC.'}, 
     
     'pdc_develop': {'type': bool, 
                     'default': False, 
                     'desc': 'PDC Development mode, basically noauth.'}, 
     
     'koji_profile': {'type': str, 
                      'default': None, 
                      'desc': 'Koji config profile.'}, 
     
     'arches': {'type': list, 
                'default': ['x86_64'], 
                'desc': 'Compose architectures.'}, 
     
     'pungi_koji': {'type': str, 
                    'default': 'pungi-koji', 
                    'desc': 'Name or full-path to pungi-koji binary.'}, 
     
     'target_dir': {'type': str, 
                    'default': './', 
                    'desc': 'Path to target dir to which store composes'}, 
     
     'target_dir_url': {'type': str, 
                        'default': 'http://localhost/odcs', 
                        'desc': 'Public facing URL to target_dir.'}, 
     
     'seconds_to_live': {'type': int, 
                         'default': 86400, 
                         'desc': 'Default number of seconds for which the compose is available.'}, 
     
     'max_seconds_to_live': {'type': int, 
                             'default': 259200, 
                             'desc': 'Max number of seconds for which the compose is available.'}, 
     
     'num_concurrent_pungi': {'type': int, 
                              'default': 2, 
                              'desc': 'Number of concurrent Pungi processes.'}, 
     
     'allowed_source_types': {'type': list, 
                              'default': ['tag', 'module'], 
                              'desc': 'Allowed source types.'}, 
     
     'auth_ldap_server': {'type': str, 
                          'default': '', 
                          'desc': "Server URL to query user's groups."}, 
     
     'auth_ldap_group_base': {'type': str, 
                              'default': '', 
                              'desc': "Group base to query user's groups from LDAP server."}, 
     
     'allowed_clients': {'type': dict, 
                         'default': {'groups': [], 'users': []}, 
                         'desc': 'Groups and users that are allowed to generate composes.'}, 
     
     'admins': {'type': dict, 
                'default': {'groups': [], 'users': []}, 
                'desc': 'Admin groups and users.'}, 
     
     'auth_backend': {'type': str, 
                      'default': '', 
                      'desc': 'Select which authentication backend is enabled and work with frond-end authentication together.'}, 
     
     'auth_openidc_userinfo_uri': {'type': str, 
                                   'default': '', 
                                   'desc': 'UserInfo endpoint to get user information from FAS.'}, 
     
     'auth_openidc_required_scopes': {'type': list, 
                                      'default': [], 
                                      'desc': 'Required scopes for submitting request to run new compose.'}, 
     
     'messaging_backend': {'type': str, 
                           'default': '', 
                           'desc': 'Messaging backend, fedmsg or umb.'}, 
     
     'messaging_broker_urls': {'type': list, 
                               'default': [], 
                               'desc': 'List of messaging broker URLs.'}, 
     
     'messaging_cert_file': {'type': str, 
                             'default': '', 
                             'desc': 'Path to certificate file used to authenticate ODCS by broker.'}, 
     
     'messaging_key_file': {'type': str, 
                            'default': '', 
                            'desc': 'Path to private key file used to authenticate ODCS by broker.'}, 
     
     'messaging_ca_cert': {'type': str, 
                           'default': '', 
                           'desc': 'Path to trusted CA certificate bundle.'}, 
     
     'messaging_topic': {'type': str, 
                         'default': '', 
                         'desc': 'Messaging topic to which messages are sent.'}}

    def __init__(self, conf_section_obj):
        """
        Initialize the Config object with defaults and then override them
        with runtime values.
        """
        for name, values in self._defaults.items():
            self.set_item(name, values['default'])

        for key in dir(conf_section_obj):
            if key.startswith('_'):
                pass
            else:
                self.set_item(key.lower(), getattr(conf_section_obj, key))

        self.login_disabled = self.auth_backend == 'noauth'

    def set_item(self, key, value):
        """
        Set value for configuration item. Creates the self._key = value
        attribute and self.key property to set/get/del the attribute.
        """
        if key == 'set_item' or key.startswith('_'):
            raise Exception("Configuration item's name is not allowed: %s" % key)
        setattr(self, '_' + key, None)
        setifok_func = '_setifok_{}'.format(key)
        if hasattr(self, setifok_func):
            setx = lambda self, val: getattr(self, setifok_func)(val)
        else:
            setx = lambda self, val: setattr(self, '_' + key, val)
        getx = lambda self: getattr(self, '_' + key)
        delx = lambda self: delattr(self, '_' + key)
        setattr(Config, key, property(getx, setx, delx))
        if key in self._defaults:
            convert = self._defaults[key]['type']
            if convert in [bool, int, list, str, set, dict]:
                try:
                    if value is not None:
                        value = convert(value)
                except:
                    raise TypeError('Configuration value conversion failed for name: %s' % key)

        else:
            if convert is not None:
                raise TypeError('Unsupported type %s for configuration item name: %s' % (convert, key))
            setattr(self, key, value)

    def _setifok_log_backend(self, s):
        if s is None:
            self._log_backend = 'console'
        elif s not in logger.supported_log_backends():
            raise ValueError('Unsupported log backend')
        self._log_backend = str(s)

    def _setifok_log_file(self, s):
        if s is None:
            self._log_file = ''
        else:
            self._log_file = str(s)

    def _setifok_log_level(self, s):
        level = str(s).lower()
        self._log_level = logger.str_to_log_level(level)