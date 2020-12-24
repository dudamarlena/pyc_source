# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jannis/Documents/code/rtr-supercell/supercell/env3/lib/python3.6/site-packages/supercell/consumer.py
# Compiled at: 2018-10-08 11:55:52
# Size of source mod 2**32: 4704 bytes
from __future__ import absolute_import, division, print_function, with_statement
from collections import defaultdict
import json
from supercell._compat import with_metaclass
from supercell.mediatypes import ContentType, MediaType
from supercell.acceptparsing import parse_accept_header
__all__ = [
 'NoConsumerFound', 'ConsumerBase', 'JsonConsumer']

class NoConsumerFound(Exception):
    __doc__ = "Raised if no matching consumer for the client's `Content-Type` header\n    was found."


class ConsumerMeta(type):
    __doc__ = 'Meta class for all consumers.\n\n    This will simply register a consumer with the respective content type\n    information and make them available in a list of content types and their\n    consumer.\n    '
    KNOWN_CONTENT_TYPES = defaultdict(list)

    def __new__(cls, name, bases, dct):
        consumer_class = type.__new__(cls, name, bases, dct)
        if name != 'ConsumerBase':
            if hasattr(consumer_class, 'CONTENT_TYPE'):
                ct = consumer_class.CONTENT_TYPE
                ConsumerMeta.KNOWN_CONTENT_TYPES[ct.content_type].append((
                 ct, consumer_class))
        return consumer_class


class ConsumerBase(with_metaclass(ConsumerMeta, object)):
    __doc__ = "Base class for content type consumers.\n\n    In order to create a new consumer, you must create a new class that\n    inherits from :py:class:`ConsumerBase` and sets the\n    :data:`ConsumerBase.CONTENT_TYPE` variable::\n\n        class MyConsumer(s.ConsumerBase):\n\n            CONTENT_TYPE = s.ContentType('application/xml')\n\n            def consume(self, handler, model):\n                return model(lxml.from_string(handler.request.body))\n\n    .. seealso:: :py:mod:`supercell.api.consumer.JsonConsumer.consume`\n    "
    CONTENT_TYPE = None

    @staticmethod
    def map_consumer(content_type, handler):
        """Map a given content type to the correct provider implementation.

        If no provider matches, raise a `NoProviderFound` exception.

        :param accept_header: HTTP Accept header value
        :type accept_header: str
        :param handler: supercell request handler

        :raises: :exc:`NoConsumerFound`
        """
        accept = parse_accept_header(content_type)
        if len(accept) == 0:
            raise NoConsumerFound()
        ctype, params, q = accept[0]
        if ctype not in handler._CONS_CONTENT_TYPES:
            raise NoConsumerFound()
        c = ContentType(ctype, vendor=(params.get('vendor', None)), version=(params.get('version', None)))
        if c not in handler._CONS_CONTENT_TYPES[ctype]:
            raise NoConsumerFound()
        known_types = [t for t in ConsumerMeta.KNOWN_CONTENT_TYPES[ctype] if t[0] == c]
        if len(known_types) == 1:
            return (
             handler._CONS_MODEL[c], known_types[0][1])
        raise NoConsumerFound()

    def consume(self, handler, model):
        """This method should return the correct representation as a parsed
        model.

        :param model: the model to convert to a certain content type
        :type model: :class:`schematics.models.Model`
        """
        raise NotImplementedError


class JsonConsumer(ConsumerBase):
    __doc__ = 'Default **application/json** consumer.'
    CONTENT_TYPE = ContentType(MediaType.ApplicationJson)

    def consume(self, handler, model):
        """Parse the body json via :func:`json.loads` and initialize the
        `model`.

        .. seealso:: :py:mod:`supercell.api.provider.ProviderBase.provide`
        """
        return model(json.loads(handler.request.body.decode('utf8')))


class JsonPatchConsumer(JsonConsumer):
    __doc__ = 'Default **application/json-patch+json** consumer.'
    CONTENT_TYPE = ContentType(MediaType.ApplicationJsonPatch)