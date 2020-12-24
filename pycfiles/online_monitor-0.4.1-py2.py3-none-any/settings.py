# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/utils/settings.py
# Compiled at: 2016-04-14 07:14:14
import ast, sys, os
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

_file_name = os.path.dirname(sys.modules[__name__].__file__) + '/../OnlineMonitor.ini'

def add_converter_path(path):
    config = ConfigParser.SafeConfigParser()
    config.read(_file_name)
    try:
        paths = get_converter_path()
    except ConfigParser.NoOptionError:
        config.set('converter', 'path', str([path])[1:-1])
        with open(_file_name, 'w') as (f):
            config.write(f)
            return

    paths.append(path)
    paths = list(set(paths))
    config.set('converter', 'path', str(paths)[1:-1])
    with open(_file_name, 'w') as (f):
        config.write(f)


def add_receiver_path(path):
    config = ConfigParser.SafeConfigParser()
    config.read(_file_name)
    try:
        paths = get_receiver_path()
    except ConfigParser.NoOptionError:
        config.set('receiver', 'path', str([path])[1:-1])
        with open(_file_name, 'w') as (f):
            config.write(f)
            return

    paths.append(path)
    paths = list(set(paths))
    config.set('receiver', 'path', str(paths)[1:-1])
    with open(_file_name, 'w') as (f):
        config.write(f)


def add_producer_sim_path(path):
    config = ConfigParser.SafeConfigParser()
    config.read(_file_name)
    try:
        paths = get_producer_sim_path()
    except ConfigParser.NoOptionError:
        config.set('producer_sim', 'path', str([path])[1:-1])
        with open(_file_name, 'w') as (f):
            config.write(f)
            return

    paths.append(path)
    paths = list(set(paths))
    config.set('producer_sim', 'path', str(paths)[1:-1])
    with open(_file_name, 'w') as (f):
        config.write(f)


def delete_converter_path(path):
    config = ConfigParser.SafeConfigParser()
    config.read(_file_name)
    paths = [ p for p in get_converter_path() if p != path ]
    config.set('converter', 'path', str(paths)[1:-1])
    with open(_file_name, 'w') as (f):
        config.write(f)


def delete_receiver_path(path):
    config = ConfigParser.SafeConfigParser()
    config.read(_file_name)
    paths = [ p for p in get_receiver_path() if p != path ]
    config.set('receiver', 'path', str(paths)[1:-1])
    with open(_file_name, 'w') as (f):
        config.write(f)


def delete_producer_sim_path(path):
    config = ConfigParser.SafeConfigParser()
    config.read(_file_name)
    paths = [ p for p in get_producer_sim_path() if p != path ]
    config.set('producer_sim', 'path', str(paths)[1:-1])
    with open(_file_name, 'w') as (f):
        config.write(f)


def get_converter_path():
    config = ConfigParser.SafeConfigParser()
    config.read(_file_name)
    path = ast.literal_eval(config.get('converter', 'path'))
    if isinstance(path, tuple):
        return [ p for p in path ]
    return [
     path]


def get_receiver_path():
    config = ConfigParser.SafeConfigParser()
    config.read(_file_name)
    path = ast.literal_eval(config.get('receiver', 'path'))
    if isinstance(path, tuple):
        return [ p for p in path ]
    return [
     path]


def get_producer_sim_path():
    config = ConfigParser.SafeConfigParser()
    config.read(_file_name)
    path = ast.literal_eval(config.get('producer_sim', 'path'))
    if isinstance(path, tuple):
        return [ p for p in path ]
    return [
     path]


def set_window_geometry(geometry):
    config = ConfigParser.SafeConfigParser()
    config.read(_file_name)
    try:
        config.add_section('OnlineMonitor')
    except ConfigParser.DuplicateSectionError:
        pass

    config.set('OnlineMonitor', 'geometry', str(geometry)[1:-1])
    with open(_file_name, 'w') as (f):
        config.write(f)


def get_window_geometry():
    config = ConfigParser.SafeConfigParser()
    config.read(_file_name)
    try:
        return ast.literal_eval(config.get('OnlineMonitor', 'geometry'))
    except ConfigParser.NoSectionError:
        return (100, 100, 1024, 768)