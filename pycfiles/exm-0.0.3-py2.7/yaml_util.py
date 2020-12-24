# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\exm\utils\yaml_util.py
# Compiled at: 2019-03-10 13:53:12
import re, os, yaml, expression

def load(file):
    conf = {}
    with open(file, 'r') as (input):
        conf = yaml.load(input)
    systemenv = dict(os.environ)
    env = {}
    env.update(systemenv)
    env.update(conf)
    env['system'] = systemenv
    conf['system'] = systemenv
    expression.evaluate(env, conf)
    return conf