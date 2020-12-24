# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/investigator/app/main/controller/default.py
# Compiled at: 2019-11-07 12:26:02
# Size of source mod 2**32: 1047 bytes
from flask import render_template, session
from ..main import application
from .helper import shutdown_server, load_available_pipes

@application.route('/')
def index():
    available_pipes = load_available_pipes()
    return render_template('default/index.html', available_pipes=available_pipes)


@application.route('/investigator_error')
@application.errorhandler(500)
@application.errorhandler(404)
@application.errorhandler(502)
def investigator_error(e):
    error_key = 'error_msg'
    success = 'Ooopsi, an error occured'
    if e.code == 404:
        success = '...could not find that page.'
    else:
        if e.code == 502:
            success = 'Probaly MongoDB has some problems. Give it a moment.'
        else:
            if error_key in session:
                success = session[error_key]
    session[error_key] = ''
    return render_template('error_page.html', error_msg=success)


@application.route('/shutdown', methods=['GET'])
def shutdown():
    if not application.config['wizard']:
        shutdown_server()
    return render_template('default/shutdown.html')