# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/responses/responses.py
# Compiled at: 2018-04-15 14:10:04
# Size of source mod 2**32: 7133 bytes
from typing import Iterable

class MenuElement:

    def __init__(self, type, title, payload=None, url=None, webview_height_ratio=None, messenger_extensions=None):
        self.type = type
        self.title = title
        self.payload = payload
        self.url = url
        self.buttons = []

    def __str__(self):
        text = 'element: ' + self.title
        return text

    def add_button(self, button):
        self.buttons.append(button)
        return button


class MessageElement:
    __doc__ = '\n    Base class for message elements.\n    '

    def to_message(self, fbid):
        return {'recipient':{'id': fbid},  'message':self.to_response()}

    def to_response(self):
        pass

    def get_response_for(self, platform='fb'):
        return str(self)

    def set_message_tag(self, tag):
        self.tag = tag

    def get_message_tag(self):
        """
        See https://developers.facebook.com/docs/messenger-platform/send-messages/message-tags
        :return: FB message tag
        """
        if hasattr(self, 'tag'):
            return self.tag

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)


class SenderActionMessage(MessageElement):

    def __init__(self, action):
        self.action = action

    def to_message(self, fbid):
        return {'sender_action':self.action, 
         'recipient':{'id': fbid}}


class TextMessage(MessageElement):
    __doc__ = '\n    A plain text message. You can attach buttons or quick replies.\n    '

    def __init__(self, text='', buttons=None, quick_replies=None):
        from .quick_reply import QuickReply
        self.text = text
        self.buttons = buttons if buttons else []
        self.quick_replies = [QuickReply(**reply) for reply in quick_replies or []]

    def to_response(self):
        if len(self.buttons):
            return {'attachment': {'type':'template', 
                            'payload':{'template_type':'button', 
                             'text':self.text, 
                             'buttons':[button.to_response() for button in self.buttons]}}}
        else:
            response = {'text': self.text}
            if self.quick_replies:
                response['quick_replies'] = [reply.to_response() for reply in self.quick_replies]
            return response

    def __str__(self):
        text = self.text
        for button in self.buttons:
            text += '\n ' + str(button)

        for reply in self.quick_replies:
            text += '\n ' + str(reply)

        return text

    def add_button(self, button):
        if self.quick_replies:
            raise ValueError('Cannot add quick_replies and buttons to the same message')
        self.buttons.append(button)
        return self

    def add_reply(self, quick_reply):
        return self.add_quick_reply(quick_reply)

    def add_quick_reply(self, quick_reply):
        if self.buttons:
            raise ValueError('Cannot add quick_replies and buttons to the same message')
        else:
            if isinstance(quick_reply, str):
                from core.responses.quick_reply import QuickReply
                quick_reply = QuickReply(title=quick_reply)
        self.quick_replies.append(quick_reply)
        return self

    def create_quick_reply(self, title=None, payload=None, image_url=None):
        from .quick_reply import QuickReply
        quick_reply = QuickReply(title=title, payload=payload, image_url=image_url)
        return self.add_quick_reply(quick_reply)

    def with_replies(self, replies: Iterable):
        for reply in replies:
            self.add_quick_reply(reply)

        return self

    def with_buttons(self, buttons: Iterable):
        for button in buttons:
            self.add_button(button)

        return self


class GenericTemplateElement(MessageElement):
    __doc__ = '\n    A horizontal card view with title, subtitle, image and buttons.\n    '

    def __init__(self, title, image_url=None, subtitle=None, item_url=None, buttons=None):
        self.title = _ellipsize(str(title)) if title else None
        self.subtitle = _ellipsize(str(subtitle)) if subtitle else None
        self.image_url = image_url
        self.item_url = item_url
        self.buttons = buttons if buttons else []

    def to_response(self):
        response = {'title':self.title, 
         'image_url':self.image_url, 
         'subtitle':self.subtitle, 
         'item_url':self.item_url}
        if self.buttons:
            response['buttons'] = [button.to_response() for button in self.buttons]
        return response

    def __str__(self):
        text = 'element: ' + self.title
        if self.subtitle:
            text += ' (' + self.subtitle + ')'
        for button in self.buttons:
            text += '\n  ' + str(button)

        return text

    def add_button(self, button):
        self.buttons.append(button)
        return self


class GenericTemplateMessage(MessageElement):
    __doc__ = '\n    A horizontal list of GenericTemplateElement items.\n    '

    def __init__(self, elements=None):
        self.elements = [GenericTemplateElement(**element) for element in elements or []]

    def to_response(self):
        return {'attachment': {'type':'template', 
                        'payload':{'template_type':'generic', 
                         'elements':[element.to_response() for element in self.elements[:10]]}}}

    def __str__(self):
        text = 'generic template:'
        for element in self.elements:
            text += '\n ' + str(element)

        return text

    def add_element(self, element):
        self.elements.append(element)
        return self

    def create_element(self, **kwargs) -> GenericTemplateElement:
        element = GenericTemplateElement(**kwargs)
        self.add_element(element)
        return element


class AttachmentMessage(MessageElement):

    def __init__(self, attachment_type, url):
        self.attachment_type = attachment_type
        self.url = url

    def to_response(self):
        return {'attachment': {'type':self.attachment_type, 
                        'payload':{'url': self.url}}}


def _ellipsize(text, max_len=80):
    if text is None:
        return
    else:
        if len(text) >= max_len:
            return text[:max_len - 5] + '...'
        return text


def _get_payload_string(payload):
    text = ''
    for entity, values in payload.items():
        if isinstance(values, list):
            for value in values:
                text += '/{}/{}/ '.format(entity, value)

            break
        text += '/{}/{}/ '.format(entity, values)

    return text