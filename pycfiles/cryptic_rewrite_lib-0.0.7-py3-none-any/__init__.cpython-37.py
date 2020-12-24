# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cryptic/__init__.py
# Compiled at: 2019-07-27 19:54:24
# Size of source mod 2**32: 16606 bytes
import json, os, socket, threading, time
from os import environ
from typing import Tuple, Dict, Callable, List, Union, NoReturn, Any, Optional
from uuid import uuid4
import logging, scheme
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import sessionmaker
import sentry_sdk
from sentry_sdk import capture_exception, configure_scope

class IllegalArgumentError(ValueError):
    pass


class IllegalReturnTypeError(ValueError):
    pass


class UnknownDBMSTypeError(ValueError):
    pass


class UnknownModeError(ValueError):
    pass


class Config:
    to_load = [
     ('MODE', 'production'),
     ('DATA_LOCATION', 'data/'),
     ('DBMS', 'sqlite'),
     ('SQLITE_FILE', 'data.db'),
     ('MYSQL_HOSTNAME', ''),
     ('MYSQL_PORT', ''),
     ('MYSQL_DATABASE', ''),
     ('MYSQL_USERNAME', ''),
     ('MYSQL_PASSWORD', ''),
     ('RECYCLE_POOL', 1550),
     ('PATH_LOGFILE', 'log_files/'),
     ('DSN', ''),
     ('RELEASE', '')]
    to_load: List[Tuple[(str, str)]]

    def __init__(self):
        self._Config__config = {}
        for key in Config.to_load:
            if isinstance(key, tuple):
                if key[0] in os.environ:
                    self._Config__config[key[0]] = os.environ.get(key[0])
                else:
                    self._Config__config[key[0]] = key[1]

    def __contains__(self, item: str):
        return item in self._Config__config

    def __getitem__(self, item: str) -> Optional[str]:
        if item in self:
            return self._Config__config[item]

    def __setitem__(self, key: str, value: Any):
        self._Config__config[key] = value

    def set_mode(self, mode):
        if mode.lower() in ('debug', 'production'):
            self['mode'] = mode
        else:
            raise UnknownModeError(f"the mode {mode} is unknown")


_config = Config()

class Sentry(logging.Logger):

    def __init__(self, name):
        super().__init__(self, logging.INFO)
        self._Sentry__using_sentry = False
        self._name = name
        self._Sentry__setup_logger()
        self._Sentry__setup_sentry()

    def __setup_logger(self) -> None:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_format)
        if _config['PATH_LOGFILE'] != '':
            if _config['PATH_LOGFILE'][(-1)] == '/':
                file_handler = logging.FileHandler(_config['PATH_LOGFILE'] + self._name + '.log')
                file_handler.setLevel(logging.DEBUG)
                file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(file_format)
                self.addHandler(file_handler)
        self.addHandler(console_handler)
        self.info('logger configured ...')

    def __setup_sentry(self) -> None:
        if _config['DSN'] != '':
            sentry_sdk.init(dsn=(_config['DSN']), release=(_config['RELEASE']))
            self._Sentry__using_sentry = True
            logging.info('Setup SDK was performed DSN:', _config['DSN'])

    def capture_exception(self, e: Exception, **kwargs) -> None:
        self.error(e, exc_info=True)
        if self._Sentry__using_sentry:
            capture_exception(e)
            with configure_scope() as (scope):
                for key in kwargs:
                    scope.set_extra(key, kwargs[key])


