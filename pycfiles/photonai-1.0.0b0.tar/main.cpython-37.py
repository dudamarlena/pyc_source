# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/investigator/app/main.py
# Compiled at: 2019-09-26 08:58:51
# Size of source mod 2**32: 702 bytes
import os
from flask import Flask
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
base_dir = os.path.join(base_dir, 'investigator')
base_dir = os.path.join(base_dir, 'app')
template_dir = os.path.join(base_dir, 'templates')
app = Flask(__name__, template_folder=template_dir)
app.config['pipe_files'] = {}
app.config['pipe_objects'] = {}
app.config['SECRET_KEY'] = 'Random_Lovely_Key'
app.config['DEBUG'] = False
from pymodm.connection import connect
connect('mongodb://trap-umbriel:27017/photon_results')
from photonai.investigator.app.controller import default, hyperpipe, outer_fold, configuration, ajax