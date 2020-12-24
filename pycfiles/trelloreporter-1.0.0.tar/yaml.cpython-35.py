# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/philanim/PycharmProjects/trelloreporter/trelloreporter/config/yaml.py
# Compiled at: 2017-12-06 04:32:14
# Size of source mod 2**32: 798 bytes
import ruamel.yaml, sys

class Yaml(object):

    def read(name):
        with open(name, mode='r') as (f):
            config = ruamel.yaml.load(f, ruamel.yaml.RoundTripLoader)
        return config