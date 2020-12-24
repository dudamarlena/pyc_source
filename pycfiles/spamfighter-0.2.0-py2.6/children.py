# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/api/domain/children.py
# Compiled at: 2009-01-30 08:10:10
"""
Команда C{sf.domain.children} - получение списка имён поддоменов.
"""
import types
from zope.interface import implements
from spamfighter.core.commands import ICommand, install, DomainedCommand, Array

class DomainChildrenCommand(DomainedCommand):
    """
    Реализация команды C{sf.domain.children}.
    """
    implements(ICommand)
    commandName = 'sf.domain.children'
    commandSignature = {}
    resultSignature = {'children': {'type': Array(types.StringType), 'required': True}}
    install()

    def perform(self):

        def gotChildren(children):
            self.result.children = children.keys()

        return self.domain.children().addCallback(gotChildren)