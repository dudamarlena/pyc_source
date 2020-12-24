# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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