# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/responses/templates.py
# Compiled at: 2018-04-15 14:10:04
# Size of source mod 2**32: 1137 bytes
from typing import List
from core.responses.responses import MessageElement, GenericTemplateElement

class ListTemplate(MessageElement):

    def __init__(self, is_compact=False, button=None):
        super().__init__()
        self.elements = []
        self.compact = is_compact
        self.button = button

    def add_element(self, element: GenericTemplateElement):
        self.elements.append(element)
        return self

    def create_element(self, **kwargs):
        element = GenericTemplateElement(**kwargs)
        return self.add_element(element)

    def to_response(self):
        response = {'attachment': {'type':'template', 
                        'payload':{'template_type':'list', 
                         'top_element_style':'compact' if self.compact else 'large', 
                         'elements':[element.to_response() for element in self.elements[:4]]}}}
        if self.button:
            response['attachment']['payload']['buttons'] = [
             self.button.to_response()]
        return response