class DatabaseWrapper:

    def __init__(self):
        if _config['MODE'] == 'debug':
            _config['DBMS'] = 'sqlite'
        elif _config['MODE'] == 'production':
            _config['DBMS'] = 'mysql'
        self.engine = None
        self.session = None
        self.Session = None
        self.Base = None
        self.connection = None
        self.setup_database()

    @staticmethod
    def __setup_sqlite(filename: str, storage_location: str='data/') -> Engine:
        """
        :param filename: The filename
        :param storage_location: The directory the database file will be stored
        :return: Tuple[DeclarativeMeta, Any] where "Any" really is of the type sessionmaker(bind=engine)() returns
        """
        if not os.path.exists(storage_location):
            os.makedirs(storage_location)
        return create_engine('sqlite:///' + os.path.join(storage_location, filename))

    @staticmethod
    def __setup_mysql(username: str, password: str, hostname: str, port: int, database: str) -> Engine:
        assert 0 < port <= 65535, 'invalid port number'
        return create_engine(f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}",
          pool_recycle=(_config['RECYCLE_POOL']))

    def setup_database(self) -> None:
        if _config['DBMS'] == 'sqlite':
            self.engine = self._DatabaseWrapper__setup_sqlite(filename=(_config['SQLITE_FILE']),
              storage_location=(_config['DATA_LOCATION']))
        elif _config['DBMS'] == 'mysql':
            port = _config['MYSQL_PORT']
            if not port.isdecimal():
                raise Exception('in qua iacet forsit animadverto se?')
            port = int(port)
            self.engine = self._DatabaseWrapper__setup_mysql(username=(_config['MYSQL_USERNAME']),
              password=(_config['MYSQL_PASSWORD']),
              hostname=(_config['MYSQL_HOSTNAME']),
              port=port,
              database=(_config['MYSQL_DATABASE']))
        else:
            raise UnknownDBMSTypeError(f"the DBMS {_config['DBMS']} is unknown")
        self.Session = sessionmaker(bind=(self.engine))
        self.Base = declarative_base()
        self.session = self.Session()
        self.connection = self.session.connection()

    def reload(self) -> None:
        self.Session = sessionmaker(bind=(self.engine))
        self.session = self.Session()
        self.connection = self.session.connection()

    def ping(self) -> None:
        try:
            self.connection.scalar(select([1]))
            return
        except Exception as e:
            try:
                self.reload()
            finally:
                e = None
                del e


