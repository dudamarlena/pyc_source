# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/api/message/input.py
# Compiled at: 2009-01-30 08:10:10
"""
Команда C{sf.message.input} - анализ входящего сообщения.
"""
import types
from zope.interface import implements
from spamfighter.core.commands import ICommand, install, DomainedCommand
from spamfighter.core.message import ITransitMessage

class MessageInputCommand(DomainedCommand):
    """
    Реализация команды C{sf.message.input}.
    """
    implements(ICommand)
    commandName = 'sf.message.input'
    commandSignature = {'message': {'type': ITransitMessage, 'required': True}, 'debug': {'type': types.BooleanType, 'required': False}}
    resultSignature = {'result': {'type': types.StringType, 'required': True}, 'log': {'type': types.StringType, 'required': False}}
    install()

    def perform(self):
        message = self.params.message.getMessage(self.domain)
        analyzer = self.domain.get('messageAnalyzer')

        def gotResult(result):
            self.result.result = result

        def logCallback(log):
            self.result.log = ('\n').join(log)

        return analyzer.analyze(message, self.domain, self.params.debug, logCallback).addCallback(gotResult)