# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/david/flask_proj/polarishub_flask/polarishub_flask/server/file_handler.py
# Compiled at: 2019-08-27 21:47:22
# Size of source mod 2**32: 1645 bytes
import os, sys, json
from flask import abort
from polarishub_flask.server.parser import printv
settings = {}

def load_settings():
    with open(os.path.join(os.getcwd(), 'server', 'settings.json')) as (f):
        return json.load(f)


def get_settings():
    global settings
    if settings == {} or settings is None:
        settings = load_settings()
    return settings


def save_settings():
    try:
        with open(os.path.join(os.getcwd(), 'server', 'settings.json'), 'w') as (f):
            json.dump(settings, f)
        return True
    except:
        return False


def get_dir(path):
    if os.path.isdir(path):
        path_list = os.listdir(path)
        printv(os.getcwd())
        path_list = [(path_list[i], os.path.isfile(os.path.join(path, path_list[i])), os.path.join(path[len(os.getcwd()):], path_list[i])) for i in range(len(path_list))]
        printv('path_list', path_list)
        return path_list
    abort(404)


keys = {'username': lambda name: len(name) > 0}

def update_settings(new_settings):
    global settings
    printv(new_settings)
    for key, value in new_settings.items():
        printv((key, value))
        if key in keys.keys() and keys[key](value):
            printv('key gets:', key)
            printv(key, value)
            if value:
                settings[key] = value
        else:
            settings = load_settings()
            return False

    if save_settings():
        return True
    else:
        return False