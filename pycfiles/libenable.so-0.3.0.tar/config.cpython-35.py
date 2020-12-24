# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/bkvaluemeal/Iron Bank/libenable/libenable/blueprints/config.py
# Compiled at: 2017-01-05 17:07:32
# Size of source mod 2**32: 1189 bytes
"""
Configuration

This module defines the Flask blueprint for the application's configuration. See
the documentation for each object and their respective unit tests for more
information.
"""
from flask import Blueprint, redirect, render_template, request
import libenable
blueprint = Blueprint('config', __name__, template_folder='../templates')

@blueprint.route('/')
def show():
    """
        The configuration interface
        """
    return render_template('config.html', config=libenable.config)


@blueprint.route('/save', methods=['POST'])
def save():
    """
        Saves the configuration
        """
    libenable.config['DEFAULT']['host'] = request.form['host']
    libenable.config['DEFAULT']['port'] = request.form['port']
    libenable.config['DEFAULT']['path'] = request.form['path']
    libenable.config['ruCAPTCHA']['key'] = request.form['ruCAPTCHA_key']
    libenable.config['ruCAPTCHA']['currency'] = request.form['ruCAPTCHA_currency']
    libenable.config['d3cryp7']['url'] = request.form['d3cryp7_url']
    libenable.config['d3cryp7']['currency'] = request.form['d3cryp7_currency']
    with open(libenable.__conf__, 'w') as (configfile):
        libenable.config.write(configfile)
    return redirect('/')