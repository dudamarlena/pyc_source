# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/esalazar/git/teleceptor/teleceptor/models.py
# Compiled at: 2014-09-09 22:53:58
"""
Contributing Authors:
    Bretton Murphy (Visgence, Inc.)
    Victor Szczepanski (Visgence, Inc)
    Jessica Greenling (Visgence, Inc)

Models contains what information will be stored in the database for each component of the project (such as the necessary attributes to be stored for a sensor).  Not all classes will have a toDict()/to_dict() function.

This module cannot be run independently as it just describes the structure of the database.

Dependencies:

external libraries:
    sqlalchemy
    json

    (c) 2014 Visgence, Inc.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""
from sqlalchemy import Column, Integer, Text, Boolean, BigInteger, ForeignKey, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, synonym
try:
    import simplejson as json
except ImportError:
    import json

Base = declarative_base()

class User(Base):
    """
    Information that identifies the user.  Currently unused.

    id : int
    email : str
    firstname : str
    lastname : str
    active : bool
    password : str
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(Text, nullable=False)
    firstname = Column(Text, nullable=False)
    lastname = Column(Text, nullable=False)
    active = Column(Boolean, default=True)
    password = Column(Text, nullable=False)

    def __repr__(self):
        return self.firstname + ' ' + self.lastname


class Session(Base):
    """
        Currently unused.
    """
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True)
    key = Column(Text, unique=True, nullable=False)
    expiration = Column(BigInteger)
    user = Column(Integer, ForeignKey('user.id'))


class SensorReading(Base):
    """
    id : int
        Uniquely identifies the SensorReading.
    datastream : int
        Used to identify a SensorReading to a DataStream.
    sensor : str
        Used to identify a SensorReading to a Sensor.
    value : float
        The value read from the sensor.
    timestamp : BigInt
        The time that the reading was taken.
    """
    __tablename__ = 'sensorreading'
    id = Column(Integer, primary_key=True)
    datastream = Column(Integer, ForeignKey('datastream.id'), index=True)
    sensor = Column(Text, ForeignKey('sensor.uuid'), index=True)
    value = Column(Float)
    timestamp = Column(BigInteger, index=True)

    def toDict(self):
        return {'id': self.id, 
           'datastream': self.datastream, 
           'sensor': self.sensor, 
           'value': self.value, 
           'timestamp': self.timestamp}


class MessageQueue(Base):
    """
    Each sensor will have it's own unique message queue with its own identification number. The message queue can contain many messages.  Message handling can be found in messages.

    id : int
        Uniquely identifies the MessageQueue.
    messages : list of Message
        Can be an empty list or have many elements. Used to store pending messages for sensor.
    sensor_id : str
        Used to identify a MessageQueue to a Sensor.
    """
    __tablename__ = 'messagequeue'
    id = Column(Integer, primary_key=True)
    messages = relationship('Message', order_by='Message.id', backref='messagequeue', lazy='dynamic', uselist=True)
    sensor_id = Column(Text)

    def to_dict(self):
        data = {'id': self.id, 
           'sensor_id': self.sensor_id}
        if self.messages is not None:
            try:
                data['messages'] = [ m.to_dict() for m in self.messages ]
            except TypeError:
                data['messages'] = self.messages.to_dict()

        return data


class Message(Base):
    """
    A message contains instructions for the sensor.

    id : int
        Uniquely identifies a Message.
    message : str
        Instructions for the sensor to perform some action that corresponds with the sensors capabilities.
    message_queue_id : int
        Used to identify a Message to a MessageQueue.
    timeout : float
        The expiration time for a Message. Old messages should not be used by the sensor.
    read : bool
        Indicates whether the Message as been sent to the basestation or read/acknowledged in some other way.
    """
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    message = Column(Text)
    message_queue_id = Column(Integer, ForeignKey('messagequeue.id'))
    timeout = Column(Float, default=30000.0)
    read = Column(Boolean, default=False)

    def to_dict(self):
        data = {'id': self.id, 
           'message': json.loads(self.message), 
           'timeout': self.timeout, 
           'read': self.read}
        return data


