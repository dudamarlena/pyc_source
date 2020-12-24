# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jsonmapper\messages.py
# Compiled at: 2012-02-25 11:03:26
"""
Message container for Twitter Bootstrap alert messages, to be put into request.session.flash and read out into a template.
"""

class GenericMessage(object):
    types = [
     'success', 'info', 'block', 'error', 'danger']

    def __init__(self, body, heading=None):
        self.heading = heading
        self.body = body


class GenericSuccessMessage(GenericMessage):
    type = 'success'


class GenericInfoMessage(GenericMessage):
    type = 'info'


class GenericBlockMessage(GenericMessage):
    type = 'block'


class GenericErrorMessage(GenericMessage):
    type = 'error'


class GenericDangerMessage(GenericMessage):
    type = 'danger'