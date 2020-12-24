# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cb/Projekter/stonebear/stonebear/push.py
# Compiled at: 2011-09-06 17:58:07
import subprocess

def push(args, config):
    """
    actual function to run the environment command
    """
    envs = config['environments']
    env = args.env[0]
    subprocess.call(config['prepush'], shell=True)
    if env in envs:
        env_cmd = envs[env]
        subprocess.call(env_cmd, shell=True)
    else:
        print "no environment '%s' defined in stonebeard.py" % env
    subprocess.call(config['postpush'], shell=True)