# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/atulvarma/Documents/18f/django-uswds-forms/example/app/render_source.py
# Compiled at: 2017-05-12 10:02:32
# Size of source mod 2**32: 1723 bytes
import ast
from pathlib import Path
from django.utils.safestring import SafeString
try:
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from pygments.lexers.templates import HtmlDjangoLexer
    from pygments.formatters import HtmlFormatter
except ImportError:
    highlight = None

APP_DIR = Path(__file__).resolve().parent
PY_DIR = APP_DIR / 'examples'
TEMPLATES_DIR = APP_DIR / 'templates' / 'examples'

def render_source(contents, filetype):
    if highlight is None:
        return contents
    else:
        formatter = HtmlFormatter(noclasses=True, style='trac')
        if filetype == 'html+django':
            lexer = HtmlDjangoLexer()
        else:
            if filetype == 'python':
                lexer = PythonLexer()
            else:
                raise ValueError('unknown filetype: {}'.format(filetype))
        return SafeString(highlight(contents, lexer, formatter))


def clean_python_source(source):
    """
    Remove the leading docstring from the given source code.
    """
    mod = ast.parse(source)
    first_non_docstring = mod.body[1]
    return '\n'.join(source.splitlines()[first_non_docstring.lineno - 1:])


def clean_template_source(source):
    """
    Remove any un-indented {% include %} tags in the given template source.
    """
    return '\n'.join(line for line in source.splitlines() if not line.startswith('{% include'))


def render_template_source(filename):
    with open(str(TEMPLATES_DIR / filename)) as (f):
        return render_source(clean_template_source(f.read()), 'html+django')


def render_python_source(filename):
    with open(str(PY_DIR / filename)) as (f):
        return render_source(clean_python_source(f.read()), 'python')