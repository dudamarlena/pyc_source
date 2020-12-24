# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/core/websockets/handlers.py
# Compiled at: 2014-05-08 12:01:23
import uuid, tornado.websocket

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """
    simple websocket server for bidirectional communication between client and server
    """
    channels = {'public': {}, 'private': {}}

    def send_message(self, *args):
        """ alias to write_message """
        self.write_message(*args)

    def add_client(self, user_id=None):
        """
        Adds current instance to public or private channel.
        If user_id is specified it will be added to the private channel,
        If user_id is not specified it will be added to the public one instead.
        """
        if user_id is None:
            self.channel = 'public'
            user_id = uuid.uuid1().hex
        else:
            self.channel = 'private'
        self.id = user_id
        self.channels[self.channel][self.id] = self
        print 'Client connected to the %s channel.' % self.channel
        return

    def remove_client(self):
        """ removes a client """
        del self.channels[self.channel][self.id]

    @classmethod
    def broadcast(cls, message):
        """ broadcast message to all connected clients """
        clients = cls.get_clients()
        for id, client in clients.iteritems():
            client.send_message(message)

    @classmethod
    def send_private_message(self, user_id, message):
        """
        Send a message to a specific client.
        Returns True if successful, False otherwise
        """
        try:
            client = self.channels['private'][str(user_id)]
        except KeyError:
            print '====debug===='
            print self.channels['private']
            print 'client with id %s not found' % user_id
            return False

        client.send_message(message)
        print 'message sent to client #%s' % user_id
        return True

    @classmethod
    def get_clients(self):
        """ return a merge of public and private clients """
        public = self.channels['public']
        private = self.channels['private']
        return dict(public.items() + private.items())

    def open(self):
        """ method which is called every time a new client connects """
        print 'Connection opened.'
        user_id = self.get_argument('user_id', None)
        self.add_client(user_id)
        self.send_message('Welcome to nodeshot websocket server.')
        client_count = len(self.get_clients().keys())
        new_client_message = 'New client connected, now we have %d %s!' % (client_count, 'client' if client_count <= 1 else 'clients')
        self.broadcast(new_client_message)
        print self.channels['private']
        return

    def on_message(self, message):
        """ method which is called every time the server gets a message from a client """
        if message == 'help':
            self.send_message('Need help, huh?')
        print "Message received: '%s'" % message

    def on_close(self):
        """ method which is called every time a client disconnects """
        print 'Connection closed.'
        self.remove_client()
        client_count = len(self.get_clients().keys())
        new_client_message = '1 client disconnected, now we have %d %s!' % (client_count, 'client' if client_count <= 1 else 'clients')
        self.broadcast(new_client_message)