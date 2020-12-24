# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Whiteboard/CommandConsole.py
# Compiled at: 2008-10-19 12:19:52
from Kamaelia.Util.Marshalling import Marshaller
from Kamaelia.Util.Console import ConsoleReader
from Kamaelia.Visualisation.PhysicsGraph.lines_to_tokenlists import lines_to_tokenlists as text_to_tokenlists
from Kamaelia.Chassis.Pipeline import Pipeline

class CommandParser:

    def marshall(data):
        output = [
         data]
        if data[0].upper() == 'LOAD':
            output.append(['GETIMG'])
        return output

    marshall = staticmethod(marshall)


def parseCommands():
    return Marshaller(CommandParser)


def CommandConsole():
    return Pipeline(ConsoleReader(), text_to_tokenlists(), parseCommands())