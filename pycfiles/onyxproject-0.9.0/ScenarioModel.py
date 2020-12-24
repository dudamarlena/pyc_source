# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/core/models/ScenarioModel.py
# Compiled at: 2017-03-29 12:18:51
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.extensions import db

class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    template = db.Column(db.String(256))
    active = db.Column(db.Integer())
    event = db.Column(db.String(256))
    action = db.Column(db.String(256))
    action_param = db.Column(db.String(256))
    user = db.Column(db.Integer())

    @property
    def is_active(self):
        return True

    def get_id_(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)