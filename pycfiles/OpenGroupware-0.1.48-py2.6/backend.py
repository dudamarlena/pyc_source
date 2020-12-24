# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/backend.py
# Compiled at: 2012-10-12 07:02:39
import io, os
from log import *
import ConfigParser, logging, foundation
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from coils.foundation import *
from defaultsmanager import DefaultsManager
from utility import get_server_root
Session = sessionmaker()

def _parse_default_as_bool(value):
    if values is None:
        return False
    else:
        if values == 'YES':
            return True
        return False


class Backend(object):
    _engine = None
    _config = None
    _bundles = None
    _session = None
    _auth = None
    _fs_url = None
    _log = None
    _defaults = None

    @staticmethod
    def __alloc__(**params):
        if Backend._config is None:
            Backend._extra_modules = params.get('extra_modules', [])
            Backend._banned_modules = params.get('banned_modules', [])
            foundation.STORE_ROOT = get_server_root(store_root=params.get('store_root', None))
            Backend._fs_url = ('{0}/fs').format(foundation.STORE_ROOT)
            sd = ServerDefaultsManager()
            log_filename = params.get('log_file', '/var/log/coils.log')
            log_level = LEVELS.get('DEBUG', logging.NOTSET)
            logging.basicConfig(filename=log_filename, level=log_level)
            Backend._log = logging
            logging.debug('Backend initialized')
        return

    def __init__(self, **params):
        if Backend._config is None:
            Backend.__alloc__(**params)
        return

    @staticmethod
    def _parse_default_as_bool(value):
        if values is None:
            return False
        else:
            if values == 'YES':
                return True
            return False

    @staticmethod
    def db_session():
        if Backend._engine is None:
            sd = ServerDefaultsManager()
            Backend._engine = create_engine(sd.orm_dsn, **{'echo': sd.orm_logging})
            Session.configure(bind=Backend._engine)
        return Session()

    @staticmethod
    def get_logic_bundle_names():
        if Backend._bundles is None:
            modules = [
             'coils.logic.foundation',
             'coils.logic.account',
             'coils.logic.address',
             'coils.logic.blob',
             'coils.logic.contact',
             'coils.logic.enterprise',
             'coils.logic.facebook',
             'coils.logic.project',
             'coils.logic.schedular',
             'coils.logic.task',
             'coils.logic.team',
             'coils.logic.twitter',
             'coils.logic.workflow',
             'coils.logic.vista',
             'coils.logic.token']
            modules.extend(Backend._extra_modules)
            for name in Backend._banned_modules:
                if name in modules:
                    modules.remove(name)

            Backend._bundles = modules
        return Backend._bundles

    @staticmethod
    def get_protocol_bundle_names():
        modules = [
         'coils.protocol.dav', 'coils.protocol.freebusy',
         'coils.protocol.proxy', 'coils.protocol.rpc2',
         'coils.protocol.sync', 'coils.protocol.jsonrpc',
         'coils.protocol.perf', 'coils.protocol.horde',
         'coils.protocol.bebrpc', 'coils.protocol.attachfs',
         'coils.protocol.vista']
        modules.extend(Backend._extra_modules)
        for name in Backend._banned_modules:
            if name in modules:
                modules.remove(name)

        return modules

    @staticmethod
    def store_root():
        return foundation.STORE_ROOT

    @staticmethod
    def fs_root():
        return Backend._fs_url

    @staticmethod
    def get_authenticator_options():
        if Backend._auth is None:
            sd = ServerDefaultsManager()
            x = sd.string_for_default('LSAuthLDAPServer')
            if len(x) > 0:
                Backend._log.info('Choosing LDAP for BASIC authentication backend')
                ldap_url = ('ldap://{0}/').format(sd.string_for_default('LSAuthLDAPServer'))
                search_filter = sd.string_for_default('LSAuthLDAPSearchFilter')
                if len(search_filter) == 0:
                    search_filter = None
                Backend._auth = {'authentication': 'ldap', 'url': ldap_url, 
                   'start_tls': 'NO', 
                   'binding': 'SIMPLE', 
                   'search_container': sd.string_for_default('LSAuthLDAPServerRoot'), 
                   'search_filter': search_filter, 
                   'bind_identity': sd.string_for_default('LDAPInitialBindDN'), 
                   'bind_secret': sd.string_for_default('LDAPInitialBindPW'), 
                   'uid_attribute': sd.string_for_default('LDAPLoginAttributeName')}
            else:
                Backend._log.info('Choosing database for BASIC authentication backend')
                Backend._auth = {'authentication': 'db'}
            Backend._auth['trustedHosts'] = sd.default_as_list('PYTrustedHosts')
            Backend._auth['lowerLogin'] = sd.bool_for_default('LSUseLowercaseLogin')
            Backend._auth['allowSpaces'] = sd.bool_for_default('AllowSpacesInLogin')
            Backend._auth['stripDomain'] = sd.bool_for_default('StripAuthenticationDomain')
        return Backend._auth