class MicroService:
    SERVICE_REQUEST_MAX_TIMEOUT = 10

    def __init__(self, name: str, server_address: Tuple[(str, int)]=None):
        self._sentry = Sentry(name)
        self._user_endpoints = {}
        self._ms_endpoints = {}
        self._user_endpoint_requirements = {}
        self._name = name
        self._awaiting = []
        self._data = {}
        self._database = DatabaseWrapper()
        if server_address is not None:
            assert len(server_address) == 2, 'the server host tuple has to be like (str, int)'
            assert 0 <= server_address[1] <= 65535, 'port has to be in the range of 0 - 65535'
            self._server_address = server_address
        else:
            self._server_address = [
             '127.0.0.1', 1239]
            if 'SERVER_HOST' in environ:
                self._server_address[0] = environ['SERVER_HOST']
            if 'SERVER_PORT' in environ:
                self._server_address[1] = int(environ['SERVER_PORT'])
            self._server_address = tuple(self._server_address)
        self._MicroService__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __send(self, data: dict) -> NoReturn:
        try:
            self._MicroService__sock.send(str(json.dumps(data)).encode('utf-8'))
        except socket.error:
            self._MicroService__reconnect()
        except json.JSONDecodeError as e:
            try:
                self._sentry.info('invalid json:', str(data))
                self._sentry.capture_exception(e, data=data)
            finally:
                e = None
                del e

    def __connect(self) -> NoReturn:
        while True:
            try:
                self._MicroService__sock.connect(self._server_address)
                return
            except socket.error:
                time.sleep(0.5)

    def __register(self) -> NoReturn:
        self._MicroService__send({'action':'register',  'name':self._name})

    def __exec(self, frame):
        if 'tag' in frame:
            if 'data' in frame:
                data = frame['data']
                tag = frame['tag']
                endpoint = tuple(frame['endpoint'])
                if tag in self._awaiting:
                    self._data[tag] = data
                elif 'ms' in frame:
                    if endpoint not in self._ms_endpoints:
                        self._sentry.debug('ms requested: ' + str(endpoint) + ' Endpoint not found')
                        self._MicroService__send({'tag':tag,  'ms':frame['ms'],  'data':{'error': 'unknown_service'}})
                        return
                    requesting_microservice = frame['ms']
                    self._database.ping()
                    try:
                        return_data = self._ms_endpoints[endpoint](data, requesting_microservice)
                    except Exception as e:
                        try:
                            self._sentry.capture_exception(e, endpoint=endpoint, data=frame)
                            return_data = {}
                        finally:
                            e = None
                            del e

                    if return_data is None:
                        return_data = {}
                    elif not isinstance(return_data, dict):
                        raise IllegalReturnTypeError('all handler functions are expected to return either noting or a dict.')
                    self._MicroService__send({'ms':requesting_microservice,  'endpoint':[],  'tag':tag,  'data':return_data})
                elif 'user' in frame:
                    if endpoint not in self._user_endpoints:
                        self._sentry.debug('user requested: ' + str(endpoint) + ' Endpoint not found')
                        self._MicroService__send({'tag':tag,  'user':frame['user'],  'data':{'error': 'unknown_service'}})
                        return
                        self._database.ping()
                        requirements = self._user_endpoint_requirements[endpoint]
                        if requirements is not None:
                            try:
                                requirements.serialize(data, 'json')
                            except:
                                self._sentry.debug('invalid input data: ' + str(data))
                                self._MicroService__send({'tag':tag,  'data':{'error': 'invalid_input_data'}})
                                return

                    else:
                        try:
                            return_data = self._user_endpoints[endpoint](data, frame['user'])
                        except Exception as e:
                            try:
                                self._sentry.capture_exception(e, endpoint=endpoint, data=frame)
                                return_data = {}
                            finally:
                                e = None
                                del e

                    if return_data is None:
                        return_data = {}
                    elif not isinstance(return_data, dict):
                        raise IllegalReturnTypeError('all handler functions are expected to return either noting or a dict.')
                    self._MicroService__send({'tag':tag,  'data':return_data})

    def __start(self) -> NoReturn:
        while True:
            try:
                data = self._MicroService__sock.recv(4096)
                if len(data) == 0:
                    self._MicroService__reconnect()
                    continue
                frame = json.loads(data)
                threading.Thread(target=(self._MicroService__exec), args=(frame,)).start()
            except json.JSONDecodeError as e:
                try:
                    self._sentry.debug('Error when trying to load json: ' + str(data))
                    self._sentry.capture_exception(e, data=(str(data)))
                    continue
                finally:
                    e = None
                    del e

            except socket.error:
                self._sentry.info('Lost connection to main server ... reconnect')
                self._MicroService__reconnect()
                continue

    def __reconnect(self):
        self._MicroService__sock.close()
        self._MicroService__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Connection closed by server ... trying to reconnect')
        while True:
            try:
                self._MicroService__connect()
                self._MicroService__register()
                print('Reconnected')
                break
            except socket.error as e:
                try:
                    time.sleep(0.5)
                finally:
                    e = None
                    del e

    def run(self) -> NoReturn:
        self._MicroService__connect()
        self._MicroService__register()
        self._MicroService__start()

    def __endpoint(self, path: Union[(List[str], Tuple[(str, ...)])], requires: Optional[scheme.Structure]=None, for_user_request: bool=False) -> Callable:

        def decorator(func):
            if isinstance(path, list):
                endpoint_path = tuple(path)
            elif isinstance(path, tuple):
                endpoint_path = path
            else:
                raise IllegalArgumentError('endpoint(...) expects a list or tuple as endpoint.')
            if for_user_request:
                self._user_endpoints[endpoint_path] = func
                self._user_endpoint_requirements[endpoint_path] = requires
            else:
                self._ms_endpoints[endpoint_path] = func

            def inner(*args, **kwargs) -> NoReturn:
                print('This function is not directly callable.')

            return inner

        return decorator

    def microservice_endpoint(self, path: Union[(List[str], Tuple[(str, ...)])]) -> Callable:
        return self._MicroService__endpoint(path, None, False)

    def user_endpoint(self, path: Union[(List[str], Tuple[(str, ...)])], requires: Optional[Dict[(str, scheme.field.Field)]]) -> Callable:
        if requires is not None:
            for req in requires.values():
                req.required = True

            requirements = scheme.Structure(requires, name=('/'.join(path)))
            return self._MicroService__endpoint(path, requirements, True)
        return self._MicroService__endpoint(path, None, True)

    def contact_microservice(self, name: str, endpoint: List[str], data: dict, uuid: Union[(None, str)]=None):
        if uuid is None:
            uuid = str(uuid4())
        self._MicroService__send({'ms':name,  'data':data,  'tag':uuid,  'endpoint':endpoint})
        self._awaiting.append(uuid)
        time_start_waiting = time.time()
        while uuid not in self._data.keys():
            time.sleep(0.001)
            if time.time() - time_start_waiting > MicroService.SERVICE_REQUEST_MAX_TIMEOUT:
                raise TimeoutError()

        data = self._data[uuid]
        self._awaiting.remove(uuid)
        del self._data[uuid]
        return data

    def contact_user(self, user_id: str, data: dict):
        self._MicroService__send({'action':'address',  'user':user_id,  'data':data})

    def get_db_session(self) -> Tuple[(Engine, DeclarativeMeta, Any)]:
        return (
         self._database.engine, self._database.Base, self._database.session)

    def get_wrapper(self) -> 'DatabaseWrapper':
        return self._database


def get_config(mode: Optional[str]=None) -> Config:
    if mode:
        _config.set_mode(mode)
    return _config