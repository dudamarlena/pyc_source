# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/api/amq/basic_message.py
# Compiled at: 2012-10-12 07:02:39
"""
Messages for AMQP

"""
from serialization import GenericContent
__all__ = [
 'Message']

class Message(GenericContent):
    """
    A Message for use with the Channnel.basic_* methods.

    """
    PROPERTIES = [
     ('content_type', 'shortstr'),
     ('content_encoding', 'shortstr'),
     ('application_headers', 'table'),
     ('delivery_mode', 'octet'),
     ('priority', 'octet'),
     ('correlation_id', 'shortstr'),
     ('reply_to', 'shortstr'),
     ('expiration', 'shortstr'),
     ('message_id', 'shortstr'),
     ('timestamp', 'timestamp'),
     ('type', 'shortstr'),
     ('user_id', 'shortstr'),
     ('app_id', 'shortstr'),
     ('cluster_id', 'shortstr')]

    def __init__(self, body='', children=None, **properties):
        """
        Expected arg types

            body: string
            children: (not supported)

        Keyword properties may include:

            content_type: shortstr
                MIME content type

            content_encoding: shortstr
                MIME content encoding

            application_headers: table
                Message header field table, a dict with string keys,
                and string | int | Decimal | datetime | dict values.

            delivery_mode: octet
                Non-persistent (1) or persistent (2)

            priority: octet
                The message priority, 0 to 9

            correlation_id: shortstr
                The application correlation identifier

            reply_to: shortstr
                The destination to reply to

            expiration: shortstr
                Message expiration specification

            message_id: shortstr
                The application message identifier

            timestamp: datetime.datetime
                The message timestamp

            type: shortstr
                The message type name

            user_id: shortstr
                The creating user id

            app_id: shortstr
                The creating application id

            cluster_id: shortstr
                Intra-cluster routing identifier

        Unicode bodies are encoded according to the 'content_encoding'
        argument. If that's None, it's set to 'UTF-8' automatically.

        example:

            msg = Message('hello world',
                            content_type='text/plain',
                            application_headers={'foo': 7})

        """
        if isinstance(body, unicode):
            if properties.get('content_encoding', None) is None:
                properties['content_encoding'] = 'UTF-8'
            self.body = body.encode(properties['content_encoding'])
        else:
            self.body = body
        super(Message, self).__init__(**properties)
        return

    def __eq__(self, other):
        """
        Check if the properties and bodies of this Message and another
        Message are the same.

        Received messages may contain a 'delivery_info' attribute,
        which isn't compared.

        """
        return super(Message, self).__eq__(other) and self.body == other.body