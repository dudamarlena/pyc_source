# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/investigator/app/main/main.py
# Compiled at: 2019-09-11 10:06:06
# Size of source mod 2**32: 797 bytes
import os
from flask import Flask
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
base_dir = os.path.join(base_dir, 'app')
base_dir = os.path.join(base_dir, 'main')
template_dir = os.path.join(base_dir, 'templates')
application = Flask(__name__, template_folder=template_dir)
application.config['pipe_files'] = {}
application.config['pipe_objects'] = {}
application.config['wizard'] = True
application.config['SECRET_KEY'] = 'Random_Lovely_Key'
application.config['DEBUG'] = False
from pymodm.connection import connect
connect('mongodb://trap-umbriel:27017/photon_results')
from .controller import default, ajax, hyperpipe, outer_fold, configuration