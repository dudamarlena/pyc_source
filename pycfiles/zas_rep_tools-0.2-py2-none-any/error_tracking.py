# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/src/utils/error_tracking.py
# Compiled at: 2018-10-05 13:51:40
import platform
from raven import Client
from raven.processors import SanitizePasswordsProcessor
from zas_rep_tools.src.utils.debugger import p

def initialisation():
    platform_info = {'platform': platform.platform(), 'uname': platform.uname(), 'system': platform.system(), 'processor': platform.processor(), 'machine': platform.machine(), 'version': platform.version(), 'architecture': platform.architecture}
    python_info = {'python_build': platform.python_build(), 'python_compiler': platform.python_compiler(), 'python_implementation': platform.python_implementation(), 'python_version': platform.python_version()}
    user_info = {'platform_info': platform_info, 'python_info': python_info}
    client = Client(dsn='https://0ec650403a06441aa6075e14322a9b15:ba5a980db0064f25b118d724eeb4d877@sentry.io/1213596', auto_log_stacks=True, include_paths=[
     __name__.split('.', 1)[0]], release='0.1', ignore_exceptions=[
     'Http404'], processors=('raven.processors.SanitizePasswordsProcessor', ), sanitize_keys=[
     '_consumer_key', '_consumer_secret', '_access_token', '_access_token_secret'])
    client.module_cache['raven.processors.SanitizePasswordsProcessor'].KEYS = frozenset(['sentry_dsn', 'password', 'passwd', 'access_token', 'secret', 'apikey', 'api_key', 'authorization', '_consumer_key', '_consumer_secret', '_access_token', '_access_token_secret'])
    client.context.merge({'user': user_info})
    return client