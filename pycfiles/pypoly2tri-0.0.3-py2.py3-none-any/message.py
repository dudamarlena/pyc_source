# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pypoly/content/webpage/message.py
# Compiled at: 2011-09-13 05:02:11
import pypoly
from pypoly.content.webpage import Content, ContentType

class Message(Content):
    type = ContentType('message')

    def __init__(self, **options):
        self.text = ''
        self.label = ''
        Content.__init__(self, None, **options)
        return

    def generate(self, **values):
        tpl = pypoly.template.load_web('webpage', 'message')
        return tpl.generate(message=self)


class Error(Message):
    type = ContentType('message.error')


class Info(Message):
    type = ContentType('message.info')


class Success(Message):
    type = ContentType('message.success')


class Warning(Message):
    type = ContentType('message.warning')