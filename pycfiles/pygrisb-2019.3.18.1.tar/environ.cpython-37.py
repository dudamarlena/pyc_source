# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/run/environ.py
# Compiled at: 2019-02-22 23:25:03
# Size of source mod 2**32: 584 bytes
import os, subprocess

def get_env_dict(key='SLURM_'):
    """get a list of environment variables containing key word of key.
    """
    envs = {}
    for e in os.environ:
        if key in e:
            envs[e] = os.environ[e]

    return envs


def unset_environ(envs):
    """unset the list of environment variables envs.
    """
    for e in envs:
        if e in os.environ:
            del os.environ[e]


def set_environ(envs):
    """set the list of environment variables envs.
    """
    for e in envs:
        if e not in os.environ:
            os.environ[e] = envs[e]