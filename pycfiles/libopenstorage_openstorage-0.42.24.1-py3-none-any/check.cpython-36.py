# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/twine/twine/commands/check.py
# Compiled at: 2020-01-10 16:25:25
# Size of source mod 2**32: 4980 bytes
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

class _WarningStream:

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


def _check_file(filename, render_warning_stream):
    """Check given distribution."""
    warnings = []
    is_ok = True
    package = PackageFile.from_filename(filename, comment=None)
    metadata = package.metadata_dictionary()
    description = metadata['description']
    description_content_type = metadata['description_content_type']
    if description_content_type is None:
        warnings.append('`long_description_content_type` missing.  defaulting to `text/x-rst`.')
        description_content_type = 'text/x-rst'
    content_type, params = cgi.parse_header(description_content_type)
    renderer = _RENDERERS.get(content_type, _RENDERERS[None])
    if description in frozenset({None, 'UNKNOWN\n\n\n'}):
        warnings.append('`long_description` missing.')
    else:
        if renderer:
            rendering_result = (renderer.render)(description, stream=render_warning_stream, **params)
            if rendering_result is None:
                is_ok = False
    return (
     warnings, is_ok)


def _indented(text, prefix):
    """Adds 'prefix' to all non-empty lines on 'text'."""

    def prefixed_lines():
        for line in text.splitlines(True):
            yield prefix + line if line.strip() else line

    return ''.join(prefixed_lines())


def check(dists, output_stream=sys.stdout):
    uploads = [i for i in _find_dists(dists) if not i.endswith('.asc')]
    if not uploads:
        output_stream.write('No files to check.\n')
        return False
    else:
        failure = False
        for filename in uploads:
            output_stream.write('Checking %s: ' % filename)
            render_warning_stream = _WarningStream()
            warnings, is_ok = _check_file(filename, render_warning_stream)
            if not is_ok:
                failure = True
                output_stream.write('FAILED\n')
                error_text = '`long_description` has syntax errors in markup and would not be rendered on PyPI.\n'
                output_stream.write(_indented(error_text, '  '))
                output_stream.write(_indented(str(render_warning_stream), '    '))
            else:
                if warnings:
                    output_stream.write('PASSED, with warnings\n')
                else:
                    output_stream.write('PASSED\n')
            for message in warnings:
                output_stream.write('  warning: ' + message + '\n')

        return failure


def main(args):
    parser = argparse.ArgumentParser(prog='twine check')
    parser.add_argument('dists',
      nargs='+',
      metavar='dist',
      help='The distribution files to check, usually dist/*')
    args = parser.parse_args(args)
    return check(args.dists)