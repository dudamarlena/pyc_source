# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/utils/translation/template.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
import re, warnings
from django.template.base import TOKEN_BLOCK, TOKEN_COMMENT, TOKEN_TEXT, TOKEN_VAR, TRANSLATOR_COMMENT_MARK, Lexer
from django.utils import six
from django.utils.encoding import force_text
from django.utils.six import StringIO
from . import TranslatorCommentWarning, trim_whitespace
dot_re = re.compile(b'\\S')

def blankout(src, char):
    """
    Change every non-whitespace character to the given char.
    Used in the templatize function.
    """
    return dot_re.sub(char, src)


context_re = re.compile(b'^\\s+.*context\\s+((?:"[^"]*?")|(?:\'[^\']*?\'))\\s*')
inline_re = re.compile(b'^\\s*trans\\s+((?:"[^"]*?")|(?:\'[^\']*?\'))(?:\\s*\\|\\s*[^\\s:]+(?::(?:[^\\s\'":]+|(?:"[^"]*?")|(?:\'[^\']*?\')))?)*(\\s+.*context\\s+((?:"[^"]*?")|(?:\'[^\']*?\')))?\\s*')
block_re = re.compile(b'^\\s*blocktrans(\\s+.*context\\s+((?:"[^"]*?")|(?:\'[^\']*?\')))?(?:\\s+|$)')
endblock_re = re.compile(b'^\\s*endblocktrans$')
plural_re = re.compile(b'^\\s*plural$')
constant_re = re.compile(b'_\\(((?:".*?")|(?:\'.*?\'))\\)')

