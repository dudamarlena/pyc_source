# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/api/model/train.py
# Compiled at: 2009-01-30 08:10:10
"""
Команда C{sf.model.train} - обучение модели.
"""
import types
from zope.interface import implements
from spamfighter.core.commands import ICommand, install, errors
from spamfighter.core.model.command import ModelBaseCommand

class ModelTrainCommand(ModelBaseCommand):
    """
    Реализация команды C{sf.model.train}.
    """
    implements(ICommand)
    commandName = 'sf.model.train'
    commandSignature = {'marker': {'type': types.StringType, 'required': True}}
    resultSignature = {}
    install()

    def perform(self):
        if self.params.marker not in ('good', 'bad'):
            raise errors.TypeParameterException, 'marker'
        return self.model.train(self.text, self.params.marker == 'good')