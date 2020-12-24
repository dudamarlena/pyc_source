# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/twine/twine/commands/check.py
# Compiled at: 2019-07-30 18:47:10
# Size of source mod 2**32: 4176 bytes
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals
import argparse, cgi, re, sys
from io import StringIO
import readme_renderer.rst
from twine.commands import _find_dists
from twine.package import PackageFile
_RENDERERS = {None:readme_renderer.rst, 
 'text/plain':None, 
 'text/x-rst':readme_renderer.rst, 
 'text/markdown':None}
_REPORT_RE = re.compile('^<string>:(?P<line>(?:\\d+)?): \\((?P<level>DEBUG|INFO|WARNING|ERROR|SEVERE)/(\\d+)?\\) (?P<message>.*)', re.DOTALL | re.MULTILINE)

class _WarningStream(object):

    def __init__(self):
        self.output = StringIO()

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


def check(dists, output_stream=sys.stdout):
    uploads = [i for i in _find_dists(dists) if not i.endswith('.asc')]
    stream = _WarningStream()
    failure = False
    for filename in uploads:
        output_stream.write('Checking distribution %s: ' % filename)
        package = PackageFile.from_filename(filename, comment=None)
        metadata = package.metadata_dictionary()
        description = metadata['description']
        description_content_type = metadata['description_content_type']
        if description_content_type is None:
            output_stream.write('warning: `long_description_content_type` missing.  defaulting to `text/x-rst`.\n')
            description_content_type = 'text/x-rst'
        content_type, params = cgi.parse_header(description_content_type)
        renderer = _RENDERERS.get(content_type, _RENDERERS[None])
        if description in frozenset({None, 'UNKNOWN\n\n\n'}):
            output_stream.write('warning: `long_description` missing.\n')
            output_stream.write('Passed\n')
        elif renderer and (renderer.render)(description, stream=stream, **params) is None:
            failure = True
            output_stream.write('Failed\n')
            output_stream.write("The project's long_description has invalid markup which will not be rendered on PyPI. The following syntax errors were detected:\n%s" % stream)
        else:
            output_stream.write('Passed\n')

    return failure


def main(args):
    parser = argparse.ArgumentParser(prog='twine check')
    parser.add_argument('dists',
      nargs='+',
      metavar='dist',
      help='The distribution files to check, usually dist/*')
    args = parser.parse_args(args)
    return check(args.dists)