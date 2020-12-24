# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycommunicate\proxies\dom\html.py
# Compiled at: 2016-06-11 07:22:25
from pycommunicate.proxies.dom.element import ElementWrapper

class HTMLWrapper:

    def __init__(self, controller):
        self.controller = controller

    def element_exists(self, selector):
        return self.controller.socket_interface.request('element.exists', selector)

    def element_by_selector(self, selector):
        if self.element_exists(selector):
            return ElementWrapper(self, selector)
        else:
            return
            return