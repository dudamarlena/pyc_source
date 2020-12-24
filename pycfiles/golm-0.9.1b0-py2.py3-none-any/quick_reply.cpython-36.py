# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/responses/quick_reply.py
# Compiled at: 2018-04-15 14:10:04
# Size of source mod 2**32: 1302 bytes
import json
from core.responses.responses import MessageElement, _get_payload_string
from core.serialize import json_serialize

class QuickReply(MessageElement):
    __doc__ = '\n    A button with text that gets sent as message when clicked.\n    '

    def __init__(self, title=None, payload=None, image_url=None):
        self.title = title
        self.payload = payload
        self.image_url = image_url

    def to_response(self):
        response = {'content_type':'text', 
         'title':self.title[:20], 
         'payload':json.dumps(self.payload if self.payload else {}, default=json_serialize)}
        if self.image_url:
            response['image_url'] = self.image_url
        return response

    def __str__(self):
        text = 'quick_reply: '
        if self.title:
            text += self.title + ': '
        if self.payload:
            text += _get_payload_string(self.payload)
        return text


class LocationQuickReply(QuickReply):
    __doc__ = "\n    A button that asks for user's location when clicked.\n    Currently only supported on Facebook Messenger.\n    "

    def __init__(self):
        super().__init__()

    def to_response(self):
        return {'content_type': 'location'}

    def __str__(self):
        return str(super) + ' location'