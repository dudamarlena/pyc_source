# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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