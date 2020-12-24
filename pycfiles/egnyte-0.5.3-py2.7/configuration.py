# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/egnyte/configuration.py
# Compiled at: 2017-05-16 04:49:01
import os.path, json

def add_directory(filepath):
    """
    Add '~/.egnyte' in a platform independent way to a file path it it's relative.
    """
    if os.path.isabs(filepath):
        return filepath
    return os.path.join(os.path.expanduser('~'), '.egnyte', filepath)


def load(filename=None):
    """
    Load configuration from a JSON file.
    If filename is None, ~/.egnyte/config.json will be loaded.
    If filename is not an absolute path, it will be prefixed with ~/.egnyte/
    Returns loaded config as a dictionary on success and {} on failure.
    """
    filename = add_directory(filename or 'config.json')
    try:
        with open(filename, 'r') as (f):
            return json.load(f)
    except IOError:
        pass

    return {}


def save(config, filename=None):
    """
    Load configuration from a JSON file.
    If filename is not an absolute path, it will be prefixed with ~/.egnyte/
    """
    filename = add_directory(filename or 'config.json')
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory, 448)
    with open(filename, 'w') as (f):
        json.dump(config, f, indent=2, sort_keys=True)