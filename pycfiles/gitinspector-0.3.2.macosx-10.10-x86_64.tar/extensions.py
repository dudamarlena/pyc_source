# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/extensions.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import print_function
from __future__ import unicode_literals
from localization import N_
from outputable import Outputable
import terminal, textwrap
DEFAULT_EXTENSIONS = [
 b'java', b'c', b'cc', b'cpp', b'h', b'hh', b'hpp', b'py', b'glsl', b'rb', b'js', b'sql']
__extensions__ = DEFAULT_EXTENSIONS
__located_extensions__ = set()

def get():
    global __extensions__
    return __extensions__


def define(string):
    global __extensions__
    __extensions__ = string.split(b',')


def add_located(string):
    if len(string) > 0:
        __located_extensions__.add(string)


EXTENSIONS_INFO_TEXT = N_(b'The extensions below were found in the repository history')
EXTENSIONS_MARKED_TEXT = N_(b'(extensions used during statistical analysis are marked)')

class Extensions(Outputable):

    def output_html(self):
        if __located_extensions__:
            extensions_xml = b'<div><div class="box">'
            extensions_xml += (b'<p>{0} {1}.</p><p>').format(_(EXTENSIONS_INFO_TEXT), _(EXTENSIONS_MARKED_TEXT))
            for i in __located_extensions__:
                if i in __extensions__:
                    extensions_xml += b'<strong>' + i + b'</strong>'
                else:
                    extensions_xml += i
                extensions_xml += b' '

            extensions_xml += b'</p></div></div>'
            print(extensions_xml)

    def output_text(self):
        if __located_extensions__:
            print(b'\n' + textwrap.fill((b'{0} {1}:').format(_(EXTENSIONS_INFO_TEXT), _(EXTENSIONS_MARKED_TEXT)), width=terminal.get_size()[0]))
            for i in __located_extensions__:
                if i in __extensions__:
                    print(b'[' + terminal.__bold__ + i + terminal.__normal__ + b']', end=b' ')
                else:
                    print(i, end=b' ')

            print(b'')

    def output_xml(self):
        if __located_extensions__:
            message_xml = b'\t\t<message>' + _(EXTENSIONS_INFO_TEXT) + b'</message>\n'
            used_extensions_xml = b''
            unused_extensions_xml = b''
            for i in __located_extensions__:
                if i in __extensions__:
                    used_extensions_xml += b'\t\t\t<extension>' + i + b'</extension>\n'
                else:
                    unused_extensions_xml += b'\t\t\t<extension>' + i + b'</extension>\n'

            print(b'\t<extensions>\n' + message_xml + b'\t\t<used>\n' + used_extensions_xml + b'\t\t</used>\n' + b'\t\t<unused>\n' + unused_extensions_xml + b'\t\t</unused>\n' + b'\t</extensions>')