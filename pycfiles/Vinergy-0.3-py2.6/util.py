# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/vinergy/util.py
# Compiled at: 2011-06-12 16:39:36
"""
  vinergy.util
  ~~~~~~~~~~~~

  Handy tools for Vinergy.
"""
__all__ = [
 'guess_ext',
 'is_termua',
 'new_name',
 'render',
 'response']
import web, string, random, mimetypes, pygments.lexers
from pygments import formatters
from pygments import highlight
from pygments.lexers import guess_lexer

def guess_ext(code):
    """Guess file ext with code"""
    lexer = guess_lexer(code)
    mime = lexer.mimetypes[0]
    ext = mimetypes.guess_extension(mime)[1:]
    return ext


def is_termua(ua):
    """Determine the given UA is of terminal or not"""
    ua = ua.lower()
    term_ua = ('wget', 'curl')
    for tua in term_ua:
        if ua.find(tua) != -1:
            return True

    return False


def new_name():
    """Generate new code name"""
    name = ''
    symbols = string.letters + string.digits
    while len(name) < 5:
        n = random.randint(0, len(symbols) - 1)
        name = name + symbols[n:n + 1]

    return name


def render(code, formatter, syntax):
    """Render code with pygments"""
    if not syntax:
        lexer = guess_lexer(code)
    syntax = syntax.lower()
    try:
        lexer = pygments.lexers.get_lexer_by_name(syntax)
    except:
        lexer = pygments.lexers.TextLexer()

    f = getattr(formatters, formatter)
    if f.__name__ == 'HtmlFormatter':
        newcode = highlight(code, lexer, f(full=True, style='manni', lineanchors='n', linenos='table', encoding='utf-8'))
    else:
        newcode = highlight(code, lexer, f())
    return newcode


def response(data, status='200 OK', headers=None):
    """Return custom response"""
    if not headers:
        headers = {'Content-Type': 'text/plain'}
    response = web.webapi.HTTPError(status, headers, data)
    return response