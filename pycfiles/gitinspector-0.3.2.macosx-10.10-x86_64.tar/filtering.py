# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/filtering.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import print_function
from __future__ import unicode_literals
from localization import N_
from outputable import Outputable
import re, terminal, textwrap
__filters__ = {b'file': [[], set()], b'author': [[], set()], b'email': [[], set()], b'revision': [[], set()]}

class InvalidRegExpError(ValueError):

    def __init__(self, msg):
        super(InvalidRegExpError, self).__init__(msg)
        self.msg = msg


def get():
    return __filters__


def __add_one__(string):
    for i in __filters__:
        if (i + b':').lower() == string[0:len(i) + 1].lower():
            __filters__[i][0].append(string[len(i) + 1:])
            return

    __filters__[b'file'][0].append(string)


def add(string):
    rules = string.split(b',')
    for rule in rules:
        __add_one__(rule)


def clear():
    for i in __filters__:
        __filters__[i][0] = []


def get_filered(filter_type=b'file'):
    return __filters__[filter_type][1]


def has_filtered():
    for i in __filters__:
        if __filters__[i][1]:
            return True

    return False


def set_filtered(string, filter_type=b'file'):
    string = string.strip()
    if len(string) > 0:
        for i in __filters__[filter_type][0]:
            try:
                if re.search(i, string) != None:
                    __filters__[filter_type][1].add(string)
                    return True
            except:
                raise InvalidRegExpError(_(b'invalid regular expression specified'))

    return False


FILTERING_INFO_TEXT = N_(b'The following files were excluded from the statistics due to the specified exclusion patterns')
FILTERING_AUTHOR_INFO_TEXT = N_(b'The following authors were excluded from the statistics due to the specified exclusion patterns')
FILTERING_EMAIL_INFO_TEXT = N_(b'The authors with the following emails were excluded from the statistics due to the specified exclusion patterns')
FILTERING_EMAIL_INFO_TEXT = N_(b'The following commit revisions were excluded from the statistics due to the specified exclusion patterns')

class Filtering(Outputable):

    @staticmethod
    def __output_html_section__(info_string, filtered):
        filtering_xml = b''
        if filtered:
            filtering_xml += b'<p>' + info_string + b'.' + b'</p>'
            for i in filtered:
                filtering_xml += b'<p>' + i + b'</p>'

        return filtering_xml

    def output_html(self):
        if has_filtered():
            filtering_xml = b'<div><div class="box">'
            Filtering.__output_html_section__(_(FILTERING_INFO_TEXT), __filters__[b'file'][1])
            Filtering.__output_html_section__(_(FILTERING_AUTHOR_INFO_TEXT), __filters__[b'author'][1])
            Filtering.__output_html_section__(_(FILTERING_EMAIL_INFO_TEXT), __filters__[b'email'][1])
            Filtering.__output_html_section__(_(FILTERING_EMAIL_INFO_TEXT), __filters__[b'revision'][1])
            filtering_xml += b'</div></div>'
            print(filtering_xml)

    @staticmethod
    def __output_text_section__(info_string, filtered):
        if filtered:
            print(b'\n' + textwrap.fill(info_string + b':', width=terminal.get_size()[0]))
            for i in filtered:
                width, _unused = terminal.get_size()
                print(b'...%s' % i[-width + 3:] if len(i) > width else i)

    def output_text(self):
        Filtering.__output_text_section__(_(FILTERING_INFO_TEXT), __filters__[b'file'][1])
        Filtering.__output_text_section__(_(FILTERING_AUTHOR_INFO_TEXT), __filters__[b'author'][1])
        Filtering.__output_text_section__(_(FILTERING_EMAIL_INFO_TEXT), __filters__[b'email'][1])
        Filtering.__output_text_section__(_(FILTERING_EMAIL_INFO_TEXT), __filters__[b'revision'][1])

    @staticmethod
    def __output_xml_section__(info_string, filtered, container_tagname):
        if filtered:
            message_xml = b'\t\t\t<message>' + info_string + b'</message>\n'
            filtering_xml = b''
            for i in filtered:
                filtering_xml += (b'\t\t\t\t<entry>').format(container_tagname) + i + (b'</entry>\n').format(container_tagname)

            print((b'\t\t<{0}>').format(container_tagname))
            print(message_xml + b'\t\t\t<entries>\n' + filtering_xml + b'\t\t\t</entries>\n')
            print((b'\t\t</{0}>').format(container_tagname))

    def output_xml(self):
        if has_filtered():
            print(b'\t<filtering>')
            Filtering.__output_xml_section__(_(FILTERING_INFO_TEXT), __filters__[b'file'][1], b'files')
            Filtering.__output_xml_section__(_(FILTERING_AUTHOR_INFO_TEXT), __filters__[b'author'][1], b'authors')
            Filtering.__output_xml_section__(_(FILTERING_EMAIL_INFO_TEXT), __filters__[b'email'][1], b'emails')
            Filtering.__output_xml_section__(_(FILTERING_EMAIL_INFO_TEXT), __filters__[b'revision'][1].union(), b'revisions')
            print(b'\t</filtering>')