# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/erwhann/Sources/Projets/sebureem/sebureem/setup_app.py
# Compiled at: 2017-04-13 05:57:09
# Size of source mod 2**32: 3500 bytes
"""Sebureem Setup webinstaller
"""
import os, bcrypt
from pathlib import Path
from configparser import ConfigParser
from flask import Blueprint, render_template, flash, request
from peewee import SqliteDatabase
from sebureem import db, config
from sebureem.models import Sebura, Sebuks
__all__ = [
 'setup_app']
setup_app = Blueprint('setup_app', __name__, url_prefix='/install',
  template_folder='templates')

def config_dir():
    if os.name == 'posix':
        config_path = Path(os.path.expandvars('$XDG_CONFIG_HOME/sebureem'))
    else:
        if os.name == 'nt':
            config_path = Path(os.path.expandvars('%LOCALAPPDATA%/sebureem'))
    return config_path


@setup_app.route('/')
def index():
    return render_template('setup/index.html')


@setup_app.route('/config/')
def create_config():
    try:
        config_path = config_dir()
        config_path.mkdir(mode=493, parents=True)
        config_file = config_path / 'sebureem.ini'
        print(str(config_file))
        with open(str(config_file), 'w') as (f):
            f.write('# Sebureem config file')
        flash('Success: Config file created', 'success')
    except FileExistsError:
        flash('Warning: Config file found', 'error')
        return render_template('setup/config.html', config_path=(config_path / 'sebureem.ini'),
          override_form=True)
    else:
        return render_template('setup/config.html', config_path=config_file,
          override_form=False)


@setup_app.route('/database/', methods=['GET', 'POST'])
def create_db():
    if request.method == 'GET':
        if os.name == 'posix':
            db_default_path = os.path.expandvars('$XDG_DATA_HOME/sebureem')
        else:
            if os.name == 'nt':
                db_default_path = os.path.expandvars('%LOCALAPPDATA%\\sebureem')
        return render_template('setup/database.html', database_path=db_default_path,
          created=False)
    if request.method == 'POST':
        db_path = Path(request.form['db_path'])
        db_path = db_path / request.form['db_name']
        db.init(str(db_path))
        db.connect()
        db.create_tables([Sebura, Sebuks])
        db.close()
        config['DATABASE'] = {'path': db_path}
        config_path = config_dir()
        config_file = config_path / 'sebureem.ini'
        with open(str(config_file), 'w') as (conf):
            config.write(conf)
        flash('Success: Database created', 'success')
        return render_template('setup/database.html', database_path=(str(db_path)),
          created=True)


@setup_app.route('/admin/', methods=['GET', 'POST'])
def create_admin():
    if request.method == 'GET':
        return render_template('setup/admin.html', created=False)
    if request.method == 'POST':
        admin_login = request.form['admin_login']
        admin_passwd = bcrypt.hashpw(bytes(request.form['admin_passwd'], 'utf-8'), bcrypt.gensalt())
        config['ADMIN'] = {'admin_login':admin_login, 
         'admin_passwd':admin_passwd.decode()}
        config_path = config_dir()
        config_file = config_path / 'sebureem.ini'
        with open(str(config_file), 'w') as (conf):
            config.write(conf)
        flash('Success: Admin account created', 'success')
        return render_template('setup/admin.html', created=True)


@setup_app.route('/site/')
def create_site():
    return render_template('setup/site.html')