# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/commonruntime/Settings.py
# Compiled at: 2020-01-20 08:59:43
# Size of source mod 2**32: 7795 bytes
""" Class description goes here. """
import logging, os
from dataclay.commonruntime.SettingsLoader import AccountIdLoader, AccountCredentialLoader, AbstractLoader
from dataclay.exceptions.exceptions import ImproperlyConfigured
from dataclay.util.PropertiesFilesLoader import PropertyDict
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'
logger = logging.getLogger(__name__)
FIELD_ACCOUNT = 'Account'
FIELD_PASSWORD = 'Password'
FIELD_STUBSFOLDER = 'StubsClasspath'
FIELD_DATASETS = 'DataSets'
FIELD_DATASETFORSTORE = 'DataSetForStore'
FIELD_CLIENTCONFIG = 'DataClayClientConfig'
FIELD_GLOBALCONFIG = 'DataClayGlobalConfig'
FIELD_LOCAL_BACKEND = 'LocalBackend'
FIELD_TRACING_ENABLED = 'Tracing'
FIELD_EXTRAE_STARTING_TASK_ID = 'ExtraeStartingTaskID'
FIELD_CLIENT_HOST = 'HOST'
FIELD_CLIENT_TCPPORT = 'TCPPORT'
UNSET_FIELD = object()

class _SettingsHub(object):
    __doc__ = 'Application-wide configuration holder.\n\n    This class holds values for all the configuration. It has some defaults,\n    but a load from the properties file will overwrite the class values for\n    specific instance values.\n\n    Note that any lookup previous to a load_properties will raise an\n    ImproperlyConfigured exception.\n    '
    loaded = False

    def __init__(self):
        self._values = {'logicmodule_host':'127.0.0.1', 
         'logicmodule_port':'2127', 
         'logicmodule_rmiport':'2127', 
         'logicmodule_dc_instance_id':None, 
         'network_timeout':7200, 
         'local_backend_name':None, 
         'admin_user':os.getenv('DATACLAY_ADMIN_USER', 'admin'), 
         'admin_password':os.getenv('DATACLAY_ADMIN_PASSWORD', 'admin'), 
         'admin_id':AccountIdLoader(self, 'admin_user'), 
         'admin_credential':AccountCredentialLoader(self, 'admin_id', 'admin_password'), 
         'current_user':UNSET_FIELD, 
         'current_password':UNSET_FIELD, 
         'current_id':AccountIdLoader(self, 'current_user'), 
         'current_credential':AccountCredentialLoader(self, 'current_id', 'current_password'), 
         'current_session_id':UNSET_FIELD, 
         'stubs_folder':UNSET_FIELD, 
         'datasets':UNSET_FIELD, 
         'dataset_for_store':UNSET_FIELD, 
         'dataset_id':UNSET_FIELD, 
         'tracing_enabled':False, 
         'extrae_starting_task_id':'0'}

    def load_properties(self, file_name):
        """Load all the properties.

        Take a properties file and load all the settings used typically by the
        client application.
        """
        dirname = os.getcwd()
        d = PropertyDict(file_name)
        logger.debug('Reading properties file %s', file_name)
        try:
            self._values['current_user'] = getattr(d, FIELD_ACCOUNT)
            self._values['current_password'] = getattr(d, FIELD_PASSWORD)
            self._values['stubs_folder'] = os.path.realpath(os.path.join(dirname, getattr(d, FIELD_STUBSFOLDER)))
            self._values['datasets'] = getattr(d, FIELD_DATASETS).split(':')
            self._values['dataset_for_store'] = getattr(d, FIELD_DATASETFORSTORE)
            try:
                self._values['extrae_starting_task_id'] = int(getattr(d, FIELD_EXTRAE_STARTING_TASK_ID))
            except AttributeError:
                logger.debug('Extrae starting task ID not defined')

            try:
                self._values['tracing_enabled'] = bool(getattr(d, FIELD_TRACING_ENABLED))
            except AttributeError:
                logger.debug('Tracing enabled conf. not defined')

            try:
                client_config_path = os.path.realpath(os.path.join(dirname, getattr(d, FIELD_CLIENTCONFIG)))
            except AttributeError:
                client_config_path = os.getenv('DATACLAYCLIENTCONFIG')
                if not client_config_path:
                    client_config_path = os.path.realpath('./cfgfiles/client.properties')

            if not client_config_path:
                raise AttributeError('Client config cannot be found neither from session file nor any default env / path')
            try:
                global_config_path = os.path.realpath(os.path.join(dirname, getattr(d, FIELD_GLOBALCONFIG)))
                Configuration.read_from_file(global_config_path)
            except AttributeError:
                pass

        except AttributeError:
            logger.error('Some required attribute was missing, reraising the AttributeError')
            raise

        self.load_connection(client_config_path)
        if hasattr(d, FIELD_LOCAL_BACKEND):
            self._values['local_backend_name'] = getattr(d, FIELD_LOCAL_BACKEND)

    def load_connection(self, file_name):
        """Load the connection settings values.

        This method may be used standalone or called from the more complete
        load_properties.
        """
        client_d = PropertyDict(file_name)
        try:
            self._values['logicmodule_host'] = getattr(client_d, FIELD_CLIENT_HOST)
            self._values['logicmodule_port'] = int(getattr(client_d, FIELD_CLIENT_TCPPORT))
        except AttributeError:
            logger.error('CLIENTCONFIG file (typically client.properties) requires both %s and %p', FIELD_CLIENT_HOST, FIELD_CLIENT_TCPPORT)
            raise

        self.loaded = True

    def __getattr__(self, item):
        if not self.loaded:
            raise ImproperlyConfigured('The settings should be loaded before lookups')
        try:
            ret = self._values[item]
        except KeyError:
            raise ImproperlyConfigured("Key '%s' not recognized as a valid setting" % item)

        if ret is UNSET_FIELD:
            raise ImproperlyConfigured("The setting for '%s' has not been set" % item)
        if isinstance(ret, AbstractLoader):
            loaded = ret.load_value()
            self._values[item] = loaded
            return loaded
        return ret

    def __setattr__(self, key, value):
        if key == 'loaded':
            if value is not True:
                raise RuntimeError('Unloading a settings is not permitted')
            object.__setattr__(self, key, value)
        else:
            if key == '_values':
                object.__setattr__(self, key, value)
            else:
                self._values[key] = value


settings = _SettingsHub()