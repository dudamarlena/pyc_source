# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/senex/models.py
# Compiled at: 2016-04-28 16:51:07
import json, datetime, os
from .utils import get_server, get_dependencies
from pyramid.security import Allow, Everyone
from sqlalchemy import Column, Integer, Text, Boolean, UnicodeText, Unicode, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
DEFAULT_ENV_DIR = 'env-old'
DEFAULT_APPS_DIR = 'oldapps'
DEFAULT_SSL_DIR = 'sslcert'
DEFAULT_VH_PATH = '/etc/apache2/sites-available/olds'

def get_default_dependency_state():
    return unicode(json.dumps(get_dependencies({'env_dir': DEFAULT_ENV_DIR})))


def get_default_server_state():
    return unicode(json.dumps(get_server()))


class OLD(Base):
    """The model for holding OLD instances.

    """
    __tablename__ = 'olds'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    human_name = Column(Text)
    running = Column(Boolean)


class SenexState(Base):
    """The model for holding Senex's state. These values can be determined on
    each request but that seems inefficient so we only refresh these values if
    the user requests a forced refresh or if a threshold time interval has
    passed.

    Note: to keep track of the history of the state, a new state model should
    be created upon each change. That is, an existing state should never be
    modified.

    """
    __tablename__ = 'senexstate'
    id = Column(Integer, primary_key=True)
    installation_in_progress = Column(Boolean, default=False)
    old_change_in_progress = Column(Boolean, default=False)
    server_state = Column(UnicodeText, default=get_default_server_state)
    dependency_state = Column(UnicodeText, default=get_default_dependency_state)
    last_state_check = Column(DateTime, default=datetime.datetime.utcnow)
    mysql_user = Column(Unicode(255))
    mysql_pwd = Column(Unicode(255))
    user_dir = os.path.expanduser('~')
    env_dir = Column(Unicode(255), default=DEFAULT_ENV_DIR)
    default_apps_path = os.path.join(user_dir, DEFAULT_APPS_DIR)
    apps_path = Column(Unicode(255), default=default_apps_path)
    host = Column(Unicode(255))
    vh_path = Column(Unicode(255), default=DEFAULT_VH_PATH)
    default_ssl_path = os.path.join(user_dir, DEFAULT_SSL_DIR)
    default_ssl_cert_path = os.path.join(default_ssl_path, 'olds.crt')
    ssl_crt_path = Column(Unicode(255), default=default_ssl_cert_path)
    default_ssl_key_path = os.path.join(default_ssl_path, 'olds.key')
    ssl_key_path = Column(Unicode(255), default=default_ssl_key_path)
    default_ssl_pem_path = os.path.join(default_ssl_path, 'olds.pem')
    ssl_pem_path = Column(Unicode(255), default=default_ssl_pem_path)
    settings_attrs = [
     'mysql_user',
     'mysql_pwd',
     'env_dir',
     'apps_path',
     'host',
     'vh_path',
     'ssl_crt_path',
     'ssl_key_path',
     'ssl_pem_path']

    def get_settings(self):
        return dict([ (attr, getattr(self, attr)) for attr in self.settings_attrs ])


class RootFactory(object):
    """This facilitates Pyramid's own authentication/authorization system. I
    don't fully understand it yet.

    """
    __acl__ = [
     (
      Allow, Everyone, 'view'),
     (
      Allow, 'group:editors', 'edit')]

    def __init__(self, request):
        pass