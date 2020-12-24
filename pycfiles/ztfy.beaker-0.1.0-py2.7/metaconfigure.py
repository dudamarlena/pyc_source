# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/beaker/metaconfigure.py
# Compiled at: 2014-11-26 05:29:48
from ztfy.beaker.metadirectives import IBeakerSessionConfiguration
from zope.component.security import PublicPermission
from zope.component.zcml import utility
from ztfy.beaker.session import BeakerMemorySessionConfiguration, BeakerDBMSessionConfiguration, BeakerFileSessionConfiguration, BeakerMemcachedSessionConfiguration, BeakerAlchemySessionConfiguration

def memorySession(context, name='', **kwargs):
    """Beaker memory session configuration declaration"""
    config = BeakerMemorySessionConfiguration()
    for key, value in kwargs.iteritems():
        setattr(config, key, value)

    utility(context, IBeakerSessionConfiguration, config, permission=PublicPermission, name=name)


def dbmSession(context, name='', **kwargs):
    """Beaker DBM session configuration declaration"""
    config = BeakerDBMSessionConfiguration()
    for key, value in kwargs.iteritems():
        setattr(config, key, value)

    utility(context, IBeakerSessionConfiguration, config, permission=PublicPermission, name=name)


def fileSession(context, name='', **kwargs):
    """Beaker file session configuration declaration"""
    config = BeakerFileSessionConfiguration()
    for key, value in kwargs.iteritems():
        setattr(config, key, value)

    utility(context, IBeakerSessionConfiguration, config, permission=PublicPermission, name=name)


def memcachedSession(context, name='', **kwargs):
    """Beaker memcached session configuration declaration"""
    config = BeakerMemcachedSessionConfiguration()
    for key, value in kwargs.iteritems():
        setattr(config, key, value)

    utility(context, IBeakerSessionConfiguration, config, permission=PublicPermission, name=name)


def alchemySession(context, name='', **kwargs):
    """Beaker SQLAlchemy session configuration declaration"""
    config = BeakerAlchemySessionConfiguration()
    for key, value in kwargs.iteritems():
        setattr(config, key, value)

    utility(context, IBeakerSessionConfiguration, config, permission=PublicPermission, name=name)