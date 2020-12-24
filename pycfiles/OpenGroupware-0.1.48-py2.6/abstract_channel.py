# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/api/amq/abstract_channel.py
# Compiled at: 2012-10-12 07:02:39
"""
Code common to Connection and Channel objects.

"""
from serialization import AMQPWriter
__all__ = [
 'AbstractChannel']

class AbstractChannel(object):
    """
    Superclass for both the Connection, which is treated
    as channel 0, and other user-created Channel objects.

    The subclasses must have a _METHOD_MAP class property, mapping
    between AMQP method signatures and Python methods.

    """

    def __init__(self, connection, channel_id):
        self.connection = connection
        self.channel_id = channel_id
        connection.channels[channel_id] = self
        self.method_queue = []
        self.auto_decode = False

    def __enter__(self):
        """
        Support for Python >= 2.5 'with' statements.

        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Support for Python >= 2.5 'with' statements.

        """
        self.close()

    def _send_method(self, method_sig, args='', content=None):
        """
        Send a method for our channel.

        """
        if isinstance(args, AMQPWriter):
            args = args.getvalue()
        self.connection.method_writer.write_method(self.channel_id, method_sig, args, content)

    def close(self):
        """
        Close this Channel or Connection

        """
        raise NotImplementedError('Must be overriden in subclass')

    def wait(self, allowed_methods=None, timeout=None):
        """
        Wait for a method that matches our allowed_methods parameter (the
        default value of None means match any method), and dispatch to it.

        """
        (method_sig, args, content) = self.connection._wait_method(self.channel_id, allowed_methods, timeout)
        if content and self.auto_decode and hasattr(content, 'content_encoding'):
            try:
                content.body = content.body.decode(content.content_encoding)
            except Exception:
                pass

        amqp_method = self._METHOD_MAP.get(method_sig, None)
        if amqp_method is None:
            raise Exception('Unknown AMQP method (%d, %d)' % method_sig)
        if content is None:
            return amqp_method(self, args)
        else:
            return amqp_method(self, args, content)
            return

    _METHOD_MAP = {}