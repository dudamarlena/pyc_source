# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/common/serialization.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 784 bytes
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
import yaml

def to_yaml(object_):
    return yaml.dump(object_, default_flow_style=False)


def from_yaml(string):
    return yaml.load(string)