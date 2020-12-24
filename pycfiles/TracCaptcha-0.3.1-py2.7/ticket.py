# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_captcha/ticket.py
# Compiled at: 2010-06-29 17:31:38
from genshi.filters.transform import Transformer
from trac.core import Component, implements
from trac.ticket.api import ITicketManipulator
from trac.web.api import ITemplateStreamFilter
from trac_captcha.controller import TracCaptchaController
__all__ = [
 'TicketCaptcha']

class TicketCaptcha(Component):
    implements(ITemplateStreamFilter, ITicketManipulator)

    def filter_stream(self, req, method, filename, stream, data):
        if filename != 'ticket.html':
            return stream
        transformer = Transformer('//div[@class="buttons"]')
        return TracCaptchaController(self.env).inject_captcha_into_stream(req, stream, transformer)

    def prepare_ticket(self, req, ticket, fields, actions):
        pass

    def validate_ticket(self, req, ticket):
        error_message = TracCaptchaController(self.env).check_captcha_solution(req)
        if error_message is None:
            return ()
        else:
            return (
             (
              None, error_message),)