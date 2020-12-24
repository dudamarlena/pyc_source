# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/context.py
# Compiled at: 2012-10-12 07:02:39
import sys, time, logging, time, uuid
from sqlalchemy import *
from pytz import timezone
from datetime import datetime, timedelta
from coils.foundation import *
from exception import *
from ldapauthenticator import LDAPAuthenticator
from dbauthenticator import DBAuthenticator
from bundlemanager import BundleManager
from accessmanager import AccessManager
from linkmanager import LinkManager
from propertymanager import PropertyManager
from typemanager import TypeManager
from lockmanager import LockManager
from command import Command
from packet import Packet
from useragents import lookup_user_agent
OGO_ROLE_TEAM_ASSIGNMENT = {OGO_ROLE_SYSTEM_ADMIN: 'OGoAdministrativeTeam', OGO_ROLE_HELPDESK: 'OGoHelpDeskRoleName', 
   OGO_ROLE_WORKFLOW_ADMIN: 'OGoWorkflowAdministrativeTeam'}

class Context(object):
    __slots__ = ('_orm', '_pm', '_log', '_queue', '_timezone', '_agent_id', '_agent_data',
                 '_defaults', '_meta', '_lockman', '_am', '_tm', '_dirty', '_stack_depth',
                 '_C_login', '_C_email', '_C_cluster_id', '_C_context_ids', '_C_roles')
    _mapper = None
    _orm = None

    def __init__(self, metadata, broker=None):
        self._orm = None
        self._dm = None
        self._lm = None
        self._pm = None
        self._tm = None
        self._lockman = None
        self._C_roles = None
        self._C_cluster_id = None
        self._C_context_ids = None
        self._C_email = None
        self._C_login = None
        self._stack_depth = 0
        self._log = logging.getLogger('context')
        self._dirty = False
        self._queue = []
        self._meta = metadata
        self._callbacks = {}
        self._uuid = str(uuid.uuid4())
        self._log.debug(('Context {0} created').format(self._uuid))
        if Context._mapper == None:
            Context._mapper = BundleManager()
        self._am = None
        if 'amq_broker' not in metadata and broker is None:
            self._log.debug('AMQ broker not available in context.')
        else:
            self._meta['amq_broker'] = metadata.get('amq_broker', broker)
        if 'connection' in metadata:
            agent_name = metadata['connection'].get('user_agent', None)
        else:
            agent_name = None
        (self._agent_id, self._agent_data) = lookup_user_agent(agent_name)
        self.log.info(('User agent {0} [{1}] select for context (Agent: "{2}")').format(self.user_agent_id, self.user_agent_description['name'], agent_name))
        return

    def __del__(self):
        self.close()

    def close(self):
        """ Close the current context, after this method is called the Context object 
            can no longer be used.  This will drop all pending callbacks and close the
            ORM connection.
        """
        self._log.debug(('Closing context {0}').format(self._uuid))
        self._callbacks = {}
        if self._orm is not None:
            self._orm.close()
            self._orm = None
        return

    @property
    def session_id(self):
        return self._uuid

    @property
    def is_dirty(self):
        return self._dirty

    def dirty(self):
        self._dirty = True

    @property
    def cluster_id(self):
        if self._C_cluster_id is None:
            prop = self.property_manager.get_server_property('http://www.opengroupware.us/global', 'clusterGUID')
            if prop is None:
                raise CoilsException('No cluster id has been generated for this server.')
            self._C_cluster_id = prop.get_value()
        return self._C_cluster_id

    @property
    def type_manager(self):
        if self._tm is None:
            self._tm = TypeManager(self)
        return self._tm

    @property
    def access_manager(self):
        if self._am is None:
            self._am = AccessManager(self)
        return self._am

    @property
    def link_manager(self):
        if self._lm is None:
            self._lm = LinkManager(self)
        return self._lm

    @property
    def property_manager(self):
        if self._pm is None:
            self._pm = PropertyManager(self)
        return self._pm

    @property
    def lock_manager(self):
        if self._lockman is None:
            self._lockman = LockManager(self)
        return self._lockman

    @property
    def log(self):
        return self._log

    @property
    def is_admin(self):
        return self.has_role(OGO_ROLE_SYSTEM_ADMIN)

    def db_session(self):
        if self._orm is None:
            self._log.debug('Allocating new database session.')
            self._orm = Backend.db_session()
            self._log.debug(self._orm.connection().engine.pool.status())
        return self._orm

    def has_role(self, role):

        def load_roles(ctx):
            role_list = []
            sd = ServerDefaultsManager()
            for (role_id, default_name) in OGO_ROLE_TEAM_ASSIGNMENT.items():
                team_name = sd.string_for_default(default_name, value='OGoAdministrators')
                team = self.run_command('team::get', name=team_name)
                if team:
                    if team.object_id in ctx.context_ids:
                        role_list.append(role_id)

            return role_list

        if 10000 in self.context_ids:
            return True
        else:
            if self._C_roles is None:
                self._C_roles = load_roles(self)
            if role in self._C_roles:
                return True
            return False

    def begin(self):
        pass

    def queue_for_commit(self, source, target, data):
        self._queue.append((source, target, data))

    def flush(self):
        self.db_session().flush()

    def commit(self):
        self._log.debug('Context commit requested.')
        self.db_session().commit()
        self._log.debug('Context commit completed.')
        if self._am is not None:
            self._am.clear_cache()
        if len(self._queue) > 0:
            if self.amq_available:
                for notice in self._queue:
                    self.send(notice[0], notice[1], notice[2])

            self._queue = []
        return

    def rollback(self):
        self.db_session().rollback()
        if self._am is not None:
            self._am.clear_cache()
        return

    def run_command(self, command_name_x, **params):
        """ Run the named command with the provided parameters.
            
            :param command_name_x: The fully qualified name of the command to run, such as "contact::new"
            :param params: The paramters to be provided to the command object
        """
        command = Context._mapper.get_command(command_name_x)
        if isinstance(command, Command):
            start = time.time()
            self._stack_depth += 1
            command.prepare(self, **params)
            command.run()
            command.epilogue()
            result = command.get_result()
            end = time.time()
            self._log.debug('duration of %s was %0.3f' % (command_name_x, end - start))
            self._stack_depth += -1
            if self.amq_available:
                self.send(None, 'coils.administrator/performance_log', {'lname': 'logic', 'oname': command_name_x, 
                   'runtime': end - start, 
                   'error': False})
            command = None
            return result
        else:
            self._log.error(('No such command as {0}').format(command_name_x))
            raise CoilsException(('No such command as {0}').format(command_name_x))
            return

    def r_c(self, command_name_x, **params):
        return self.run_command(command_name_x, **params)

    @property
    def defaults_manager(self):
        if self._dm is None:
            self._dm = UserDefaultsManager(self.account_id)
        return self._dm

    def get_timezone(self):
        return timezone('UTC')

    def get_utctime(self):
        utc = timezone('UTC')
        return datetime.now(tz=utc)

    def get_timestamp(self):
        return int(datetime.utcnow().strftime('%s'))

    def as_localtime(self, time):
        if time is None:
            return self.get_localtime()
        else:
            return time.astimezone(self.get_timezone())

    def get_offset_from(self, time):
        return (86400 - self.get_timezone().utcoffset(time).seconds) * -1

    def get_locatime(self):
        tz = self.get_timezone()
        localtime = self.get_utctime().astimezone(tz)

    @property
    def login(self):
        return self.get_login()

    def get_login(self):
        return

    @property
    def email(self):
        if not self._C_email:
            if hasattr(self._C_login, 'company_values'):
                cv = self._C_login.company_values.get('email1', None)
                if cv:
                    self._C_email = cv.string_value
                else:
                    self._C_email = None
        return self._C_email

    @property
    def amq_broker(self):
        return self._meta['amq_broker']

    @property
    def amq_available(self):
        if 'amq_broker' in self._meta:
            return True
        return False

    def send(self, source, target, data, callback=None):
        if self.amq_available:
            packet = Packet(source, target, data)
            self.amq_broker.send(packet, callback=self.callback)
            if callback is not None:
                self._callbacks[packet.uuid] = callback
            return packet.uuid
        else:
            raise CoilsException('Service bus not available to context.')
            return

    def callback(self, uuid, source, target, data):
        if uuid in self._callbacks:
            if self._callbacks[uuid](uuid, source, target, data):
                del self._callbacks[uuid]
                return True
            else:
                return False
        self.log.warn(('Request for callback on packet {0} which has no callback.').format(uuid))

    def wait(self, timeout=1000):
        start = time.time()
        end = start + timeout / 1000.0
        while len(self._callbacks) > 0 and time.time() < end:
            self.amq_broker.wait(timeout=timeout)

        return len(self._callbacks) > 0

    def get_favorited_ids_for_kind(self, kind, refresh=True):
        if self.account_id == 0:
            return []
        kind = kind.lower()
        if kind == 'contact':
            kind = 'person'
        default_name = ('{0}_favorites').format(kind.lower())
        if refresh == False and hasattr(self, ('_cache_{0}').format(default_name)):
            return getattr(self, ('_cache_{0}').format(default_name))
        fav_ids = [ int(x) for x in self.defaults_manager.default_as_list(default_name, []) ]
        setattr(self, ('_cache_{0}').format(default_name), fav_ids)
        return fav_ids

    def set_favorited_ids_for_kind(self, kind, object_ids):
        kind = kind.lower()
        if kind == 'contact':
            kind = 'person'
        default_name = ('{0}_favorites').format(kind.lower())
        if isinstance(object_ids, basestring):
            favorite_ids = favorite_ids.split(',')
        favorite_ids = [ int(x) for x in object_ids ]
        default_name = ('{0}_favorites').format(kind.lower())
        self.defaults_manager.set_default_value(default_name, favorite_ids)
        self.defaults_manager.sync()

    def favorite(self, object_id):
        kind = self.type_manager.get_type(object_id)
        if kind:
            favorites = self.get_favorited_ids_for_kind(kind)
            if object_id not in favorites:
                favorites.append(object_id)
                self.set_favorited_ids_for_kind(kind, favorites)

    def unfavorite(self, object_id):
        object_id = int(object_id)
        kind = self.type_manager.get_type(object_id)
        if kind:
            favorites = self.get_favorited_ids_for_kind(kind)
            if object_id in favorites:
                favorites.remove(object_id)
                self.set_favorited_ids_for_kind(kind, favorites)
            if object_id not in favorites:
                favorites.append(object_id)

    def send_administrative_notice(self, subject=None, message=None, urgency=9, category='unspecified', attachments=[]):
        try:
            self.send(None, 'coils.administrator/notify', {'urgency': urgency, 'category': category, 
               'subject': subject, 
               'message': message})
        except Exception, e:
            self.log.error('Exception attempting to send administrative notice')
            self.log.exception(e)

        return

    def set_user_agent(self, agent_string):
        (self._agent_id, self._agent_data) = lookup_user_agent(agent_string)

    @property
    def user_agent_id(self):
        return self._agent_id

    @property
    def user_agent_description(self):
        return self._agent_data


