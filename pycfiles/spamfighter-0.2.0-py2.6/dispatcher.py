# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/core/commands/dispatcher.py
# Compiled at: 2009-01-30 08:10:10
"""
Диспетчеризация команд по имени.

Т.е. отображаем имя команды (атрибут comandName из интерфейса L{spamfighter.core.commands.ICommand}) в
класс команды.
"""
from spamfighter.utils.registrator import registrator
from spamfighter.core.commands import errors
dispatch_map = {}

@registrator
def install(command_class):
    u"""Вариант функции L{installCommand} которую можно использовать в определении класса

    Пример использования::
        from spamfighter.core.commands import install, Command
        class MyCommand(Command):
            install()
    """
    installCommand(command_class)


def installCommand(command_class):
    u"""Установить новую команду в карту диспетчеризации.

    @param command_class: класс, производный от L{Command}
    """
    name = command_class.commandName
    assert name not in dispatch_map
    dispatch_map[name] = command_class


def deinstallCommand(command_class):
    u"""
    Убрать команду из карты диспетчеризации.

    @param command_class: класс, производный от L{Command}
    """
    name = command_class.commandName
    assert name in dispatch_map
    del dispatch_map[name]


def dispatchCommand(commandName):
    u"""
    Найти класс команды, соответствующий данной команде по имени

    @param commandName: имя команды
    @type commandName: C{str}
    @raise errors.CommandUnknownException: если такой команды не существует
    @rtype: производная от L{Command}
    """
    if commandName not in dispatch_map:
        raise errors.CommandUnknownException, commandName
    return dispatch_map[commandName]()


def listAllCommands():
    u"""
    Вернуть список всех команд.
    """
    return dispatch_map.keys()