# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/formatters/latex.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 17758 bytes
"""
    pygments.formatters.latex
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Formatter for LaTeX fancyvrb output.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from __future__ import division
from pygments.formatter import Formatter
from pygments.lexer import Lexer
from pygments.token import Token, STANDARD_TYPES
from pygments.util import get_bool_opt, get_int_opt, StringIO, xrange, iteritems
__all__ = [
 'LatexFormatter']

def escape_tex(text, commandprefix):
    return text.replace('\\', '\x00').replace('{', '\x01').replace('}', '\x02').replace('\x00', '\\%sZbs{}' % commandprefix).replace('\x01', '\\%sZob{}' % commandprefix).replace('\x02', '\\%sZcb{}' % commandprefix).replace('^', '\\%sZca{}' % commandprefix).replace('_', '\\%sZus{}' % commandprefix).replace('&', '\\%sZam{}' % commandprefix).replace('<', '\\%sZlt{}' % commandprefix).replace('>', '\\%sZgt{}' % commandprefix).replace('#', '\\%sZsh{}' % commandprefix).replace('%', '\\%sZpc{}' % commandprefix).replace('$', '\\%sZdl{}' % commandprefix).replace('-', '\\%sZhy{}' % commandprefix).replace("'", '\\%sZsq{}' % commandprefix).replace('"', '\\%sZdq{}' % commandprefix).replace('~', '\\%sZti{}' % commandprefix)


DOC_TEMPLATE = '\n\\documentclass{%(docclass)s}\n\\usepackage{fancyvrb}\n\\usepackage{color}\n\\usepackage[%(encoding)s]{inputenc}\n%(preamble)s\n\n%(styledefs)s\n\n\\begin{document}\n\n\\section*{%(title)s}\n\n%(code)s\n\\end{document}\n'
STYLE_TEMPLATE = '\n\\makeatletter\n\\def\\%(cp)s@reset{\\let\\%(cp)s@it=\\relax \\let\\%(cp)s@bf=\\relax%%\n    \\let\\%(cp)s@ul=\\relax \\let\\%(cp)s@tc=\\relax%%\n    \\let\\%(cp)s@bc=\\relax \\let\\%(cp)s@ff=\\relax}\n\\def\\%(cp)s@tok#1{\\csname %(cp)s@tok@#1\\endcsname}\n\\def\\%(cp)s@toks#1+{\\ifx\\relax#1\\empty\\else%%\n    \\%(cp)s@tok{#1}\\expandafter\\%(cp)s@toks\\fi}\n\\def\\%(cp)s@do#1{\\%(cp)s@bc{\\%(cp)s@tc{\\%(cp)s@ul{%%\n    \\%(cp)s@it{\\%(cp)s@bf{\\%(cp)s@ff{#1}}}}}}}\n\\def\\%(cp)s#1#2{\\%(cp)s@reset\\%(cp)s@toks#1+\\relax+\\%(cp)s@do{#2}}\n\n%(styles)s\n\n\\def\\%(cp)sZbs{\\char`\\\\}\n\\def\\%(cp)sZus{\\char`\\_}\n\\def\\%(cp)sZob{\\char`\\{}\n\\def\\%(cp)sZcb{\\char`\\}}\n\\def\\%(cp)sZca{\\char`\\^}\n\\def\\%(cp)sZam{\\char`\\&}\n\\def\\%(cp)sZlt{\\char`\\<}\n\\def\\%(cp)sZgt{\\char`\\>}\n\\def\\%(cp)sZsh{\\char`\\#}\n\\def\\%(cp)sZpc{\\char`\\%%}\n\\def\\%(cp)sZdl{\\char`\\$}\n\\def\\%(cp)sZhy{\\char`\\-}\n\\def\\%(cp)sZsq{\\char`\\\'}\n\\def\\%(cp)sZdq{\\char`\\"}\n\\def\\%(cp)sZti{\\char`\\~}\n%% for compatibility with earlier versions\n\\def\\%(cp)sZat{@}\n\\def\\%(cp)sZlb{[}\n\\def\\%(cp)sZrb{]}\n\\makeatother\n'

def _get_ttype_name(ttype):
    fname = STANDARD_TYPES.get(ttype)
    if fname:
        return fname
    else:
        aname = ''
        while fname is None:
            aname = ttype[(-1)] + aname
            ttype = ttype.parent
            fname = STANDARD_TYPES.get(ttype)

        return fname + aname


class LatexFormatter(Formatter):
    __doc__ = '\n    Format tokens as LaTeX code. This needs the `fancyvrb` and `color`\n    standard packages.\n\n    Without the `full` option, code is formatted as one ``Verbatim``\n    environment, like this:\n\n    .. sourcecode:: latex\n\n        \\begin{Verbatim}[commandchars=\\\\\\{\\}]\n        \\PY{k}{def }\\PY{n+nf}{foo}(\\PY{n}{bar}):\n            \\PY{k}{pass}\n        \\end{Verbatim}\n\n    The special command used here (``\\PY``) and all the other macros it needs\n    are output by the `get_style_defs` method.\n\n    With the `full` option, a complete LaTeX document is output, including\n    the command definitions in the preamble.\n\n    The `get_style_defs()` method of a `LatexFormatter` returns a string\n    containing ``\\def`` commands defining the macros needed inside the\n    ``Verbatim`` environments.\n\n    Additional options accepted:\n\n    `style`\n        The style to use, can be a string or a Style subclass (default:\n        ``\'default\'``).\n\n    `full`\n        Tells the formatter to output a "full" document, i.e. a complete\n        self-contained document (default: ``False``).\n\n    `title`\n        If `full` is true, the title that should be used to caption the\n        document (default: ``\'\'``).\n\n    `docclass`\n        If the `full` option is enabled, this is the document class to use\n        (default: ``\'article\'``).\n\n    `preamble`\n        If the `full` option is enabled, this can be further preamble commands,\n        e.g. ``\\usepackage`` (default: ``\'\'``).\n\n    `linenos`\n        If set to ``True``, output line numbers (default: ``False``).\n\n    `linenostart`\n        The line number for the first line (default: ``1``).\n\n    `linenostep`\n        If set to a number n > 1, only every nth line number is printed.\n\n    `verboptions`\n        Additional options given to the Verbatim environment (see the *fancyvrb*\n        docs for possible values) (default: ``\'\'``).\n\n    `commandprefix`\n        The LaTeX commands used to produce colored output are constructed\n        using this prefix and some letters (default: ``\'PY\'``).\n\n        .. versionadded:: 0.7\n        .. versionchanged:: 0.10\n           The default is now ``\'PY\'`` instead of ``\'C\'``.\n\n    `texcomments`\n        If set to ``True``, enables LaTeX comment lines.  That is, LaTex markup\n        in comment tokens is not escaped so that LaTeX can render it (default:\n        ``False``).\n\n        .. versionadded:: 1.2\n\n    `mathescape`\n        If set to ``True``, enables LaTeX math mode escape in comments. That\n        is, ``\'$...$\'`` inside a comment will trigger math mode (default:\n        ``False``).\n\n        .. versionadded:: 1.2\n\n    `escapeinside`\n        If set to a string of length 2, enables escaping to LaTeX. Text\n        delimited by these 2 characters is read as LaTeX code and\n        typeset accordingly. It has no effect in string literals. It has\n        no effect in comments if `texcomments` or `mathescape` is\n        set. (default: ``\'\'``).\n\n        .. versionadded:: 2.0\n\n    `envname`\n        Allows you to pick an alternative environment name replacing Verbatim.\n        The alternate environment still has to support Verbatim\'s option syntax.\n        (default: ``\'Verbatim\'``).\n\n        .. versionadded:: 2.0\n    '
    name = 'LaTeX'
    aliases = ['latex', 'tex']
    filenames = ['*.tex']

    def __init__(self, **options):
        (Formatter.__init__)(self, **options)
        self.docclass = options.get('docclass', 'article')
        self.preamble = options.get('preamble', '')
        self.linenos = get_bool_opt(options, 'linenos', False)
        self.linenostart = abs(get_int_opt(options, 'linenostart', 1))
        self.linenostep = abs(get_int_opt(options, 'linenostep', 1))
        self.verboptions = options.get('verboptions', '')
        self.nobackground = get_bool_opt(options, 'nobackground', False)
        self.commandprefix = options.get('commandprefix', 'PY')
        self.texcomments = get_bool_opt(options, 'texcomments', False)
        self.mathescape = get_bool_opt(options, 'mathescape', False)
        self.escapeinside = options.get('escapeinside', '')
        if len(self.escapeinside) == 2:
            self.left = self.escapeinside[0]
            self.right = self.escapeinside[1]
        else:
            self.escapeinside = ''
        self.envname = options.get('envname', 'Verbatim')
        self._create_stylesheet()

    def _create_stylesheet(self):
        t2n = self.ttype2name = {Token: ''}
        c2d = self.cmd2def = {}
        cp = self.commandprefix

        def rgbcolor(col):
            if col:
                return ','.join(['%.2f' % (int(col[i] + col[(i + 1)], 16) / 255.0) for i in (0,
                                                                                             2,
                                                                                             4)])
            else:
                return '1,1,1'

        for ttype, ndef in self.style:
            name = _get_ttype_name(ttype)
            cmndef = ''
            if ndef['bold']:
                cmndef += '\\let\\$$@bf=\\textbf'
            if ndef['italic']:
                cmndef += '\\let\\$$@it=\\textit'
            if ndef['underline']:
                cmndef += '\\let\\$$@ul=\\underline'
            if ndef['roman']:
                cmndef += '\\let\\$$@ff=\\textrm'
            if ndef['sans']:
                cmndef += '\\let\\$$@ff=\\textsf'
            if ndef['mono']:
                cmndef += '\\let\\$$@ff=\\textsf'
            if ndef['color']:
                cmndef += '\\def\\$$@tc##1{\\textcolor[rgb]{%s}{##1}}' % rgbcolor(ndef['color'])
            if ndef['border']:
                cmndef += '\\def\\$$@bc##1{\\setlength{\\fboxsep}{0pt}\\fcolorbox[rgb]{%s}{%s}{\\strut ##1}}' % (
                 rgbcolor(ndef['border']),
                 rgbcolor(ndef['bgcolor']))
            else:
                if ndef['bgcolor']:
                    cmndef += '\\def\\$$@bc##1{\\setlength{\\fboxsep}{0pt}\\colorbox[rgb]{%s}{\\strut ##1}}' % rgbcolor(ndef['bgcolor'])
            if cmndef == '':
                pass
            else:
                cmndef = cmndef.replace('$$', cp)
                t2n[ttype] = name
                c2d[name] = cmndef

    def get_style_defs(self, arg=''):
        """
        Return the command sequences needed to define the commands
        used to format text in the verbatim environment. ``arg`` is ignored.
        """
        cp = self.commandprefix
        styles = []
        for name, definition in iteritems(self.cmd2def):
            styles.append('\\expandafter\\def\\csname %s@tok@%s\\endcsname{%s}' % (
             cp, name, definition))

        return STYLE_TEMPLATE % {'cp':self.commandprefix,  'styles':'\n'.join(styles)}

    def format_unencoded(self, tokensource, outfile):
        t2n = self.ttype2name
        cp = self.commandprefix
        if self.full:
            realoutfile = outfile
            outfile = StringIO()
        outfile.write('\\begin{' + self.envname + '}[commandchars=\\\\\\{\\}')
        if self.linenos:
            start, step = self.linenostart, self.linenostep
            outfile.write(',numbers=left' + (start and ',firstnumber=%d' % start or '') + (step and ',stepnumber=%d' % step or ''))
        if self.mathescape or self.texcomments or self.escapeinside:
            outfile.write(',codes={\\catcode`\\$=3\\catcode`\\^=7\\catcode`\\_=8}')
        if self.verboptions:
            outfile.write(',' + self.verboptions)
        outfile.write(']\n')
        for ttype, value in tokensource:
            if ttype in Token.Comment:
                if self.texcomments:
                    start = value[0:1]
                    for i in xrange(1, len(value)):
                        if start[0] != value[i]:
                            break
                        start += value[i]

                    value = value[len(start):]
                    start = escape_tex(start, cp)
                    value = start + value
                else:
                    if self.mathescape:
                        parts = value.split('$')
                        in_math = False
                        for i, part in enumerate(parts):
                            if not in_math:
                                parts[i] = escape_tex(part, cp)
                            in_math = not in_math

                        value = '$'.join(parts)
                    else:
                        if self.escapeinside:
                            text = value
                            value = ''
                            while text:
                                a, sep1, text = text.partition(self.left)
                                if sep1:
                                    b, sep2, text = text.partition(self.right)
                                    if sep2:
                                        value += escape_tex(a, cp) + b
                                    else:
                                        value += escape_tex(a + sep1 + b, cp)
                                else:
                                    value += escape_tex(a, cp)

                        else:
                            value = escape_tex(value, cp)
            elif ttype not in Token.Escape:
                value = escape_tex(value, cp)
            else:
                styles = []
                while ttype is not Token:
                    try:
                        styles.append(t2n[ttype])
                    except KeyError:
                        styles.append(_get_ttype_name(ttype))

                    ttype = ttype.parent

                styleval = '+'.join(reversed(styles))
                if styleval:
                    spl = value.split('\n')
                    for line in spl[:-1]:
                        if line:
                            outfile.write('\\%s{%s}{%s}' % (cp, styleval, line))
                        outfile.write('\n')

                    if spl[(-1)]:
                        outfile.write('\\%s{%s}{%s}' % (cp, styleval, spl[(-1)]))
                else:
                    outfile.write(value)

        outfile.write('\\end{' + self.envname + '}\n')
        if self.full:
            encoding = self.encoding or 'utf8'
            encoding = {'utf_8':'utf8', 
             'latin_1':'latin1', 
             'iso_8859_1':'latin1'}.get(encoding.replace('-', '_'), encoding)
            realoutfile.write(DOC_TEMPLATE % dict(docclass=(self.docclass), preamble=(self.preamble),
              title=(self.title),
              encoding=encoding,
              styledefs=(self.get_style_defs()),
              code=(outfile.getvalue())))


class LatexEmbeddedLexer(Lexer):
    __doc__ = '\n    This lexer takes one lexer as argument, the lexer for the language\n    being formatted, and the left and right delimiters for escaped text.\n\n    First everything is scanned using the language lexer to obtain\n    strings and comments. All other consecutive tokens are merged and\n    the resulting text is scanned for escaped segments, which are given\n    the Token.Escape type. Finally text that is not escaped is scanned\n    again with the language lexer.\n    '

    def __init__(self, left, right, lang, **options):
        self.left = left
        self.right = right
        self.lang = lang
        (Lexer.__init__)(self, **options)

    def get_tokens_unprocessed(self, text):
        buf = ''
        idx = 0
        for i, t, v in self.lang.get_tokens_unprocessed(text):
            if t in Token.Comment or t in Token.String:
                if buf:
                    for x in self.get_tokens_aux(idx, buf):
                        yield x

                    buf = ''
                yield (
                 i, t, v)
            else:
                if not buf:
                    idx = i
                buf += v

        if buf:
            for x in self.get_tokens_aux(idx, buf):
                yield x

    def get_tokens_aux(self, index, text):
        while text:
            a, sep1, text = text.partition(self.left)
            if a:
                for i, t, v in self.lang.get_tokens_unprocessed(a):
                    yield (
                     index + i, t, v)
                    index += len(a)

            if sep1:
                b, sep2, text = text.partition(self.right)
                if sep2:
                    yield (
                     index + len(sep1), Token.Escape, b)
                    index += len(sep1) + len(b) + len(sep2)
                else:
                    yield (
                     index, Token.Error, sep1)
                    index += len(sep1)
                    text = b