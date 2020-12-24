# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dropbox\dropbox\projects\python\do-pack\do\config.py
# Compiled at: 2018-03-04 17:08:18
# Size of source mod 2**32: 894 bytes
"""
Retrieve and load the user inputs for common fields.
config command.
"""
import os, json
path_config = os.path.join(os.path.dirname(__file__), 'config.json')

def load_json():
    """
    Load the config.json
    """
    with open(path_config, 'r') as (f):
        return json.load(f)


def write_json(author, mail):
    """
    Retrieves the input info form do.config()
    and write the confit.json.
    """
    loaded_config = load_json()
    loaded_config['default_author'] = author
    loaded_config['default_mail'] = mail
    with open(path_config, 'w') as (f):
        json.dump(loaded_config, f)


def show_common(field):
    """
    return the default data for the assistant command
    """
    loaded_config = load_json()
    return loaded_config[field]


if __name__ == '__main__':
    pass