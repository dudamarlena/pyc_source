# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/formprocess/pylonshandler.py
# Compiled at: 2011-03-24 02:54:04
""" Pylons specific form handlers and schemas. """
import pylons
from formprocess.handler import FormHandler

def set_fill_encoding(handler_instance, defaults, errors, state, fill_kwargs):
    """ Set the encoding for htmlfill to use. """
    fill_kwargs.update({'encoding': pylons.response.determine_charset()})
    return fill_kwargs


class PylonsFormHandler(FormHandler):
    """ A form handler for use with pylons. """

    def __init__(self, **kwargs):
        kwargs.setdefault('customize_fill_kwargs_hooks', []).append(set_fill_encoding)
        super(PylonsFormHandler, self).__init__(**kwargs)