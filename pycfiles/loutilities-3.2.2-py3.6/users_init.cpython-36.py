# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\user\scripts\users_init.py
# Compiled at: 2020-03-14 15:36:52
# Size of source mod 2**32: 4641 bytes
"""
users_init - command line database initialization - clean database initialize users
=========================================================================================
run from 3 levels up, like python -m loutilities.user.scripts.users_init

"""
from os.path import join, dirname
from copy import deepcopy
from loutilities.transform import Transform
from loutilities.user import create_app
from loutilities.user.settings import Development
from loutilities.user.model import db
from loutilities.user.applogging import setlogging
from loutilities.user.model import User, Role, Interest, Application
from loutilities.user.model import APP_ALL
from loutilities.user.roles import all_roles

class parameterError(Exception):
    pass


def init_db(defineowner=True):
    from loutilities.user import user_datastore
    from flask_security import hash_password
    interests = [
     {'interest':'fsrc', 
      'description':'Frederick Steeplechasers Running Club',  'public':True}]
    allapps = []
    appname2db = {}
    for app in APP_ALL:
        thisapp = Application(application=app)
        db.session.add(thisapp)
        db.session.flush()
        allapps.append(thisapp)
        appname2db[app] = thisapp

    combinedroles = {}
    local_all_roles = deepcopy(all_roles)
    for approles in local_all_roles:
        for approle in approles:
            apps = approle.pop('apps')
            rolename = approle['name']
            thisrole = Role.query.filter_by(name=rolename).one_or_none() or (user_datastore.create_role)(**approle)
            for thisapp in apps:
                thisrole.applications.append(appname2db[thisapp])

            combinedroles[rolename] = thisrole

    allinterests = []
    for interest in interests:
        thisinterest = Interest(**interest)
        for thisapp in allapps:
            thisinterest.applications.append(thisapp)

        db.session.flush()
        allinterests.append(thisinterest)

    if defineowner:
        from flask import current_app
        rootuser = current_app.config['APP_OWNER']
        rootpw = current_app.config['APP_OWNER_PW']
        name = current_app.config['APP_OWNER_NAME']
        given_name = current_app.config['APP_OWNER_GIVEN_NAME']
        owner = User.query.filter_by(email=rootuser).first()
        if not owner:
            owner = user_datastore.create_user(email=rootuser, password=(hash_password(rootpw)), name=name, given_name=given_name)
            for rolename in combinedroles:
                user_datastore.add_role_to_user(owner, combinedroles[rolename])

        db.session.flush()
        owner = User.query.filter_by(email=rootuser).one()
        if not owner.interests:
            for thisinterest in allinterests:
                owner.interests.append(thisinterest)

    db.session.commit()


scriptdir = dirname(__file__)
scriptfolder = dirname(scriptdir)
configdir = join(scriptfolder, 'config')
configfile = 'users.cfg'
configpath = join(configdir, configfile)
app = create_app(Development(configpath), configpath)
db.init_app(app)
with app.app_context():
    setlogging()
    db.drop_all(bind='users')
    db.create_all(bind='users')
    init_db()
    db.session.commit()