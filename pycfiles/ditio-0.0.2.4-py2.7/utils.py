# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditio/utils.py
# Compiled at: 2018-01-30 11:19:12


def apply_commands(context, executor, commands, cell):
    for cmd, params in commands:
        cell = executor(context, cell, cmd, params)

    return cell


def commands_update(commands, k, v):
    for index, entry in enumerate(commands):
        cmd, params = entry
        if cmd == k:
            commands[index] = (
             k, v)
            return

    commands.append((k, v))