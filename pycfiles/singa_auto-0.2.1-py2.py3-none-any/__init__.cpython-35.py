# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nailixing/PyProjects/nusdb_rafiki/singa_auto/__init__.py
# Compiled at: 2020-04-24 21:27:49
# Size of source mod 2**32: 1427 bytes
import os, sys

def start_admin():
    model_path = os.path.dirname(__file__).rsplit('/', 1)[0]
    sys.path.append(model_path)
    os.system('python {}'.format(model_path + '/scripts/start_admin.py'))


def start_predictor():
    model_path = os.path.dirname(__file__).rsplit('/', 1)[0]
    sys.path.append(model_path)
    os.system('python {}'.format(model_path + '/scripts/start_predictor.py'))


def start_worker():
    model_path = os.path.dirname(__file__).rsplit('/', 1)[0]
    sys.path.append(model_path)
    os.system('python {}'.format(model_path + '/scripts/start_worker.py'))


from singa_auto.client import Client