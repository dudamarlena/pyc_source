# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jannis/Documents/code/rtr-supercell/supercell/env3/lib/python3.6/site-packages/supercell/decorators.py
# Compiled at: 2019-02-13 11:26:58
# Size of source mod 2**32: 4593 bytes
"""Several decorators for using with :class:`supercell.api.RequestHandler`
implementations.
"""
from __future__ import absolute_import, division, print_function, with_statement
from collections import defaultdict
from supercell.mediatypes import ContentType

def provides(content_type, vendor=None, version=None, default=False, partial=False):
    """Class decorator for mapping HTTP GET responses to content types and
    their representation.

    In order to allow the **application/json** content type, create the handler
    class like this::

        @s.provides(s.MediaType.ApplicationJson)
        class MyHandler(s.RequestHandler):
            pass

    It is also possible to support more than one content type. The content type
    selection is then based on the client **Accept** header. If this is not
    present, ordering of the :func:`provides` decorators matter, i.e. the first
    content type is used::

        @s.provides(s.MediaType.ApplicationJson)
        class MyHandler(s.RequestHandler):
            ...

    :param str content_type: The base content type such as **application/json**
    :param str vendor: Any vendor information for the base content type
    :param float version: The vendor version
    :param bool default: If **True** and no **Accept** header is present, this
                         content type is provided
    :param bool partial: If **True**, the provider can return partial
                         representations, i.e. the underlying model validates
                         even though required fields are missing.
    """

    def wrapper(cls):
        if not isinstance(cls, type):
            raise AssertionError('This decorator may only be used as class decorator')
        else:
            if not hasattr(cls, '_PROD_CONTENT_TYPES'):
                cls._PROD_CONTENT_TYPES = defaultdict(list)
            if not hasattr(cls, '_PROD_CONFIGURATION'):
                cls._PROD_CONFIGURATION = defaultdict(dict)
            ctype = ContentType(content_type, vendor, version)
            cls._PROD_CONTENT_TYPES[content_type].append(ctype)
            cls._PROD_CONFIGURATION[content_type]['partial'] = partial
            assert default and 'default' not in cls._PROD_CONTENT_TYPES, 'TODO: nice msg'
            cls._PROD_CONTENT_TYPES['*/*'] = [ctype]
            cls._PROD_CONFIGURATION['*/*']['partial'] = partial
        return cls

    return wrapper


def consumes(content_type, model, vendor=None, version=None, validate=True):
    """Class decorator for mapping HTTP POST and PUT bodies to

    Example::

        @s.consumes(s.MediaType.ApplicationJson, model=Model)
        class MyHandler(s.RequestHandler):

            def post(self, *args, **kwargs):
                # ...
                raise s.OkCreated()

    :param str content_type: The base content type such as **application/json**
    :param model: The model that should be consumed.
    :type model: :class:`schematics.models.Model`
    :param str vendor: Any vendor information for the base content type
    :param float version: The vendor version
    :param bool validate: Whether to validate the consumed model
    """

    def wrapper(cls):
        if not isinstance(cls, type):
            raise AssertionError('This decorator may only be used as class decorator')
        else:
            assert model, 'In order to consume content a schematics model class has to be given via the model parameter'
            if not hasattr(cls, '_CONS_CONTENT_TYPES'):
                cls._CONS_CONTENT_TYPES = defaultdict(list)
            cls._CONS_MODEL = hasattr(cls, '_CONS_MODEL') or dict()
        ct = ContentType(content_type, vendor, version)
        cls._CONS_CONTENT_TYPES[content_type].append(ct)
        cls._CONS_MODEL[ct] = (model, validate)
        return cls

    return wrapper