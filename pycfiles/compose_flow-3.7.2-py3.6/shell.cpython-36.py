# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/shell.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 895 bytes
import os, sh, shlex
from sh import ErrorReturnCode_1
OS_ENV_INCLUDES = ('DOCKER_HOST', 'HOME', 'PATH', 'USER', 'DISPLAY', 'DBUS_SESSION_BUS_ADDRESS',
                   'KUBECONFIG', 'SSH_AUTH_SOCK', 'SSH_AGENT_PID')

def execute(command: str, env, **kwargs):
    """
    Executes a shell command
    """
    command_split = shlex.split(command)
    _env = env.copy()
    for env_var in OS_ENV_INCLUDES:
        env_val = os.environ.get(env_var)
        if env_val:
            _env.update({env_var: env_val})

    kwargs.update(dict(_env=_env))
    proc = getattr(sh, command_split[0])
    return proc(*command_split[1:], **kwargs)