# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/configInstance.py
# Compiled at: 2018-10-03 05:10:51
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import ConfigParser, path, types
from string import strip

def create(filePath, moreSerchPath=[], variables={}, raw=False, case_sensitive=False):
    config = ConfigParser.ConfigParser(allow_no_value=raw, defaults=variables)
    if case_sensitive:
        config.optionxform = lambda option: option
    fp = open(filePath)
    config.readfp(fp)
    fp.close()
    config.items_without_defaults = types.MethodType(items_without_defaults, config)
    config.get_list = types.MethodType(get_list_impl, config)
    config.get_list_list = types.MethodType(get_list_list_impl, config)
    config.get_list_int = types.MethodType(get_list_int_impl, config)
    config.get_list_float = types.MethodType(get_list_float_impl, config)
    config.get_password = types.MethodType(get_password, config)
    config.get_path = types.MethodType(get_path, config)
    config.get_list_path = types.MethodType(get_list_path_impl, config)
    return config


def items_without_defaults(target, section_name, raw=False):
    res = []
    default_section_items = dict(target.items('DEFAULT', raw=raw))
    for s in target.items(section_name, raw=raw):
        if s[0] in target.defaults().keys():
            if s[1] == default_section_items[s[0]]:
                pass
            else:
                res.append(s)
        else:
            res.append(s)

    return res


def get_list_impl(target, section, itemname):
    v = target.get(section, itemname)
    if v == None or v == '':
        return
    v = v.strip()
    v = v[1:-1]
    t = v.split(',')
    return map(strip, t)


def get_list_list_impl(target, section, itemname):
    l1 = get_list_impl(target, section, itemname)
    res = []
    for el in l1:
        tmp = el.split('|')
        res.append(map(strip, tmp))

    return res


def get_list_int_impl(target, section, itemname):
    v = target.get(section, itemname)
    if v == None or v == '':
        return
    v = v.strip()
    v = v[1:-1]
    t = v.split(',')
    res = map(strip, t)
    return map(int, res)


def get_list_float_impl(target, section, itemname):
    v = target.get(section, itemname)
    if v == None or v == '':
        return
    v = v.strip()
    v = v[1:-1]
    t = v.split(',')
    res = map(strip, t)
    return map(float, res)


def get_list_path_impl(target, section, itemname):
    v = target.get(section, itemname)
    if v == None or v == '':
        return
    v = v.strip()
    v = v[1:-1]
    t = v.split(',')
    res = map(strip, t)
    return map(path.path, res)


def get_password(target, section, itemname):
    psw = target.get(section, itemname)
    if psw == None:
        return
    else:
        if psw == 'ask':
            import getpass
            psw = getpass.getpass('insert password:')
        return psw


def get_path(target, section, itemname):
    p = target.get(section, itemname)
    if p == None:
        return
    else:
        return path.path(p)