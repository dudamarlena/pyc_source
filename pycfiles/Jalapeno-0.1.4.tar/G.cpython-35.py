# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jakob/Jest/Jalapeno/GUI/G.py
# Compiled at: 2017-03-19 13:09:49
# Size of source mod 2**32: 2272 bytes
from flask import Flask, render_template, url_for, redirect
import os, Jalapeno.core, Jalapeno.lib
from Jalapeno.path import APP_DIR
from Jalapeno.Globalvar import *
from multiprocessing import Process
from Jalapeno.Globalvar import events, Event
import os
from sys import exit
gui = Flask('GUI')
GUI_DIR = APP_DIR + os.sep + 'Jalapeno' + os.sep + 'GUI'
gui.template_folder = GUI_DIR + os.sep + 'templates'
gui.static_folder = GUI_DIR + os.sep + 'static'
import Jalapeno.GUI.Gutils.gtheme
from Jalapeno.GUI.views import welcome, sites, run, touch
gui.register_blueprint(welcome.welcome)
gui.register_blueprint(sites.sites)
gui.register_blueprint(run.run)
gui.register_blueprint(touch.touch)

def gui_starter(listener):
    gui.config['carrier'] = listener
    gui.run(port=5588)


events['GUI'] = Event('GUI', 'Proc', gui_starter)

@gui.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@gui.route('/freeze', methods=['GET', 'POST'])
def freeze():
    gui.config['carrier'](event=events['FREEZE'])
    return redirect(url_for('home'))


@gui.route('/shortcut')
def shortcut():
    Jalapeno.lib.shortcuts.create_shortcuts()
    return redirect(url_for('home'))


@gui.route('/help')
def help_session():
    return render_template('welcome.html')


@gui.route('/exit', methods=['GET', 'POST'])
def exit_proc():
    try:
        return 'Goodbye'
    finally:
        gui.config['carrier'](command='Stop')


@gui.route('/bye', methods=['GET', 'POST'])
def exitsbye():
    return render_template('bye.html')


@gui.route('/version')
def ver():
    return '0.1.3'


@gui.route('/redirect')
def redir():
    return render_template('redirect.html')