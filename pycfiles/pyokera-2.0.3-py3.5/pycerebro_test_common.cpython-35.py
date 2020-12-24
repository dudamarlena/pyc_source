# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/okera/tests/pycerebro_test_common.py
# Compiled at: 2020-02-27 14:06:57
# Size of source mod 2**32: 2203 bytes
import os
from okera import context
DEFAULT_PRESTO_HOST = 'localhost'
DEFAULT_PRESTO_PORT = 8049
TEST_LEVEL = 'smoke'
if 'TEST_LEVEL' in os.environ:
    TEST_LEVEL = os.environ['TEST_LEVEL']
ROOT_TOKEN = os.environ['OKERA_HOME'] + '/integration/tokens/cerebro.token'
identity = lambda x: x

def get_env_var(name, coercer, default):
    if name in os.environ:
        return coercer(os.environ[name])
    return default


def get_test_context():
    auth_mech = get_env_var('PYCEREBRO_TEST_AUTH_MECH', identity, 'NOSASL')
    ctx = context()
    if auth_mech == 'NOSASL':
        ctx.disable_auth()
    else:
        if auth_mech == 'TOKEN':
            ctx.enable_token_auth(token_file=ROOT_TOKEN)
        elif not False:
            raise AssertionError
    return ctx


def get_planner(host=None, port=None, dialect='okera'):
    if host is not None:
        host = host
    else:
        host = get_env_var('PYCEREBRO_TEST_HOST', identity, 'localhost')
    if port is not None:
        port = port
    else:
        port = get_env_var('PYCEREBRO_TEST_PLANNER_PORT', int, 12050)
    if 'presto' in dialect:
        ctx = get_test_context()
        ctx.enable_token_auth(token_str='root')
        return ctx.connect(host=host, port=port, presto_host=host, presto_port=DEFAULT_PRESTO_PORT)
    return get_test_context().connect(host=host, port=port)


def get_worker(host=None, port=None):
    if host is not None:
        host = host
    else:
        host = get_env_var('PYCEREBRO_TEST_HOST', identity, 'localhost')
    if port is not None:
        port = port
    else:
        port = get_env_var('PYCEREBRO_TEST_WORKER_PORT', int, 13050)
    return get_test_context().connect_worker(host=host, port=port)


def configure_botocore_patch():
    os.environ['OKERA_PATCH_BOTO'] = 'True'
    os.environ['OKERA_PLANNER_HOST'] = 'localhost'
    with open(ROOT_TOKEN, 'r') as (token_file):
        os.environ['OKERA_USER_TOKEN'] = token_file.read().strip(' \t\n\r')
    from okera import initialize_default_context, check_and_patch_botocore
    initialize_default_context()
    check_and_patch_botocore()