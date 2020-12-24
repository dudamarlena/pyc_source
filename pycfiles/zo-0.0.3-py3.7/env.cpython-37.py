# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zo/aa/env.py
# Compiled at: 2020-04-02 02:38:39
# Size of source mod 2**32: 2572 bytes
import pathlib, re, time
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
from typing import List, Union, Any
from zo.pydantic import BaseModelValidation, constr, conint
from zo.log import log_level

class _Env(BaseModelValidation):
    validate_assignment = True
    title = ''
    title: constr(min_length=1, max_length=256)
    version = ''
    version: constr(min_length=1, max_length=128)
    debug = False
    debug: bool
    api_prefix = ''
    api_prefix: str
    app_host = '127.0.0.1'
    app_host: constr(regex='^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$')
    app_port = 8000
    app_port: conint(ge=1, le=65536)
    db_host = '127.0.0.1'
    db_host: Union[(constr(regex='^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$'), constr(regex='(d|ssdb)'))]
    db_port = 8000
    db_port: conint(ge=1, le=65536)
    token_secret_key = ''
    token_secret_key: Any
    token_user_expire = 1
    token_user_expire: conint(ge=1)
    allowed_hosts = []
    allowed_hosts: List[str]
    run_app = 'run:app'
    run_app: constr(regex='^(run|main):app$')
    run_reload = False
    run_reload: bool
    run_workers = 1
    run_workers: int
    run_log_level = 'info'
    run_log_level: constr(regex='^(critical|error|warning|info|debug|trace)$')
    run_access_log = False
    run_access_log: bool
    docs_url = None
    docs_url: Union[(constr(regex='^/\\w+'), None)]
    redoc_url = None
    redoc_url: Union[(constr(regex='^/\\w+'), None)]


def get_env(path='.env') -> _Env:
    path = pathlib.Path(path)
    if not path.exists():
        raise AssertionError('.env file not exist')
    else:
        config = Config(path)
        env = _Env()
        env.debug = config('debug', cast=bool, default=False)
        if env.debug:
            env.version = time.strftime('%Y.%m.%d_%H.%M.%S', time.localtime())
            co = re.sub('VERSION = .*', f"VERSION = {env.version}", path.read_text())
            path.write_text(co)
        else:
            env.version = config('version')
    env.title = config('title')
    env.api_prefix = config('api_prefix', default='')
    env.app_host = config('app_host')
    env.app_port = config('app_port', cast=int)
    env.db_host = config('db_host')
    env.db_port = config('db_port', cast=int)
    env.token_secret_key = config('token_secret_key', cast=Secret)
    env.token_user_expire = eval(config('token_user_expire'))
    env.allowed_hosts = list(config('allowed_hosts', cast=CommaSeparatedStrings, default=''))
    env.run_app = config('run_app')
    env.run_reload = config('run_reload')
    env.run_workers = config('run_workers')
    env.run_log_level = config('run_log_level')
    env.run_access_log = config('run_access_log')
    env.docs_url = config('docs_url', default=None) or None
    env.redoc_url = config('redoc_url', default=None) or None
    return env