# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\daversy\command\name.py
# Compiled at: 2016-01-14 15:12:15
from daversy.command import Command
from daversy.state import PROVIDERS

class Name(Command):
    __names__ = [
     'name', 'nm']
    __usage__ = ['Display the name of the given STATE.']
    __args__ = [
     'STATE']
    __options__ = []

    def execute(self, args, options):
        input = args[0]
        saved_state = None
        for provider in PROVIDERS:
            if provider.can_load(input):
                saved_state = provider.load(input, {})
                break

        if not saved_state:
            self.parser().error('STATE: could not open for reading')
        print saved_state.name
        return