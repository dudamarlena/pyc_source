# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\parsers\sof2pm.py
# Compiled at: 2016-03-08 18:42:10
from b3.parsers.sof2 import Sof2Parser
from b3.functions import prefixText
__author__ = 'xlr8or, ~cGs*Pr3z, ~cGs*AQUARIUS'
__version__ = '1.3'

class Sof2PmParser(Sof2Parser):
    gameName = 'sof2pm'
    privateMsg = True
    _commands = {'ban': 'addip %(cid)s', 
       'kick': 'clientkick %(cid)s', 
       'message': 'tell %(cid)s %(message)s', 
       'say': 'say %(message)s', 
       'set': 'set %(name)s "%(value)s"', 
       'tempban': 'clientkick %(cid)s'}

    def message(self, client, text):
        """
        Send a private message to a client.
        :param client: The client to who send the message.
        :param text: The message to be sent.
        """
        if client is None:
            self.say(text)
            return
        else:
            if client.cid is None:
                return
            lines = []
            message = prefixText([self.msgPrefix, self.pmPrefix], text)
            message = message.strip()
            for line in self.getWrap(message):
                lines.append(self.getCommand('message', cid=client.cid, message=line))

            self.writelines(lines)
            return