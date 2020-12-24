# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/olek/Wszystkie_aggrescamy_swiata/aggrescan3d/a3d_gui/__init__.py
# Compiled at: 2018-11-20 10:51:24
import os, subprocess, sys
flask_loc = os.path.dirname(os.path.abspath(__file__))
try:
    from flask import Flask
    app = Flask(__name__)
    config = dict(PAGINATION=45, STATIC=os.path.join(flask_loc, 'static'), PICTURES=os.path.join(flask_loc, 'pictures'), USERJOB_DIRECTORY=os.path.join(flask_loc, 'computations'), DEBUG=True, SECRET_KEY='This_apps_super_secret_key')
    app.config.update(config)
    import viewsutils, views, db_manager, job_handling
    if not os.path.isfile(os.path.join(flask_loc, 'a3d_database.db')):
        db_manager.create_new_database(os.path.join(flask_loc, 'a3d_database.db'))
        print 'Database for your projects has been created.'
    app.config.update(dict(DATABASE=os.path.join(flask_loc, 'a3d_database.db')))
except ImportError:
    with open(os.path.join(flask_loc, 'requirements.txt'), 'r') as (f):
        print 'This program requires a few python packages to run: '
        for line in f:
            print line.strip()

        print 'Do you wish to use pip to install/upgrade those?'
    test = raw_input("Type 'y' or 'Y' if yes, else press enter to quit\n")
    if test == 'y' or test == 'Y':
        subprocess.Popen(['pip', 'install', '-r', os.path.join(flask_loc, 'requirements.txt')]).communicate()
    else:
        print 'The program has failed to start. Please contact us if you need further assistance.'
        sys.exit(0)
    print ''
    print 'The program attempted to install necessary packages. Re-run this script to run the app.'
    print "Note, the script will fail if you don't have pip installed. If that is the case please visit https://pip.pypa.io/en/stable/installing/ for instructions on how to install it."
    print ''