# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pycoon\components\tmp.py
# Compiled at: 2007-03-10 10:10:14
__author__ = 'Andrey Nordin <mailto:anrienord@inbox.ru>'
import lxml.etree as etree
from pycoon.components import Generator, Component
from docutils.core import publish_parts

class RestructuredGenerator(Generator):
    __module__ = __name__

    def configure(self, element=None):
        Component.configure(self, element)
        if element is not None:
            self.encoding = element.find('encoding').text
        else:
            self.encoding = 'utf-8'
        return

    def generate(self, env, source, params):
        self.log.debug('<map:generate src="%s"> process()' % source.uri)
        data = source.read()
        overrides = {'input_encoding': self.encoding, 'output_encoding': self.encoding}
        data = publish_parts(data, writer_name='html', settings_overrides=overrides).get('html_body')
        env.response.body = etree.fromstring('<div xmlns="http://www.w3.org/1999/xhtml">\n  %s\n</div>' % data)