# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jakob/Jest/Jalapeno/GUI/views/run.py
# Compiled at: 2017-03-17 12:07:13
# Size of source mod 2**32: 533 bytes
from flask import Blueprint, render_template, redirect, url_for, current_app as gui
from Jalapeno.Globalvar import events
run = Blueprint('run', __name__)

@run.route('/run', methods=['GET', 'POST'])
def runner():
    gui.config['carrier'](event=events['APP'])
    return redirect(url_for('home'))


@run.route('/run/stop', methods=['GET', 'POST'])
def stoper():
    gui.config['carrier'](kill='APP')
    return redirect(url_for('home'))


@run.route('/run/preview')
def runner_previewer():
    return "<iframe src='http://127.0.0.1:9999/'></iframe>"