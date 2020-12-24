# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/configmaster/SPyCfg.py
# Compiled at: 2015-08-17 15:21:11
import copy
from configmaster.ConfigGenerator import GenerateConfigFile, GenerateNetworkedConfigFile

def construct(data, sandbox=True):
    nloc = copy.copy(locals())
    nglob = copy.copy(globals())
    if sandbox:
        del nglob['__builtins__']
    exec(data, locals=nloc, globals=nglob)
    del nglob
    ndict = {}
    for key, value in nloc.items():
        ndict[key] = value

    return ndict


def load_hook(is_net: bool=False, **kwargs):

    def actual_load_hook(cfg):
        if 'sandbox' in kwargs:
            sandbox = kwargs['sandbox']
        else:
            sandbox = True
        if not is_net:
            data = construct(cfg.fd.read(), sandbox)
        else:
            data = construct(cfg.request.text, sandbox=True)
        cfg.config.load_from_dict(data)

    return actual_load_hook


JSONConfigFile = GenerateConfigFile(load_hook=load_hook(False), dump_hook=None, json_fix=True)
NetworkedJSONConfigFile = GenerateNetworkedConfigFile(load_hook=load_hook(True), normal_class_load_hook=load_hook(False), normal_class_dump_hook=None)