class AnonymousContext(Context):

    def __init__(self, metadata={}, broker=None):
        Context.__init__(self, metadata, broker=broker)

    @property
    def account_id(self):
        return 0

    @property
    def context_ids(self):
        return [0]

    def get_login(self):
        return 'Coils\\Anonymous'


class NetworkContext(Context):

    def __init__(self, metadata={}, broker=None):
        Context.__init__(self, metadata, broker=broker)

    @property
    def account_id(self):
        return 8999

    @property
    def context_ids(self):
        return [8999]

    def get_login(self):
        return 'Coils\\Network'

    @property
    def email(self):
        sd = ServerDefaultsManager()
        email = sd.string_for_default('AdministrativeEMailAddress', value='root@localhost')
        return email


class AdministrativeContext(Context):

    def __init__(self, metadata={}, broker=None):
        Context.__init__(self, metadata, broker=broker)

    @property
    def account_id(self):
        return 10000

    @property
    def context_ids(self):
        return [10000]

    def get_login(self):
        return 'Coils\\Administrator'


class UserContext(Context):

    def __init__(self, metadata, broker=None):
        Context.__init__(self, metadata, broker=broker)

    def get_defaults(self):
        if self._defaults is None:
            self._defaults = self.run_command('account::get-defaults')
        return self._defaults

    def get_timezone(self):
        if self._timezone is None:
            defaults = self.get_defaults()
            if defaults.has_key('timezone'):
                self._timezone = timezone(defaults['timezone'])
            else:
                self._timezone = timezone('UTC')
        return self._timezone

    @property
    def context_ids(self):
        if self._C_context_ids is None:
            self._C_context_ids = []
            self._C_context_ids.append(self.account_id)
            x = self.run_command('team::get', member_id=self.account_id)
            for team in x:
                self._C_context_ids.append(team.object_id)

        return self._C_context_ids


