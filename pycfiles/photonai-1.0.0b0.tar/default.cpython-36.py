# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/investigator/app/main/controller/default.py
# Compiled at: 2019-09-11 10:06:06
# Size of source mod 2**32: 479 bytes
from flask import render_template
from ..main import application
from .helper import shutdown_server, load_available_pipes

@application.route('/')
def index():
    available_pipes = load_available_pipes()
    return render_template('default/index.html', available_pipes=available_pipes)


@application.route('/shutdown', methods=['GET'])
def shutdown():
    if not application.config['wizard']:
        shutdown_server()
        return render_template('default/shutdown.html')