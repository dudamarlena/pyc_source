# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/core/models/CalendarModel.py
# Compiled at: 2017-05-04 11:06:35
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from onyx.extensions import db

class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idAccount = db.Column(db.String(64))
    title = db.Column(db.String(64))
    lieu = db.Column(db.String(255))
    notes = db.Column(db.String(255))
    start = db.Column(db.String(64))
    end = db.Column(db.String(64))
    color = db.Column(db.String(64))
    allday = db.Column(db.String(64))

    @property
    def is_active(self):
        return True

    def get_id_(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)