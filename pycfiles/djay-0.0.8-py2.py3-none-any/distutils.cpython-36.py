# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/readme-renderer/readme_renderer/integration/distutils.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 3582 bytes
from __future__ import absolute_import, division, print_function
import cgi, io, re, distutils.log
from distutils.command.check import check as _check
from distutils.core import Command
import six
from ..rst import render
_REPORT_RE = re.compile('^<string>:(?P<line>(?:\\d+)?): \\((?P<level>DEBUG|INFO|WARNING|ERROR|SEVERE)/(\\d+)?\\) (?P<message>.*)', re.DOTALL | re.MULTILINE)

@six.python_2_unicode_compatible
class _WarningStream(object):

    def __init__(self):
        self.output = io.StringIO()

    def write(self, text):
        matched = _REPORT_RE.search(text)
        if not matched:
            self.output.write(text)
            return
        self.output.write('line {line}: {level_text}: {message}\n'.format(level_text=(matched.group('level').capitalize()),
          line=(matched.group('line')),
          message=(matched.group('message').rstrip('\r\n'))))

    def __str__(self):
        return self.output.getvalue()


class Check(_check):

    def check_restructuredtext(self):
        """
        Checks if the long string fields are reST-compliant.
        """
        Command.warn(self, 'This command has been deprecated. Use `twine check` instead: https://packaging.python.org/guides/making-a-pypi-friendly-readme#validating-restructuredtext-markup')
        data = self.distribution.get_long_description()
        content_type = getattr(self.distribution.metadata, 'long_description_content_type', None)
        if content_type:
            content_type, _ = cgi.parse_header(content_type)
            if content_type != 'text/x-rst':
                self.warn("Not checking long description content type '%s', this command only checks 'text/x-rst'." % content_type)
                return
        if not data or data == 'UNKNOWN':
            self.warn("The project's long_description is either missing or empty.")
            return
        stream = _WarningStream()
        markup = render(data, stream=stream)
        if markup is None:
            self.warn("The project's long_description has invalid markup which will not be rendered on PyPI. The following syntax errors were detected:\n%s" % stream)
            return
        self.announce("The project's long description is valid RST.",
          level=(distutils.log.INFO))