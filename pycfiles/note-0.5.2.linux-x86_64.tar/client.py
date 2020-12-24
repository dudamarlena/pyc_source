# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/note/client.py
# Compiled at: 2014-12-20 09:55:02
import zmq, json

class Note_Client(object):
    """ This is the client side library to interact with the note server """

    def __init__(self):
        """
        Initialize the client, mostly ZMQ setup
        """
        self.server_addr = '127.0.0.1'
        self.server_port = 5500
        self.server_uri = 'tcp://'
        self.server_uri = self.server_uri + self.server_addr
        self.server_uri = self.server_uri + ':'
        self.server_uri = self.server_uri + str(self.server_port)
        self.poll_timeout = 1000
        self.context = zmq.Context.instance()
        self.sock = self.context.socket(zmq.REQ)
        self.sock.connect(self.server_uri)

    def Send(self, msg):
        """
        Add a note to the database on the server
        :param msg: The text of the note.
        :type msg: str
        :param tags: A list of tags to associate with the note.
        :type tags: list
        :returns: The message from the server
        :rtype: str
        """
        if 'type' not in msg:
            return
        self.sock.send(json.dumps(msg))
        msg = self.sock.recv()
        return msg

    def Encrypt(self):
        """

        """
        pass