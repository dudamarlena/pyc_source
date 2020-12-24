# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/flask_boot/project/manage.py
# Compiled at: 2018-09-06 05:56:50
from application.server import app
from flask_script import Manager
from application.model import ModelBase, engines
manager = Manager(app)

@manager.command
def create():
    ModelBase.metadata.create_all(engines['master'])


if __name__ == '__main__':
    manager.run()