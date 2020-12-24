# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\user\model.py
# Compiled at: 2020-03-21 07:22:44
# Size of source mod 2**32: 11272 bytes
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
db = SQLAlchemy()
Table = db.Table
Column = db.Column
Integer = db.Integer
Float = db.Float
Boolean = db.Boolean
String = db.String
Text = db.Text
Date = db.Date
Time = db.Time
DateTime = db.DateTime
Sequence = db.Sequence
Enum = db.Enum
UniqueConstraint = db.UniqueConstraint
ForeignKey = db.ForeignKey
relationship = db.relationship
backref = db.backref
object_mapper = db.object_mapper
Base = db.Model
DESCR_LEN = 512
INTEREST_LEN = 32
APPLICATION_LEN = 32
USERROLEDESCR_LEN = 512
ROLENAME_LEN = 32
EMAIL_LEN = 100
NAME_LEN = 256
PASSWORD_LEN = 255
UNIQUIFIER_LEN = 255
APP_CONTRACTS = 'contracts'
APP_MEMBERS = 'members'
APP_ROUTES = 'routes'
APP_SCORES = 'scores'
APP_ALL = [APP_CONTRACTS, APP_MEMBERS, APP_ROUTES, APP_SCORES]
userinterest_table = Table('users_interests', (Base.metadata), (Column('user_id', Integer, ForeignKey('user.id'))),
  (Column('interest_id', Integer, ForeignKey('interest.id'))),
  info={'bind_key': 'users'})
appinterest_table = Table('apps_interests', (Base.metadata), (Column('application_id', Integer, ForeignKey('application.id'))),
  (Column('interest_id', Integer, ForeignKey('interest.id'))),
  info={'bind_key': 'users'})
approle_table = Table('apps_roles', (Base.metadata), (Column('application_id', Integer, ForeignKey('application.id'))),
  (Column('role_id', Integer, ForeignKey('role.id'))),
  info={'bind_key': 'users'})

class Interest(Base):
    __tablename__ = 'interest'
    __bind_key__ = 'users'
    id = Column((Integer()), primary_key=True)
    interest = Column(String(INTEREST_LEN))
    users = relationship('User', secondary=userinterest_table,
      backref=(backref('interests')))
    applications = relationship('Application', secondary=appinterest_table,
      backref=(backref('interests')))
    description = Column(String(DESCR_LEN))
    public = Column(Boolean)
    version_id = Column(Integer, nullable=False, default=1)
    __mapper_args__ = {'version_id_col': version_id}


class Application(Base):
    __tablename__ = 'application'
    __bind_key__ = 'users'
    id = Column((Integer()), primary_key=True)
    application = Column(String(APPLICATION_LEN))
    version_id = Column(Integer, nullable=False, default=1)
    __mapper_args__ = {'version_id_col': version_id}


class RolesUsers(Base):
    __tablename__ = 'roles_users'
    __bind_key__ = 'users'
    id = Column((Integer()), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(Base, RoleMixin):
    __tablename__ = 'role'
    __bind_key__ = 'users'
    id = Column((Integer()), primary_key=True)
    name = Column((String(ROLENAME_LEN)), unique=True)
    description = Column(String(USERROLEDESCR_LEN))
    applications = relationship('Application', secondary=approle_table,
      backref=(backref('roles')))
    version_id = Column(Integer, nullable=False, default=1)
    __mapper_args__ = {'version_id_col': version_id}


class User(Base, UserMixin):
    __tablename__ = 'user'
    __bind_key__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column((String(EMAIL_LEN)), unique=True)
    password = Column(String(PASSWORD_LEN))
    name = Column(String(NAME_LEN))
    given_name = Column(String(NAME_LEN))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(UNIQUIFIER_LEN))
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users', backref=backref('users', lazy='dynamic'))
    version_id = Column(Integer, nullable=False, default=1)
    __mapper_args__ = {'version_id_col': version_id}


class ManageLocalTables:

    def __init__(self, db, appname, localusermodel, localinterestmodel, hasuserinterest=False):
        """
        operations on localuser model for callers of User model

        :param db: SQLAlchemy instance used by caller
        :param appname: name of application, must match Application.application
        :param localusermodel: model class for User, in the slave database (must have user_id column)
        :param localinterestmodel: model class for Interest, in the slave database
        :param hasuserinterest: (optional) if localusermodel has interest_id field, the users are copied for
                                           each interest used by appname, default False
        """
        self.db = db
        self.localusermodel = localusermodel
        self.localusertable = localusermodel.__table__.name
        self.hasuserinterest = hasuserinterest
        self.localinterestmodel = localinterestmodel
        self.localinteresttable = localinterestmodel.__table__.name
        self.application = Application.query.filter_by(application=appname).one()

    def _updateuser_byinterest(self):
        if not db.engine.has_table(self.localusertable):
            return
        alllocal = {}
        for localuser in self.localusermodel.query.all():
            alllocal[(localuser.user_id, localuser.interest_id)] = localuser

        for user in User.query.all():
            for interest in Interest.query.all():
                if self.application not in interest.applications:
                    pass
                else:
                    localinterest = self.localinterestmodel.query.filter_by(interest_id=(interest.id)).one()
                if (
                 user.id, localinterest.id) in alllocal:
                    localuser = alllocal.pop((user.id, localinterest.id))
                    localuser.active = user.active
                else:
                    newlocal = self.localusermodel(user_id=(user.id), interest_id=(localinterest.id), active=True)
                    self.db.session.add(newlocal)

        for user_id, interest_id in alllocal:
            localuser = self.localusermodel.query.filter_by(user_id=user_id, interest_id=interest_id).one()
            localuser.active = False

    def _updateuser_only(self):
        if not db.engine.has_table(self.localusertable):
            return
        alllocal = {}
        for localuser in self.localusermodel.query.all():
            alllocal[localuser.user_id] = localuser

        for user in User.query.all():
            if user.id in alllocal:
                localuser = alllocal.pop(user.id)
                localuser.active = user.active
            else:
                newlocal = self.localusermodel(user_id=(user.id), active=(user.active))
                self.db.session.add(newlocal)

        for user_id in alllocal:
            localuser = self.localusermodel.query.filter_by(user_id=user_id).one()
            localuser.active = False

    def _updateinterest(self):
        if not db.engine.has_table(self.localinteresttable):
            return
        alllocal = {}
        for localinterest in self.localinterestmodel.query.all():
            alllocal[localinterest.interest_id] = localinterest

        for interest in Interest.query.all():
            if self.application not in interest.applications:
                continue
            if interest.id in alllocal:
                discard = alllocal.pop(interest.id)
            else:
                newlocal = self.localinterestmodel(interest_id=(interest.id))
                self.db.session.add(newlocal)

        for interest_id in alllocal:
            localinterest = self.localinterestmodel.query.filter_by(interest_id=interest_id).one()
            self.db.session.delete(localinterest)

    def update(self):
        """
        keep localuser and localinterest tables consistent with external db User table
        """
        self._updateinterest()
        db.session.flush()
        if self.hasuserinterest:
            self._updateuser_byinterest()
        else:
            self._updateuser_only()
        self.db.session.commit()