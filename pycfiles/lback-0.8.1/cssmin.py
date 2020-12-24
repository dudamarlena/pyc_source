# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mdipierro/make_web2py/web2py/gluon/contrib/minify/cssmin.py
# Compiled at: 2013-10-14 11:16:24
"""`cssmin` - A Python port of the YUI CSS compressor."""
from StringIO import StringIO
import re
__version__ = '0.1.4'

def remove_comments(css):
    """Remove all CSS comment blocks."""
    iemac = False
    preserve = False
    comment_start = css.find('/*')
    while comment_start >= 0:
        preserve = css[comment_start + 2:comment_start + 3] == '!'
        comment_end = css.find('*/', comment_start + 2)
        if comment_end < 0:
            if not preserve:
                css = css[:comment_start]
                break
        elif comment_end >= comment_start + 2:
            if css[(comment_end - 1)] == '\\':
                comment_start = comment_end + 2
                iemac = True
            elif iemac:
                comment_start = comment_end + 2
                iemac = False
            elif not preserve:
                css = css[:comment_start] + css[comment_end + 2:]
            else:
                comment_start = comment_end + 2
        comment_start = css.find('/*', comment_start)

    return css


def remove_unnecessary_whitespace(css):
    """Remove unnecessary whitespace characters."""

    def pseudoclasscolon(css):
        """
        Prevents 'p :link' from becoming 'p:link'.

        Translates 'p :link' into 'p ___PSEUDOCLASSCOLON___link'; this is
        translated back again later.
        """
        regex = re.compile('(^|\\})(([^\\{\\:])+\\:)+([^\\{]*\\{)')
        match = regex.search(css)
        while match:
            css = ('').join([
             css[:match.start()],
             match.group().replace(':', '___PSEUDOCLASSCOLON___'),
             css[match.end():]])
            match = regex.search(css)

        return css

    css = pseudoclasscolon(css)
    css = re.sub('\\s+([!{};:>+\\(\\)\\],])', '\\1', css)
    css = re.sub('^(.*)(@charset \\"[^\\"]*\\";)', '\\2\\1', css)
    css = re.sub('^(\\s*@charset [^;]+;\\s*)+', '\\1', css)
    css = re.sub('\\band\\(', 'and (', css)
    css = css.replace('___PSEUDOCLASSCOLON___', ':')
    css = re.sub('([!{}:;>+\\(\\[,])\\s+', '\\1', css)
    return css


def remove_unnecessary_semicolons(css):
    """Remove unnecessary semicolons."""
    return re.sub(';+\\}', '}', css)


def remove_empty_rules(css):
    """Remove empty rules."""
    return re.sub('[^\\}\\{]+\\{\\}', '', css)


def normalize_rgb_colors_to_hex(css):
    """Convert `rgb(51,102,153)` to `#336699`."""
    regex = re.compile('rgb\\s*\\(\\s*([0-9,\\s]+)\\s*\\)')
    match = regex.search(css)
    while match:
        colors = map(lambda s: s.strip(), match.group(1).split(','))
        hexcolor = '#%.2x%.2x%.2x' % tuple(map(int, colors))
        css = css.replace(match.group(), hexcolor)
        match = regex.search(css)

    return css


def condense_zero_units(css):
    """Replace `0(px, em, %, etc)` with `0`."""
    return re.sub('([\\s:])(0)(px|em|%|in|cm|mm|pc|pt|ex)', '\\1\\2', css)


def condense_multidimensional_zeros(css):
    """Replace `:0 0 0 0;`, `:0 0 0;` etc. with `:0;`."""
    css = css.replace(':0 0 0 0;', ':0;')
    css = css.replace(':0 0 0;', ':0;')
    css = css.replace(':0 0;', ':0;')
    css = css.replace('background-position:0;', 'background-position:0 0;')
    return css


def condense_floating_points(css):
    """Replace `0.6` with `.6` where possible."""
    return re.sub('(:|\\s)0+\\.(\\d+)', '\\1.\\2', css)


def condense_hex_colors(css):
    """Shorten colors from #AABBCC to #ABC where possible."""
    regex = re.compile('([^\\"\'=\\s])(\\s*)#([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])')
    match = regex.search(css)
    while match:
        first = match.group(3) + match.group(5) + match.group(7)
        second = match.group(4) + match.group(6) + match.group(8)
        if first.lower() == second.lower():
            css = css.replace(match.group(), match.group(1) + match.group(2) + '#' + first)
            match = regex.search(css, match.end() - 3)
        else:
            match = regex.search(css, match.end())

    return css


def condense_whitespace(css):
    """Condense multiple adjacent whitespace characters into one."""
    return re.sub('\\s+', ' ', css)


def condense_semicolons(css):
    """Condense multiple adjacent semicolon characters into one."""
    return re.sub(';;+', ';', css)


def wrap_css_lines(css, line_length):
    """Wrap the lines of the given CSS to an approximate length."""
    lines = []
    line_start = 0
    for i, char in enumerate(css):
        if char == '}' and i - line_start >= line_length:
            lines.append(css[line_start:i + 1])
            line_start = i + 1

    if line_start < len(css):
        lines.append(css[line_start:])
    return ('\n').join(lines)


def cssmin(css, wrap=None):
    css = remove_comments(css)
    css = condense_whitespace(css)
    css = css.replace('"\\"}\\""', '___PSEUDOCLASSBMH___')
    css = remove_unnecessary_whitespace(css)
    css = remove_unnecessary_semicolons(css)
    css = condense_zero_units(css)
    css = condense_multidimensional_zeros(css)
    css = condense_floating_points(css)
    css = normalize_rgb_colors_to_hex(css)
    css = condense_hex_colors(css)
    if wrap is not None:
        css = wrap_css_lines(css, wrap)
    css = css.replace('___PSEUDOCLASSBMH___', '"\\"}\\""')
    css = condense_semicolons(css)
    return css.strip()


def main():
    import optparse, sys
    p = optparse.OptionParser(prog='cssmin', version=__version__, usage='%prog [--wrap N]', description='Reads raw CSS from stdin, and writes compressed CSS to stdout.')
    p.add_option('-w', '--wrap', type='int', default=None, metavar='N', help='Wrap output to approximately N chars per line.')
    options, args = p.parse_args()
    sys.stdout.write(cssmin(sys.stdin.read(), wrap=options.wrap))
    return


if __name__ == '__main__':
    main()