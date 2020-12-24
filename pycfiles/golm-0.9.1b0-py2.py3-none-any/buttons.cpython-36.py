# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/responses/buttons.py
# Compiled at: 2018-04-15 14:10:04
# Size of source mod 2**32: 3324 bytes
import json
from abc import ABC, abstractmethod
from core.responses.responses import MessageElement
from core.serialize import json_serialize

class Button(MessageElement, ABC):
    __doc__ = "\n    An abstract chat button. Don't use this class directly.\n    "

    @abstractmethod
    def to_response(self):
        raise NotImplementedError('Abstract method')

    @abstractmethod
    def __str__(self):
        raise NotImplementedError('Abstract method')


class PayloadButton(Button):
    __doc__ = '\n    A button that sends predefined data back to the bot when clicked.\n    '

    def __init__(self, title, payload):
        super(Button, self).__init__()
        self.title = title
        self.payload = payload

    def to_response(self):
        return {'title':self.title, 
         'type':'postback', 
         'payload':json.dumps(self.payload, default=json_serialize)}

    def __str__(self):
        return 'button: {}: {}'.format(self.title, self.payload)


class LinkButton(Button):
    __doc__ = '\n    A button that opens a website when clicked.\n    '

    def __init__(self, title, url, webview=False):
        super(Button, self).__init__()
        self.title = title
        self.url = url
        self.webview_height_ratio = 'compact' if webview else 'full'

    def to_response(self):
        return {'title':self.title, 
         'type':'web_url', 
         'url':self.url, 
         'webview_height_ratio':self.webview_height_ratio}

    def __str__(self):
        return 'button: {}: {}'.format(self.title, self.url)


class PhoneButton(Button):
    __doc__ = '\n    A button that calls a number when clicked.\n    Currently only Facebook Messenger is supported.\n    '

    def __init__(self, title, phone_number):
        super(Button, self).__init__()
        self.title = title
        self.phone_number = phone_number

    def to_response(self):
        return {'title':self.title, 
         'type':'phone_number', 
         'payload':self.phone_number}

    def __str__(self):
        return 'button: {}: {}'.format(self.title, self.phone_number)


class AccountLinkButton(Button):
    __doc__ = '\n    A button that shows the FB messenger account linking dialog when clicked.\n    '

    def __init__(self, url):
        super(Button, self).__init__()
        self.url = url

    def to_response(self):
        return {'type':'account_link', 
         'url':self.url}

    def __str__(self):
        return 'button: account_link: {}'.format(self.url)


class AccountUnlinkButton(Button):
    __doc__ = '\n    A button that shows the FB messenger account unlinking dialog when clicked.\n    '

    def __init__(self, url):
        super(Button, self).__init__()
        self.url = url

    def to_response(self):
        return {'type': 'account_unlink'}

    def __str__(self):
        return 'button: account_unlink'


class ShareButton(Button):
    __doc__ = "\n    A button that opens share dialog for the message it's attached to.\n    Currently only Facebook Messener is supported.\n    "

    def __init__(self):
        super(Button, self).__init__()

    def to_response(self):
        return {'type': 'element_share'}

    def __str__(self):
        return 'button: share'