# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nico/computer/venv/lib/python3.4/site-packages/bass/common.py
# Compiled at: 2015-09-06 05:30:54
# Size of source mod 2**32: 792 bytes
"""
bass.common
-----
Basic functions shared by other modules.
"""
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def read_file(filename):
    """read entire file, return content as one string"""
    with open(filename, 'rU') as (f):
        text = ''.join(f.readlines())
    return text


def write_file(text, filename):
    """write text to file"""
    with open(filename, 'w') as (f):
        f.write(text)


def read_yaml_file(path):
    """read file, return YAML content as dictionary"""
    with open(path, 'r') as (f):
        result = load(f, Loader=Loader)
    return result


def read_yaml_string(string):
    """read string, return YAML content as dictionary"""
    result = load(string, Loader=Loader)
    return result