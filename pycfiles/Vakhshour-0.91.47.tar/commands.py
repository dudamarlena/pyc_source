# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/Vakhshour/vakhshour/commands.py
# Compiled at: 2012-08-29 12:42:00
import json
from twisted.protocols.amp import Integer, String, Unicode, Command, CommandLocator, AMP
from base import VObject

class Json(String):
    """
    Json argument type.
    """

    def toString(self, inObject):
        return str(json.dumps(inObject))

    def fromString(self, inString):
        return json.loads(inString)


class Event(Command):
    arguments = [
     (
      'name', Unicode()),
     (
      'sender', String()),
     (
      'kwargs', Json())]
    response = [
     (
      'status', Integer())]