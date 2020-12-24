# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_controlpanel/kotti_controlpanel/resources.py
# Compiled at: 2017-06-09 03:03:53
"""
Created on 2016-06-15
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
import json
from kotti import Base
from kotti.interfaces import IDefaultWorkflow
from kotti.resources import Content
from sqlalchemy import Column, String, Unicode, Integer, ForeignKey
from sqlalchemy.types import PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from zope.interface import implements
from kotti_controlpanel import _

class ControlPanel(Base):
    tablename = 'controlpanels'

    @declared_attr
    def __tablename__(cls):
        return cls.tablename

    id = Column(Unicode(100), primary_key=True, nullable=False)
    settings = Column(PickleType)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()

    def set_settings(self, settings):
        self.settings = settings

    def get_settings(self):
        return self.settings


class ModuleSettings(object):
    """Object to hold informations about the settings of
       the calling module.
    """

    def __init__(self, **kwargs):
        self.module = None
        self.name = None
        self.title = None
        self.icon = 'kotti_controlpanel:static/gears.png'
        self.description = None
        self.success_message = ''
        self.settings = []
        self.schema_factory = None
        self.settings_objs = []
        self.template = None
        self.bind = {}
        self.__dict__.update(kwargs)
        return


class SettingObj(object):
    """One setting in a module. Here we are also set the defaults
       for one setting.
    """

    def __init__(self, **kwargs):
        self.module = None
        self.type = 'String'
        self.name = None
        self.icon = 'kotti_controlpanel:static/gears.png'
        self.title = None
        self.description = ''
        self.default = ''
        self.bind = {}
        self.__dict__.update(kwargs)
        return

    @property
    def field_name(self):
        """Return a name that is somewhat unique.
        """
        return '%s-%s' % (self.module, self.name)