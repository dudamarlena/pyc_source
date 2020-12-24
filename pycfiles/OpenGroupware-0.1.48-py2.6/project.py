# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/alchemy/project.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy.orm import relation, backref, object_session
from sqlalchemy import *
from base import Base, KVC
from sqlalchemy.ext.associationproxy import association_proxy

class ProjectInfo(Base, KVC):
    """ An OpenGroupware ProjectInfo object """
    __tablename__ = 'project_info'
    __entityName__ = 'ProjectInfo'
    __internalName__ = 'ProjectInfo'
    object_id = Column('project_info_id', Integer, Sequence('key_generator'), primary_key=True)
    project_id = Column('project_id', ForeignKey('project.project_id'))
    comment = Column('comment', String)
    status = Column('db_status', String(50))

    def __init__(self):
        self.status = 'inserted'

    def __repr__(self):
        return ('<ProjectInfo objectId={0} projectId={1}/>').format(self.object_id, self.project_id)

    project = relation('Project', uselist=False, backref=backref('project', cascade='all, delete-orphan'), primaryjoin='ProjectInfo.project_id==Project.object_id')


class Project(Base, KVC):
    """ An OpenGroupware Project object """
    __tablename__ = 'project'
    __entityName__ = 'Project'
    __internalName__ = 'Project'
    object_id = Column('project_id', Sequence('key_generator'), ForeignKey('doc.project_id'), ForeignKey('project_info.project_id'), ForeignKey('note.project_id'), primary_key=True)
    version = Column('object_version', Integer)
    owner_id = Column('owner_id', Integer, ForeignKey('person.company_id'), nullable=False)
    status = Column('db_status', String(50))
    sky_url = Column('url', String(100))
    end = Column('end_date', DateTime())
    kind = Column('kind', String(50))
    name = Column('name', String(255))
    number = Column('number', String(100))
    is_fake = Column('is_fake', Integer)
    parent_id = Column('parent_project_id', Integer)
    start = Column('start_date', DateTime())

    def __init__(self):
        self.status = 'inserted'
        self.version = 0
        self._info = ProjectInfo()

    def get_display_name(self):
        return self.number

    def __repr__(self):
        return ('<Project objectId={0} version={1} name="{2}" number="{3}" kind="{4}" url="{5}" fake={6} owner={7} start="{8}" end="{8}">').format(self.object_id, self.version, self.name, self.number, self.kind, self.sky_url, self.is_fake, self.owner_id, self.start.strftime('%Y%m%dT%H:%M'), self.end.strftime('%Y%m%dT%H:%M'))

    _info = relation('ProjectInfo', uselist=False, backref=backref('project_info'), primaryjoin='ProjectInfo.project_id==Project.object_id')
    comment = association_proxy('_info', 'comment')