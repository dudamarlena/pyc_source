# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/project.py
# Compiled at: 2015-03-18 13:43:44
from __future__ import absolute_import
import sys, os, json
from catalyze import output
FILE_PATH = './.git/catalyze-config.json'

def read_settings(required=True):
    if os.path.isdir('./.git'):
        if os.path.isfile(FILE_PATH):
            with open(FILE_PATH, 'r') as (file):
                return json.load(file)
        else:
            if required:
                output.error('No Catalyze environment associated with this local repo. Run "catalyze associate" first.')
            return
    elif required:
        output.error('No git repo found in the current directory.')
    else:
        return
    return


def save_settings(settings):
    with open(FILE_PATH, 'w') as (file):
        json.dump(settings, file)


def clear_settings():
    if os.path.isdir('./.git'):
        if os.path.isfile(FILE_PATH):
            os.remove(FILE_PATH)