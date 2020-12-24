# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/formatters/latex.py
# Compiled at: 2011-04-22 17:53:24
"""
    pygments.formatters.latex
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Formatter for LaTeX fancyvrb output.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.formatter import Formatter
from pygments.token import Token, STANDARD_TYPES
from pygments.util import get_bool_opt, get_int_opt, StringIO
__all__ = [
 'LatexFormatter']

def escape_tex(text, commandprefix):
    return text.replace('\\', '\x00').replace('{', '\x01').replace('}', '\x02').replace('\x00', '\\%sZbs{}' % commandprefix).replace('\x01', '\\%sZob{}' % commandprefix).replace('\x02', '\\%sZcb{}' % commandprefix).replace('^', '\\%sZca{}' % commandprefix).replace('_', '\\%sZus{}' % commandprefix).replace('#', '\\%sZsh{}' % commandprefix).replace('%', '\\%sZpc{}' % commandprefix).replace('$', '\\%sZdl{}' % commandprefix).replace('~', '\\%sZti{}' % commandprefix)


DOC_TEMPLATE = '\n\\documentclass{%(docclass)s}\n\\usepackage{fancyvrb}\n\\usepackage{color}\n\\usepackage[%(encoding)s]{inputenc}\n%(preamble)s\n\n%(styledefs)s\n\n\\begin{document}\n\n\\section*{%(title)s}\n\n%(code)s\n\\end{document}\n'
STYLE_TEMPLATE = '\n\\makeatletter\n\\def\\%(cp)s@reset{\\let\\%(cp)s@it=\\relax \\let\\%(cp)s@bf=\\relax%%\n    \\let\\%(cp)s@ul=\\relax \\let\\%(cp)s@tc=\\relax%%\n    \\let\\%(cp)s@bc=\\relax \\let\\%(cp)s@ff=\\relax}\n\\def\\%(cp)s@tok#1{\\csname %(cp)s@tok@#1\\endcsname}\n\\def\\%(cp)s@toks#1+{\\ifx\\relax#1\\empty\\else%%\n    \\%(cp)s@tok{#1}\\expandafter\\%(cp)s@toks\\fi}\n\\def\\%(cp)s@do#1{\\%(cp)s@bc{\\%(cp)s@tc{\\%(cp)s@ul{%%\n    \\%(cp)s@it{\\%(cp)s@bf{\\%(cp)s@ff{#1}}}}}}}\n\\def\\%(cp)s#1#2{\\%(cp)s@reset\\%(cp)s@toks#1+\\relax+\\%(cp)s@do{#2}}\n\n%(styles)s\n\n\\def\\%(cp)sZbs{\\char`\\\\}\n\\def\\%(cp)sZus{\\char`\\_}\n\\def\\%(cp)sZob{\\char`\\{}\n\\def\\%(cp)sZcb{\\char`\\}}\n\\def\\%(cp)sZca{\\char`\\^}\n\\def\\%(cp)sZsh{\\char`\\#}\n\\def\\%(cp)sZpc{\\char`\\%%}\n\\def\\%(cp)sZdl{\\char`\\$}\n\\def\\%(cp)sZti{\\char`\\~}\n%% for compatibility with earlier versions\n\\def\\%(cp)sZat{@}\n\\def\\%(cp)sZlb{[}\n\\def\\%(cp)sZrb{]}\n\\makeatother\n'

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
    r"""
    Format tokens as LaTeX code. This needs the `fancyvrb` and `color`
    standard packages.

    Without the `full` option, code is formatted as one ``Verbatim``
    environment, like this:

    .. sourcecode:: latex

        \begin{Verbatim}[commandchars=\\{\}]
        \PY{k}{def }\PY{n+nf}{foo}(\PY{n}{bar}):
            \PY{k}{pass}
        \end{Verbatim}

    The special command used here (``\PY``) and all the other macros it needs
    are output by the `get_style_defs` method.

    With the `full` option, a complete LaTeX document is output, including
    the command definitions in the preamble.

    The `get_style_defs()` method of a `LatexFormatter` returns a string
    containing ``\def`` commands defining the macros needed inside the
    ``Verbatim`` environments.

    Additional options accepted:

    `style`
        The style to use, can be a string or a Style subclass (default:
        ``'default'``).

    `full`
        Tells the formatter to output a "full" document, i.e. a complete
        self-contained document (default: ``False``).

    `title`
        If `full` is true, the title that should be used to caption the
        document (default: ``''``).

    `docclass`
        If the `full` option is enabled, this is the document class to use
        (default: ``'article'``).

    `preamble`
        If the `full` option is enabled, this can be further preamble commands,
        e.g. ``\usepackage`` (default: ``''``).

    `linenos`
        If set to ``True``, output line numbers (default: ``False``).

    `linenostart`
        The line number for the first line (default: ``1``).

    `linenostep`
        If set to a number n > 1, only every nth line number is printed.

    `verboptions`
        Additional options given to the Verbatim environment (see the *fancyvrb*
        docs for possible values) (default: ``''``).

    `commandprefix`
        The LaTeX commands used to produce colored output are constructed
        using this prefix and some letters (default: ``'PY'``).
        *New in Pygments 0.7.*

        *New in Pygments 0.10:* the default is now ``'PY'`` instead of ``'C'``.

    `texcomments`
        If set to ``True``, enables LaTeX comment lines.  That is, LaTex markup
        in comment tokens is not escaped so that LaTeX can render it (default:
        ``False``).  *New in Pygments 1.2.*

    `mathescape`
        If set to ``True``, enables LaTeX math mode escape in comments. That
        is, ``'$...$'`` inside a comment will trigger math mode (default:
        ``False``).  *New in Pygments 1.2.*
    """
    name = 'LaTeX'
    aliases = ['latex', 'tex']
    filenames = ['*.tex']

    def __init__(self, **options):
        Formatter.__init__(self, **options)
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
        self._create_stylesheet()

    def _create_stylesheet(self):
        t2n = self.ttype2name = {Token: ''}
        c2d = self.cmd2def = {}
        cp = self.commandprefix

        def rgbcolor(col):
            if col:
                return (',').join([ '%.2f' % (int(col[i] + col[(i + 1)], 16) / 255.0) for i in (0,
                                                                                                2,
                                                                                                4)
                                  ])
            else:
                return '1,1,1'

        for (ttype, ndef) in self.style:
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
                cmndef += '\\def\\$$@bc##1{\\fcolorbox[rgb]{%s}{%s}{##1}}' % (
                 rgbcolor(ndef['border']),
                 rgbcolor(ndef['bgcolor']))
            elif ndef['bgcolor']:
                cmndef += '\\def\\$$@bc##1{\\colorbox[rgb]{%s}{##1}}' % rgbcolor(ndef['bgcolor'])
            if cmndef == '':
                continue
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
        for (name, definition) in self.cmd2def.iteritems():
            styles.append('\\def\\%s@tok@%s{%s}' % (cp, name, definition))

        return STYLE_TEMPLATE % {'cp': self.commandprefix, 'styles': ('\n').join(styles)}

    def format_unencoded(self, tokensource, outfile):
        t2n = self.ttype2name
        cp = self.commandprefix
        if self.full:
            realoutfile = outfile
            outfile = StringIO()
        outfile.write('\\begin{Verbatim}[commandchars=\\\\\\{\\}')
        if self.linenos:
            start, step = self.linenostart, self.linenostep
            outfile.write(',numbers=left' + (start and ',firstnumber=%d' % start or '') + (step and ',stepnumber=%d' % step or ''))
        if self.mathescape or self.texcomments:
            outfile.write(',codes={\\catcode`\\$=3\\catcode`\\^=7\\catcode`\\_=8}')
        if self.verboptions:
            outfile.write(',' + self.verboptions)
        outfile.write(']\n')
        for (ttype, value) in tokensource:
            if ttype in Token.Comment:
                if self.texcomments:
                    start = value[0:1]
                    for i in xrange(1, len(value)):
                        if start[0] != value[i]:
                            break
                        start += value[i]

                    value = value[len(start):]
                    start = escape_tex(start, self.commandprefix)
                    value = start + value
                elif self.mathescape:
                    parts = value.split('$')
                    in_math = False
                    for (i, part) in enumerate(parts):
                        if not in_math:
                            parts[i] = escape_tex(part, self.commandprefix)
                        in_math = not in_math

                    value = ('$').join(parts)
                else:
                    value = escape_tex(value, self.commandprefix)
            else:
                value = escape_tex(value, self.commandprefix)
            styles = []
            while ttype is not Token:
                try:
                    styles.append(t2n[ttype])
                except KeyError:
                    styles.append(_get_ttype_name(ttype))

                ttype = ttype.parent

            styleval = ('+').join(reversed(styles))
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

        outfile.write('\\end{Verbatim}\n')
        if self.full:
            realoutfile.write(DOC_TEMPLATE % dict(docclass=self.docclass, preamble=self.preamble, title=self.title, encoding=self.encoding or 'latin1', styledefs=self.get_style_defs(), code=outfile.getvalue()))