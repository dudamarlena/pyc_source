# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/api/model/classify.py
# Compiled at: 2009-01-30 08:10:10
"""
Команда C{sf.model.classify} - классификация по модели.
"""
import types
from zope.interface import implements
from spamfighter.core.commands import ICommand, install, errors
from spamfighter.core.model.command import ModelBaseCommand

class ModelClassifyCommand(ModelBaseCommand):
    """
    Реализация команды C{sf.model.classify}.
    """
    implements(ICommand)
    commandName = 'sf.model.classify'
    commandSignature = {}
    resultSignature = {'marker': {'type': types.StringType, 'required': True}}
    install()

    def perform(self):

        def gotResult(result):
            if result:
                self.result.marker = 'good'
            else:
                self.result.marker = 'bad'

        return self.model.classify(self.text).addCallback(gotResult)