class AuthenticatedContext(UserContext):
    _auth_class = None
    _auth_options = None
    _defaults = None
    _timezone = None

    def __init__(self, metadata, broker=None):
        UserContext.__init__(self, metadata, broker=broker)
        if AuthenticatedContext._auth_options is None:
            AuthenticatedContext._auth_options = Backend.get_authenticator_options()
        if AuthenticatedContext._auth_class is None:
            class_name = '%sAuthenticator' % AuthenticatedContext._auth_options['authentication'].upper()
            AuthenticatedContext._auth_class = eval(class_name)
        Backend._log.debug(('Authentication class is {0}').format(AuthenticatedContext._auth_class))
        self.authorizor = AuthenticatedContext._auth_class(self, self._meta, AuthenticatedContext._auth_options)
        if self.authorizor.authenticated_id() is None:
            self._log.warn('Unable to authenticate sessoion')
            raise AuthenticationException('Unable to authenticate session')
        else:
            db = self.db_session()
            query = db.query(Contact).filter(and_(Contact.object_id == self.authorizor.authenticated_id(), Contact.is_account == 1, Contact.status != 'archived'))
            data = query.first()
            if data is not None:
                self._C_login = data
        return

    def get_login(self):
        return self._meta['authentication']['login']

    @property
    def account_id(self):
        return self.authorizor.authenticated_id()

    @property
    def account_object(self):
        db = self.db_session()
        query = db.query(Contact).filter(and_(Contact.object_id == self.authorizor.authenticated_id(), Contact.is_account == 1, Contact.status != 'archived'))
        return query.first()


class AssumedContext(UserContext):
    _defaults = None
    _timezone = None

    def __init__(self, context_id, metadata={}, broker=None):
        UserContext.__init__(self, metadata, broker=broker)
        self._get_login(context_id)

    def _get_login(self, context_id):
        db = self.db_session()
        query = db.query(Contact).filter(and_(Contact.object_id == context_id, Contact.is_account == 1, Contact.status != 'archived'))
        data = query.first()
        if data is not None:
            self._C_login = data
        else:
            raise AuthenticationException(('No account with id of {0}.').format(context_id))
        return

    def get_login(self):
        return self._C_login.login

    @property
    def account_id(self):
        return self._C_login.object_id