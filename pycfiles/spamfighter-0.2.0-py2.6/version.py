# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/api/info/version.py
# Compiled at: 2009-01-30 08:10:10
"""
Команда C{sf.info.version} - получение версии сервера
"""
import types
from zope.interface import implements
from spamfighter.core.commands import ICommand, install, Command
from spamfighter import version

class InfoVersionCommand(Command):
    """
    Реализация команды C{sf.info.version}.
    """
    implements(ICommand)
    commandName = 'sf.info.version'
    commandSignature = {}
    resultSignature = {'version': {'type': types.StringType, 'required': True}}
    install()

    def perform(self):
        self.result.version = version