def templatize(src, origin=None, charset=b'utf-8'):
    """
    Turn a Django template into something that is understood by xgettext. It
    does so by translating the Django translation tags into standard gettext
    function invocations.
    """
    src = force_text(src, charset)
    out = StringIO(b'')
    message_context = None
    intrans = False
    inplural = False
    trimmed = False
    singular = []
    plural = []
    incomment = False
    comment = []
    lineno_comment_map = {}
    comment_lineno_cache = None
    raw_prefix = b'u' if six.PY3 else b''

    def join_tokens(tokens, trim=False):
        message = (b'').join(tokens)
        if trim:
            message = trim_whitespace(message)
        return message

    for t in Lexer(src).tokenize():
        if incomment:
            if t.token_type == TOKEN_BLOCK and t.contents == b'endcomment':
                content = (b'').join(comment)
                translators_comment_start = None
                for lineno, line in enumerate(content.splitlines(True)):
                    if line.lstrip().startswith(TRANSLATOR_COMMENT_MARK):
                        translators_comment_start = lineno

                for lineno, line in enumerate(content.splitlines(True)):
                    if translators_comment_start is not None and lineno >= translators_comment_start:
                        out.write(b' # %s' % line)
                    else:
                        out.write(b' #\n')

                incomment = False
                comment = []
            else:
                comment.append(t.contents)
        elif intrans:
            if t.token_type == TOKEN_BLOCK:
                endbmatch = endblock_re.match(t.contents)
                pluralmatch = plural_re.match(t.contents)
                if endbmatch:
                    if inplural:
                        if message_context:
                            out.write((b' npgettext({p}{!r}, {p}{!r}, {p}{!r},count) ').format(message_context, join_tokens(singular, trimmed), join_tokens(plural, trimmed), p=raw_prefix))
                        else:
                            out.write((b' ngettext({p}{!r}, {p}{!r}, count) ').format(join_tokens(singular, trimmed), join_tokens(plural, trimmed), p=raw_prefix))
                        for part in singular:
                            out.write(blankout(part, b'S'))

                        for part in plural:
                            out.write(blankout(part, b'P'))

                    else:
                        if message_context:
                            out.write((b' pgettext({p}{!r}, {p}{!r}) ').format(message_context, join_tokens(singular, trimmed), p=raw_prefix))
                        else:
                            out.write((b' gettext({p}{!r}) ').format(join_tokens(singular, trimmed), p=raw_prefix))
                        for part in singular:
                            out.write(blankout(part, b'S'))

                    message_context = None
                    intrans = False
                    inplural = False
                    singular = []
                    plural = []
                elif pluralmatch:
                    inplural = True
                else:
                    filemsg = b''
                    if origin:
                        filemsg = b'file %s, ' % origin
                    raise SyntaxError(b'Translation blocks must not include other block tags: %s (%sline %d)' % (
                     t.contents, filemsg, t.lineno))
            elif t.token_type == TOKEN_VAR:
                if inplural:
                    plural.append(b'%%(%s)s' % t.contents)
                else:
                    singular.append(b'%%(%s)s' % t.contents)
            elif t.token_type == TOKEN_TEXT:
                contents = t.contents.replace(b'%', b'%%')
                if inplural:
                    plural.append(contents)
                else:
                    singular.append(contents)
        else:
            if comment_lineno_cache is not None:
                cur_lineno = t.lineno + t.contents.count(b'\n')
                if comment_lineno_cache == cur_lineno:
                    if t.token_type != TOKEN_COMMENT:
                        for c in lineno_comment_map[comment_lineno_cache]:
                            filemsg = b''
                            if origin:
                                filemsg = b'file %s, ' % origin
                            warn_msg = b"The translator-targeted comment '%s' (%sline %d) was ignored, because it wasn't the last item on the line." % (
                             c, filemsg, comment_lineno_cache)
                            warnings.warn(warn_msg, TranslatorCommentWarning)

                        lineno_comment_map[comment_lineno_cache] = []
                else:
                    out.write(b'# %s' % (b' | ').join(lineno_comment_map[comment_lineno_cache]))
                comment_lineno_cache = None
            if t.token_type == TOKEN_BLOCK:
                imatch = inline_re.match(t.contents)
                bmatch = block_re.match(t.contents)
                cmatches = constant_re.findall(t.contents)
                if imatch:
                    g = imatch.group(1)
                    if g[0] == b'"':
                        g = g.strip(b'"')
                    elif g[0] == b"'":
                        g = g.strip(b"'")
                    g = g.replace(b'%', b'%%')
                    if imatch.group(2):
                        context_match = context_re.match(imatch.group(2))
                        message_context = context_match.group(1)
                        if message_context[0] == b'"':
                            message_context = message_context.strip(b'"')
                        elif message_context[0] == b"'":
                            message_context = message_context.strip(b"'")
                        out.write((b' pgettext({p}{!r}, {p}{!r}) ').format(message_context, g, p=raw_prefix))
                        message_context = None
                    else:
                        out.write((b' gettext({p}{!r}) ').format(g, p=raw_prefix))
                elif bmatch:
                    for fmatch in constant_re.findall(t.contents):
                        out.write(b' _(%s) ' % fmatch)

                    if bmatch.group(1):
                        context_match = context_re.match(bmatch.group(1))
                        message_context = context_match.group(1)
                        if message_context[0] == b'"':
                            message_context = message_context.strip(b'"')
                        elif message_context[0] == b"'":
                            message_context = message_context.strip(b"'")
                    intrans = True
                    inplural = False
                    trimmed = b'trimmed' in t.split_contents()
                    singular = []
                    plural = []
                elif cmatches:
                    for cmatch in cmatches:
                        out.write(b' _(%s) ' % cmatch)

                elif t.contents == b'comment':
                    incomment = True
                else:
                    out.write(blankout(t.contents, b'B'))
            elif t.token_type == TOKEN_VAR:
                parts = t.contents.split(b'|')
                cmatch = constant_re.match(parts[0])
                if cmatch:
                    out.write(b' _(%s) ' % cmatch.group(1))
                for p in parts[1:]:
                    if p.find(b':_(') >= 0:
                        out.write(b' %s ' % p.split(b':', 1)[1])
                    else:
                        out.write(blankout(p, b'F'))

            elif t.token_type == TOKEN_COMMENT:
                if t.contents.lstrip().startswith(TRANSLATOR_COMMENT_MARK):
                    lineno_comment_map.setdefault(t.lineno, []).append(t.contents)
                    comment_lineno_cache = t.lineno
            else:
                out.write(blankout(t.contents, b'X'))

    return out.getvalue()