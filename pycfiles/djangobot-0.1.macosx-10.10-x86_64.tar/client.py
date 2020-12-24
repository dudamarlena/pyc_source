# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/scott/.envs/home/lib/python2.7/site-packages/djangobot/client.py
# Compiled at: 2016-04-09 16:45:12
import json
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory, connectWS
import channels
from twisted.internet import reactor, ssl
from twisted.internet.ssl import ClientContextFactory
from .slack import SlackAPI

def pack(message):
    """
    Serialize the message into something for sending
    across the wire.

    Args:
        message: {dict} dictionary that full specifies a slack message
    """
    return json.dumps(message).encode('utf8')


def unpack(text):
    """
    Decode & Load

    Args:
        text: {str} JSON blob
    """
    return json.loads(text.decode('utf8'))


class SlackClientProtocol(WebSocketClientProtocol):
    """
    This defines how messages from Slack are passed onto
    Channels and how a specific channel is passed to Slack
    """

    def __init__(self, *args, **kwargs):
        super(SlackClientProtocol, self).__init__(*args, **kwargs)
        self._message_id = 0

    @property
    def message_id(self):
        """
        Return an auto-incrementing integer
        """
        self._message_id += 1
        return self._message_id

    def make_message(self, text, channel):
        """
        High-level function for creating messages. Return packed bytes.

        Args:
            text: {str}
            channel: {str} Either name or ID
        """
        try:
            channel_id = self.slack.channel_from_name(channel)['id']
        except ValueError:
            channel_id = channel

        return pack({'text': text, 
           'type': 'message', 
           'channel': channel_id, 
           'id': self.message_id})

    def translate(self, message):
        """
        Translate machine identifiers into human-readable
        """
        try:
            user_id = message.pop('user')
            user = self.slack.user_from_id(user_id)
            message['user'] = user['name']
        except (KeyError, IndexError, ValueError):
            pass

        try:
            channel_id = message.pop('channel')
            channel = self.slack.channel_from_id(channel_id)
            message['channel'] = channel['name']
        except (KeyError, IndexError, ValueError):
            pass

        return message

    def sendHello(self):
        self.sendMessage(self.make_message('<yawn /> Why hello there.', 'general'))

    def onOpen(self):
        """
        Store this protocol instance in the factory and wave hello.
        """
        self.factory.protocols.append(self)
        self.sendHello()

    def onMessage(self, payload, isBinary):
        """
        Send the payload onto the {slack.[payload['type]'} channel.
        The message is transalated from IDs to human-readable identifiers.

        Note: The slack API only sends JSON, isBinary will always be false.
        """
        msg = self.translate(unpack(payload))
        if 'type' in msg:
            channel_name = ('slack.{}').format(msg['type'])
            print ('Sending on {}').format(channel_name)
            channels.Channel(channel_name).send({'text': pack(msg)})

    def sendSlack(self, message):
        """
        Send message to Slack
        """
        channel = message.get('channel', 'general')
        self.sendMessage(self.make_message(message['text'], channel))


class SlackClientFactory(WebSocketClientFactory):

    def run(self):
        if self.isSecure:
            contextFactory = ssl.ClientContextFactory()
        else:
            contextFactory = None
        self.connector = connectWS(self, contextFactory)
        self.read_channel()
        reactor.run(installSignalHandlers=True)
        return

    def read_channel(self):
        """
        Get available messages and send through to the protocol
        """
        channel, message = self.protocol.channel_layer.receive_many(['slack.send'], block=False)
        delay = 0.1
        if channel:
            self.protocols[0].sendSlack(message)
        reactor.callLater(delay, self.read_channel)


class Client(object):
    """
    Main client to instantiate the SlackAPI and client factory
    """

    def __init__(self, channel_layer, token, channel_name='slack.send'):
        """
        Args:
            channel_layer: channel layer on which this client will communicate to Django
            token: {str} Slack token
            channel_name: {str} channel name to send messages that will come back to slack
        """
        self.channel_layer = channel_layer
        self.token = token
        self.channel_name = channel_name

    def run(self):
        """
        Main interface. Instantiate the SlackAPI, connect to RTM
        and start the client.
        """
        slack = SlackAPI(token=self.token)
        rtm = slack.rtm_start()
        factory = SlackClientFactory(rtm['url'])
        factory.protocol = SlackClientProtocol
        factory.protocol.slack = slack
        factory.protocol.channel_layer = self.channel_layer
        factory.channel_name = self.channel_name
        factory.run()