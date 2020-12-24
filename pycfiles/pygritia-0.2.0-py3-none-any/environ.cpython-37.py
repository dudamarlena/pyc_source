# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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