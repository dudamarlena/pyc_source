# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/responsibilities.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import print_function
from __future__ import unicode_literals
from localization import N_
from outputable import Outputable
import blame, changes, format, gravatar, terminal, textwrap

class ResponsibiltyEntry:
    blames = {}


class Responsibilities:

    @staticmethod
    def get(hard, useweeks, author_name):
        author_blames = {}
        for i in blame.get(hard, useweeks, changes.get(hard)).blames.items():
            if author_name == i[0][0]:
                total_rows = i[1].rows - i[1].comments
                if total_rows > 0:
                    author_blames[i[0][1]] = total_rows

        return sorted(author_blames.items())


RESPONSIBILITIES_INFO_TEXT = N_(b'The following repsonsibilties, by author, were found in the current revision of the repository (comments are exluded from the line count, if possible)')
MOSTLY_RESPONSIBLE_FOR_TEXT = N_(b'is mostly responsible for')

class ResponsibilitiesOutput(Outputable):

    def __init__(self, hard, useweeks):
        self.hard = hard
        self.useweeks = useweeks
        Outputable.__init__(self)
        self.changes = changes.get(hard)

    def output_text(self):
        print(b'\n' + textwrap.fill(_(RESPONSIBILITIES_INFO_TEXT) + b':', width=terminal.get_size()[0]))
        for i in sorted(set(i[0] for i in blame.get(self.hard, self.useweeks, self.changes).blames)):
            responsibilities = sorted(((i[1], i[0]) for i in Responsibilities.get(self.hard, self.useweeks, i)), reverse=True)
            if responsibilities:
                print(b'\n' + i, _(MOSTLY_RESPONSIBLE_FOR_TEXT) + b':')
                for j, entry in enumerate(responsibilities):
                    width, _unused = terminal.get_size()
                    width -= 7
                    print(str(entry[0]).rjust(6), end=b' ')
                    print(b'...%s' % entry[1][-width + 3:] if len(entry[1]) > width else entry[1])
                    if j >= 9:
                        break

    def output_html(self):
        resp_xml = b'<div><div class="box" id="responsibilities">'
        resp_xml += b'<p>' + _(RESPONSIBILITIES_INFO_TEXT) + b'.</p>'
        for i in sorted(set(i[0] for i in blame.get(self.hard, self.useweeks, self.changes).blames)):
            responsibilities = sorted(((i[1], i[0]) for i in Responsibilities.get(self.hard, self.useweeks, i)), reverse=True)
            if responsibilities:
                resp_xml += b'<div>'
                if format.get_selected() == b'html':
                    author_email = self.changes.get_latest_email_by_author(i)
                    resp_xml += (b'<h3><img src="{0}"/>{1} {2}</h3>').format(gravatar.get_url(author_email, size=32), i, _(MOSTLY_RESPONSIBLE_FOR_TEXT))
                else:
                    resp_xml += (b'<h3>{0} {1}</h3>').format(i, _(MOSTLY_RESPONSIBLE_FOR_TEXT))
                for j, entry in enumerate(responsibilities):
                    resp_xml += b'<div' + (b' class="odd">' if j % 2 == 1 else b'>') + entry[1] + b' (' + str(entry[0]) + b' eloc)</div>'
                    if j >= 9:
                        break

                resp_xml += b'</div>'

        resp_xml += b'</div></div>'
        print(resp_xml)

    def output_xml(self):
        message_xml = b'\t\t<message>' + _(RESPONSIBILITIES_INFO_TEXT) + b'</message>\n'
        resp_xml = b''
        for i in sorted(set(i[0] for i in blame.get(self.hard, self.useweeks, self.changes).blames)):
            responsibilities = sorted(((i[1], i[0]) for i in Responsibilities.get(self.hard, self.useweeks, i)), reverse=True)
            if responsibilities:
                author_email = self.changes.get_latest_email_by_author(i)
                resp_xml += b'\t\t\t<author>\n'
                resp_xml += b'\t\t\t\t<name>' + i + b'</name>\n'
                resp_xml += b'\t\t\t\t<gravatar>' + gravatar.get_url(author_email) + b'</gravatar>\n'
                resp_xml += b'\t\t\t\t<files>\n'
                for j, entry in enumerate(responsibilities):
                    resp_xml += b'\t\t\t\t\t<file>\n'
                    resp_xml += b'\t\t\t\t\t\t<name>' + entry[1] + b'</name>\n'
                    resp_xml += b'\t\t\t\t\t\t<rows>' + str(entry[0]) + b'</rows>\n'
                    resp_xml += b'\t\t\t\t\t</file>\n'
                    if j >= 9:
                        break

                resp_xml += b'\t\t\t\t</files>\n'
                resp_xml += b'\t\t\t</author>\n'

        print(b'\t<responsibilities>\n' + message_xml + b'\t\t<authors>\n' + resp_xml + b'\t\t</authors>\n\t</responsibilities>')