# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/rpc/proxy.py
# Compiled at: 2016-06-13 14:11:03
"""
A helper class for proxy objects to remote APIs.

For more information about rpc API version numbers, see:
    rpc/dispatcher.py
"""
import os
from vsm.openstack.common import rpc

class RpcProxy(object):
    """A helper class for rpc clients.

    This class is a wrapper around the RPC client API.  It allows you to
    specify the topic and API version in a single place.  This is intended to
    be used as a base class for a class that implements the client side of an
    rpc API.
    """

    def __init__(self, topic, default_version):
        """Initialize an RpcProxy.

        :param topic: The topic to use for all messages.
        :param default_version: The default API version to request in all
               outgoing messages.  This can be overridden on a per-message
               basis.
        """
        self.topic = topic
        self.default_version = default_version
        self.host = os.popen('hostname').read().strip()
        super(RpcProxy, self).__init__()

    def _set_version(self, msg, vers):
        """Helper method to set the version in a message.

        :param msg: The message having a version added to it.
        :param vers: The version number to add to the message.
        """
        msg['version'] = vers if vers else self.default_version

    def _get_topic(self, topic):
        """Return the topic to use for a message."""
        if topic:
            return topic
        return self.topic

    @staticmethod
    def make_msg(method, **kwargs):
        return {'method': method, 'args': kwargs}

    def call(self, context, msg, topic=None, version=None, timeout=None, need_try=True):
        """rpc.call() a remote method.

        :param context: The request context
        :param msg: The message to send, including the method and args.
        :param topic: Override the topic for this message.
        :param timeout: (Optional) A timeout to use when waiting for the
               response.  If no timeout is specified, a default timeout will be
               used that is usually sufficient.
        :param version: (Optional) Override the requested API version in this
               message.

        :returns: The return value from the remote method.
        """
        self._set_version(msg, version)
        return rpc.call(context, self._get_topic(topic), msg, timeout, need_try=need_try)

    def multicall(self, context, msg, topic=None, version=None, timeout=None, need_try=True):
        """rpc.multicall() a remote method.

        :param context: The request context
        :param msg: The message to send, including the method and args.
        :param topic: Override the topic for this message.
        :param timeout: (Optional) A timeout to use when waiting for the
               response.  If no timeout is specified, a default timeout will be
               used that is usually sufficient.
        :param version: (Optional) Override the requested API version in this
               message.

        :returns: An iterator that lets you process each of the returned values
                  from the remote method as they arrive.
        """
        self._set_version(msg, version)
        return rpc.multicall(context, self._get_topic(topic), msg, timeout, need_try=need_try)

    def cast(self, context, msg, topic=None, version=None, need_try=True):
        """rpc.cast() a remote method.

        :param context: The request context
        :param msg: The message to send, including the method and args.
        :param topic: Override the topic for this message.
        :param version: (Optional) Override the requested API version in this
               message.

        :returns: None.  rpc.cast() does not wait on any return value from the
                  remote method.
        """
        self._set_version(msg, version)
        rpc.cast(context, self._get_topic(topic), msg, need_try)

    def fanout_cast(self, context, msg, topic=None, version=None, need_try=True):
        """rpc.fanout_cast() a remote method.

        :param context: The request context
        :param msg: The message to send, including the method and args.
        :param topic: Override the topic for this message.
        :param version: (Optional) Override the requested API version in this
               message.

        :returns: None.  rpc.fanout_cast() does not wait on any return value
                  from the remote method.
        """
        self._set_version(msg, version)
        rpc.fanout_cast(context, self._get_topic(topic), msg, need_try)

    def cast_to_server(self, context, server_params, msg, topic=None, version=None, need_try=True):
        """rpc.cast_to_server() a remote method.

        :param context: The request context
        :param server_params: Server parameters.  See rpc.cast_to_server() for
               details.
        :param msg: The message to send, including the method and args.
        :param topic: Override the topic for this message.
        :param version: (Optional) Override the requested API version in this
               message.

        :returns: None.  rpc.cast_to_server() does not wait on any
                  return values.
        """
        self._set_version(msg, version)
        rpc.cast_to_server(context, server_params, self._get_topic(topic), msg, need_try)

    def fanout_cast_to_server(self, context, server_params, msg, topic=None, version=None, need_try=True):
        """rpc.fanout_cast_to_server() a remote method.

        :param context: The request context
        :param server_params: Server parameters.  See rpc.cast_to_server() for
               details.
        :param msg: The message to send, including the method and args.
        :param topic: Override the topic for this message.
        :param version: (Optional) Override the requested API version in this
               message.

        :returns: None.  rpc.fanout_cast_to_server() does not wait on any
                  return values.
        """
        self._set_version(msg, version)
        rpc.fanout_cast_to_server(context, server_params, self._get_topic(topic), msg, need_try)