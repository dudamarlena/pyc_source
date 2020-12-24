# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/core/models/WidgetsModel.py
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

class Widget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(256))
    url = db.Column(db.String(256))
    user = db.Column(db.Integer())
    name = db.Column(db.String(256))
    see_more = db.Column(db.String(256))
    param = db.Column(db.String())

    @property
    def is_active(self):
        return True

    def get_id_(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)