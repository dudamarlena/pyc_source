# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/api/domain/get.py
# Compiled at: 2009-01-30 08:10:10
"""
Команда C{sf.domain.get} - получение информации об одном свойстве домена.
"""
import types
from zope.interface import implements, providedBy
from spamfighter.core.commands import ICommand, install, DomainedCommand, Array, errors
from spamfighter.core.domain import DomainKeyError

class DomainGetCommand(DomainedCommand):
    """
    Реализация команды C{sf.domain.get}.
    """
    implements(ICommand)
    commandName = 'sf.domain.get'
    commandSignature = {'name': {'type': types.StringType, 'required': True}}
    resultSignature = {'repr': {'type': types.StringType, 'required': True}, 'interfaces': {'type': Array(types.StringType), 'required': True}, 'classname': {'type': types.StringType, 'required': True}}
    install()

    def perform(self):
        try:
            value = self.domain.get(self.params.name)
        except DomainKeyError:
            raise errors.AttributeKeyException, self.params.name

        self.result.repr = str(value)
        self.result.classname = value.__class__.__name__
        self.result.interfaces = map(lambda iface: iface.__name__, providedBy(value))