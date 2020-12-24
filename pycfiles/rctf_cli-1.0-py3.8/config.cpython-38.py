# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rctf-cli/rctf/config.py
# Compiled at: 2020-03-23 01:59:17
# Size of source mod 2**32: 4058 bytes
import collections, envparse, os, sys, json
from . import logging, execute, check_file, colored_command

def read_env(fname):
    env_backup = envparse.os.environ
    envparse.os.environ = dict()
    envparse.env.read_envfile(fname)
    contents = envparse.os.environ
    envparse.os.environ = env_backup
    return contents


class Config(collections.OrderedDict):
    config_keys = {'RCTF_NAME':'ctf.name', 
     'RCTF_ORIGIN':'ctf.origin', 
     'RCTF_DATABASE_URL':'db.url', 
     'RCTF_REDIS_URL':'redis.url', 
     'RCTF_SMTP_URL':'smtp.url', 
     'RCTF_EMAIL_FROM':'smtp.from'}
    default_config = collections.OrderedDict({'cli.ansi': True})

    def __init__(self, config_path, *args, dotenv_path=None, **kwargs):
        retval = (super().__init__)(*args, **kwargs)
        self.config_path = config_path
        self.dotenv_path = dotenv_path
        self.get = self._Config__get
        self.set = self._Config__set
        return retval

    def __get(self, key, default=None):
        if key in self:
            return str(self[key])
        return default

    def get_bool(self, *args, **kwargs):
        return str((self.get)(*args, **kwargs).strip().lower()) in ('true', '1', 'enable',
                                                                    'true')

    def get_int(self, *args, **kwargs):
        return int(str((self.get)(*args, **kwargs).strip()))

    def __set(self, key, value):
        self[key] = str(value)
        return key

    def read(self, update_config=False):
        if self.config_path == '':
            raise RuntimeError('Attempted to read dummy config path')
        elif not update_config:
            check_file(self.config_path) or print('kk')
            logging.debug('Config file ', colored_command(self.config_path), ' does not exist, using default config...')
            config = Config.default_config.copy()
            if update_config:
                config = self.read(update_config=False)
            if self.dotenv_path:
                logging.debug('... and importing config from dotenv file ', colored_command(self.dotenv_path))
                dotenv_config = read_env(self.dotenv_path)
                for key in sorted(dotenv_config.keys()):
                    value = dotenv_config[key]
                    if key in Config.config_keys:
                        config[Config.config_keys[key]] = str(value)

            self.clear()
            self.update(config)
            self.write()
        else:
            with open(self.config_path, 'r') as (f):
                config = json.loads((f.read()), object_pairs_hook=(collections.OrderedDict))
            self.clear()
            self.update(config)
        return self

    def write--- This code section failed: ---

 L. 120         0  LOAD_FAST                'self'
                2  LOAD_ATTR                config_path
                4  LOAD_STR                 ''
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 121        10  LOAD_GLOBAL              RuntimeError
               12  LOAD_STR                 'Attempted to write dummy config path'
               14  CALL_FUNCTION_1       1  ''
               16  RAISE_VARARGS_1       1  'exception instance'
             18_0  COME_FROM             8  '8'

 L. 123        18  LOAD_GLOBAL              json
               20  LOAD_ATTR                dumps
               22  LOAD_FAST                'self'
               24  LOAD_CONST               2
               26  LOAD_CONST               ('indent',)
               28  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               30  STORE_FAST               'config'

 L. 125        32  LOAD_GLOBAL              open
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                config_path
               38  LOAD_STR                 'w'
               40  CALL_FUNCTION_2       2  ''
               42  SETUP_WITH           68  'to 68'
               44  STORE_FAST               'f'

 L. 126        46  LOAD_FAST                'f'
               48  LOAD_METHOD              write
               50  LOAD_FAST                'config'
               52  CALL_METHOD_1         1  ''
               54  POP_BLOCK        
               56  ROT_TWO          
               58  BEGIN_FINALLY    
               60  WITH_CLEANUP_START
               62  WITH_CLEANUP_FINISH
               64  POP_FINALLY           0  ''
               66  RETURN_VALUE     
             68_0  COME_FROM_WITH       42  '42'
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  END_FINALLY      

 L. 130        74  LOAD_GLOBAL              os
               76  LOAD_METHOD              chmod
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                config_path
               82  LOAD_CONST               384
               84  CALL_METHOD_2         2  ''
               86  POP_TOP          

Parse error at or near `ROT_TWO' instruction at offset 56

    def _get_as_environ(self):
        envvars = dict()
        reverse_config_keys = {key:value for key, value in Config.config_keys.items()}
        for key, value in self.items():
            if key in reverse_config_keys:
                envvars[reverse_config_keys[key]] = str(value)
            else:
                if not key.startswith('cli.'):
                    envvars[key] = str(value)
                return envvars