class Sensor(Base):
    """
    uuid : str
        Unique identifier of this sensor.
    sensor_IOtype : bool
        True indicates that the sensor takes input.  False indicates that the sensor is only for output.
    sensor_type : str
        Indicates the type of sensor.  Used in conjunction with message to check that the message is valid for this type of sensor.
    name : str
        User-friendly (human-readable) name.
    units : str
        Identifies the type of data gathered from the sensor.
    model : str
        Identifies the model of the sensor.
    description : str
        Some information that describes the sensor. Meant for the user's purposes.
    last_calibration_id : int
        Used to identify a Sensor to a Calibration.
    last_calibration : Calibration
        Has the current calibration data for the sensor.
    message_queue: MessageQueue
        Message queue that contains message for the sensor.
    _meta_data : str
        Any extra information about the sensor.
    """
    __tablename__ = 'sensor'
    uuid = Column(Text, primary_key=True)
    sensor_IOtype = Column(Boolean)
    sensor_type = Column(Text, default='')
    last_value = Column(Text, default='')
    name = Column(Text)
    units = Column(String(32))
    model = Column(Text)
    description = Column(Text)
    last_calibration_id = Column(Integer, ForeignKey('calibration.id'))
    last_calibration = relationship('Calibration')
    message_queue_id = Column(Integer, ForeignKey('messagequeue.id'))
    message_queue = relationship('MessageQueue')
    _meta_data = Column('meta_data', Text)

    def toDict(self):
        print 'todict sensor'
        data = {'uuid': self.uuid, 
           'sensor_type': self.sensor_type, 
           'units': self.units, 
           'description': self.description, 
           'name': self.name, 
           'model': self.model, 
           'last_value': self.last_value, 
           'sensor_IOtype': self.sensor_IOtype, 
           'meta_data': self.meta_data}
        if self.last_calibration is not None:
            data['last_calibration'] = self.last_calibration.toDict()
        return data

    @property
    def meta_data(self):
        if self._meta_data == '' or self._meta_data is None:
            return {}
        return json.loads(self._meta_data)

    @meta_data.setter
    def meta_data(self, data):
        if data == '' or data is None:
            data = {}
        self._meta_data = json.dumps(data)
        return

    meta_data = synonym('_meta_data', descriptor=meta_data)


class DataStream(Base):
    """
    id : int
        Unique identifier of this DataStream.
    sensor : str
        Used to identify a DataStream to a Sensor.
    owner : int
        Identifies the user for the datastream.  Currently unused.
    min_value : float
    max_value : float
    name : str
        User-friendly (human-readable) name.  Currently unused.
    description : str
        Some information that describes the datastream.  Currently unused.
    """
    __tablename__ = 'datastream'
    id = Column(Integer, primary_key=True)
    sensor = Column(Text, ForeignKey('sensor.uuid'), unique=True, index=True)
    owner = Column(Integer, ForeignKey('user.id'))
    min_value = Column(Float)
    max_value = Column(Float)
    name = Column(Text)
    description = Column(Text)

    def toDict(self):
        return {'id': self.id, 
           'min_value': self.min_value, 
           'max_value': self.max_value, 
           'name': self.name, 
           'description': self.description, 
           'owner': self.owner, 
           'sensor': self.sensor}


class Calibration(Base):
    """
    id : int
        Unique identifier of this Calibration.
    sensor_id : str
        Used to identify a Calibration to a Sensor.
    timestamp : BigInt
        Indentifies the time in miliseconds when the calibration was stored.
    user : str
        Currently unused.
    coefficients: str
        Describes the coefficients of a polynomial function to a apply to the readings.  Order of coefficients is in decreasing polynomial degree (e.g. [1, 0] represents the polynomial 1*x + 0)
    """
    __tablename__ = 'calibration'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Text)
    timestamp = Column(BigInteger)
    user = Column(Text)
    coefficients = Column(Text, nullable=False)

    def toDict(self):
        print 'calibration toDict'
        print self.coefficients
        return {'id': self.id, 
           'sensor_id': self.sensor_id, 
           'timestamp': self.timestamp, 
           'user': self.user, 
           'coefficients': json.loads(self.coefficients)}