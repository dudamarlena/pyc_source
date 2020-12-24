# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./gthnk/models/entry.py
# Compiled at: 2017-11-21 20:58:03
# Size of source mod 2**32: 2269 bytes
import datetime
from flask_diamond.mixins.crud import CRUDMixin
from .. import db
import flask

class Entry(db.Model, CRUDMixin):
    __doc__ = '\n    An entry is an individual chunk of content in the Journal.\n    An entry has a day, hour, and minute.  Seconds is always 0.\n    '
    id = db.Column((db.Integer), primary_key=True)
    timestamp = db.Column((db.DateTime), nullable=False)
    content = db.Column(db.Unicode(4294967296))
    day_id = db.Column((db.Integer), (db.ForeignKey('day.id')), nullable=False)
    day = db.relationship('Day', backref=db.backref('entries', lazy='dynamic'))

    def save(self, _commit):
        if not self.day_id:
            from .day import Day
            this_date = datetime.date.fromordinal(self.timestamp.toordinal())
            this_day = Day.find(date=this_date)
            if not this_day:
                this_day = Day.create(date=this_date)
            self.day = this_day
        flask.current_app.logger.debug('saving')
        flask.current_app.logger.debug(self)
        obj = super(Entry, self).save(_commit)
        return obj

    def date_str(self):
        this_date = datetime.date.fromordinal(self.timestamp.toordinal())
        return datetime.datetime.strftime(this_date, '%Y-%m-%d')

    def hhmm(self):
        return datetime.datetime.strftime(self.timestamp, '%H%M')

    def __repr__(self):
        return '<Entry {}>'.format(self.timestamp)

    def __unicode__(self):
        return '\n\n{}\n\n{}'.format(datetime.datetime.strftime(self.timestamp, '%H%M'), self.content)

    def __str__(self):
        return self.__unicode__()