# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/api/domain/list.py
# Compiled at: 2009-01-30 08:10:10
"""
Команда C{sf.domain.list} - получение списка имён свойств домена.
"""
import types
from zope.interface import implements
from spamfighter.core.commands import ICommand, install, DomainedCommand, Array

class DomainListCommand(DomainedCommand):
    """
    Реализация команды C{sf.domain.list}.
    """
    implements(ICommand)
    commandName = 'sf.domain.list'
    commandSignature = {}
    resultSignature = {'properties': {'type': Array(types.StringType), 'required': True}}
    install()

    def perform(self):
        self.result.properties = self.domain.list()