# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/g/projects/superhelp/build/lib/superhelp/mdv_fixed.py
# Compiled at: 2020-04-16 19:16:39
# Size of source mod 2**32: 51732 bytes
"""_
# Usage:

    mdv [options] [MDFILE]

# Options:
    -A         : no_colors     : Strip all ansi (no colors then)
    -C MODE    : code_hilite   : Sourcecode highlighting mode
    -F FILE    : config_file   : Alternative configfile (defaults ~./.mdv or ~/.config/mdv)
    -H         : do_html       : Print html version
    -L         : display_links : Backwards compatible shortcut for '-u i'
    -M DIR     : monitor_dir   : Monitor directory for markdown file changes
    -T C_THEME : c_theme       : Theme for code highlight. If not set we use THEME.
    -X Lexer   : c_def_lexer   : Default lexer name (default python). Set -x to use it always.
    -b TABL    : tab_length    : Set tab_length to sth. different than 4 [default 4]
    -c COLS    : cols          : Fix columns to this (default <your terminal width>)
    -f FROM    : from_txt      : Display FROM given substring of the file.
    -h         : sh_help       : Show help
    -i         : theme_info    : Show theme infos with output
    -l         : bg_light      : Light background (not yet supported)
    -m         : monitor_file  : Monitor file for changes and redisplay FROM given substring
    -n NRS     : header_nrs    : Header numbering (default off. Say e.g. -3 or 1- or 1-5)
    -t THEME   : theme         : Key within the color ansi_table.json. 'random' accepted.
    -u STYL    : link_style    : Link Style (it=inline table=default, h=hide, i=inline)
    -x         : c_no_guess    : Do not try guess code lexer (guessing is a bit slow)

# Details

### **MDFILE**

Filename to markdownfile or '-' for pipe mode (no termwidth auto dedection then)

### Configuration

Happens like:

    1. parse_default_files at (`~/.mdv` or `~/.config/mdv`)
    2. overlay with any -F <filename> config
    3. overlay with environ vars (e.g. `$MDV_THEME`)
    4. overlay with CLI vars

#### File Formats

We try yaml.  
If not installed we try json.  
If it is the custom config file we fail if not parsable.  
If you prefer shell style config then source and export so you have it as environ.

### **-c COLS**: Columns

We use stty tool to derive terminal size. If you pipe into mdv we use 80 cols.
You can force the columns used via `-c`.  
If you export `$width`, this has precedence over `$COLUMNS`.

### **-b TABL**: Tablength

Setting tab_length away from 4 violates [markdown](https://pythonhosted.org/Markdown/).
But since many editors interpret such source we allow it via that flag.

### **-f FROM**: Partial Display

FROM may contain max lines to display, seperated by colon.
Example:

    -f 'Some Head:10' -> displays 10 lines after 'Some Head'

If the substring is not found we set it to the *first* character of the file -
resulting in output from the top (if your terminal height can be derived
correctly through the stty cmd).

## Themes

`$MDV_CODE_THEME` is an alias for the standard `$MDV_C_THEME`

```bash
export MDV_THEME='729.8953'; mdv foo.md
```

### Theme rollers:

    mdv -T all:  All available code styles on the given file.
    mdv -t all:  All available md styles on the given file.
                 If file is not given we use a short sample file.

So to see all code hilite variations with a given theme:

Say `C_THEME=all` and fix `THEME`

Setting both to all will probably spin your beach ball...

## Inline Usage (mdv as lib)

Call the main function with markdown string at hand to get a
formatted one back. Sorry then for no Py3 support, accepting PRs if they
don't screw Py2.

## Source Code Highlighting

Set -C <all|code|doc|mod> for source code highlighting of source code files.
Mark inline markdown with a '_' following the docstring beginnings.

- all: Show markdown docstrings AND code (default, if you say e.g. -C.)
- code: Only Code
- doc: Only docstrings with markdown
- mod: Only the module level docstring

## File Monitor:

If FROM is not found we display the whole file.

## Directory Monitor:

We check only text file changes, monitoring their size.

By default .md, .mdown, .markdown files are checked but you can change like
`-M 'mydir:py,c,md,'` where the last empty substrings makes mdv also monitor
any file w/o extension (like 'README').

### Running actions on changes:

If you append to `-M` a `'::<cmd>'` we run the command on any change detected
(sync, in foreground).

The command can contain placeholders:

    _fp_     # Will be replaced with filepath
    _raw_    # Will be replaced with the base64 encoded raw content
               of the file
    _pretty_ # Will be replaced with the base64 encoded prettyfied output

Like: `mdv -M './mydocs:py,md::open "_fp_"'` which calls the open command
with argument the path to the changed file.

"""
from __future__ import absolute_import, print_function, unicode_literals
import sys
PY3 = sys.version_info.major > 2
from functools import partial
import imp, io
from json import loads
import logging, os
from random import randint
import re, shutil, textwrap, time, markdown, markdown.util
from markdown.util import etree
from markdown.extensions.tables import TableExtension
from tabulate import tabulate
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension, fenced_code
errout, envget = partial(print, file=(sys.stderr)), os.environ.get
hr_sep, txt_block_cut, code_pref, list_pref, bquote_pref, hr_ends = ('─', '✂', '| ',
                                                                     '- ', '|', '◈')
H1, H2, H3, H4, H5, R, L, BG, BGL, T, TL, C = (231, 153, 117, 109, 65, 124, 59, 16,
                                               188, 188, 59, 102)
CH1, CH2, CH3, CH4, CH5 = (
 H1, H2, H3, H4, H5)
MAGENTA = 89
GREEN = 28
RUST = 196
WHITE = 231
code_hl = {'Comment':'L', 
 'Error':'R', 
 'Generic':'CH2', 
 'Keyword':'GREEN', 
 'Name':'CH1', 
 'Number':'CH4', 
 'Operator':'WHITE', 
 'String':'CH4', 
 'Operator.Word':'MAGENTA', 
 'Literal.String.Single':'RUST', 
 'Literal.String.Double':'RUST', 
 'Punctuation':'WHITE', 
 'Literal.Number.Integer':'WHITE', 
 'Literal.Number.Float':'WHITE', 
 'Keyword.Constant':'GREEN'}
admons = {'note':'H3', 
 'warning':'R', 
 'attention':'H1', 
 'hint':'H4', 
 'summary':'H1', 
 'hint':'H4', 
 'question':'H5', 
 'danger':'R', 
 'dev':'H5', 
 'hint':'H4', 
 'caution':'H2'}
link_start = '①'
link_start_ord = ord(link_start)
def_lexer = 'python'
guess_lexer = True
background = BG
left_indent = '  '
color = T
show_links = 'it'
themes = {}
md_sample = ''
mon_max_files = 1000

def get_terminal_size():
    """get terminal size for python3.3 or greater, using shutil.

    taken and modified from http://stackoverflow.com/a/14422538

    Returns:
        tuple: (column, rows) from terminal size, or (0, 0) if error.
    """
    error_terminal_size = (0, 0)
    if hasattr(shutil, 'get_terminal_size'):
        terminal_size = shutil.get_terminal_size(fallback=error_terminal_size)
        return (terminal_size.columns, terminal_size.lines)
    return error_terminal_size


term_columns, term_rows = envget('width', envget('COLUMNS')), envget('LINES')
if not term_columns:
    if '-c' not in sys.argv:
        try:
            term_rows, term_columns = os.popen('stty size 2>/dev/null', 'r').read().split()
            term_columns, term_rows = int(term_columns), int(term_rows)
        except:
            term_columns, term_rows = get_terminal_size()
            if '-' not in sys.argv:
                if (term_columns, term_rows) == (0, 0):
                    logging.debug('!! Could not derive your terminal width !!')

else:
    term_columns, term_rows = int(term_columns or 80), int(term_rows or 200)

    def die(msg):
        errout(msg)
        sys.exit(1)


    def parse_env_and_cli():
        """replacing docopt"""
        kw, argv = {}, list(sys.argv[1:])
        opts = __doc__.split('# Options', 1)[1].split('# Details', 1)[0].strip()
        opts = [_.lstrip().split(':', 2) for _ in opts.splitlines()]
        opts = dict([(l[0].split()[0], (l[0].split()[1:], l[1].strip(), l[2].strip())) for l in opts if len(l) > 2])
        aliases = {'MDV_C_THEME':[
          'AXC_CODE_THEME', 'MDV_CODE_THEME'], 
         'MDV_THEME':[
          'AXC_THEME']}
        for k, v in aliases.items():
            for f in v:
                if f in os.environ:
                    os.environ[k] = envget(f)

        for k, v in opts.items():
            V = envget('MDV_' + v[1].upper())
            if V is not None:
                kw[v[1]] = V

        while argv:
            k = argv.pop(0)
            k = '-h' if k == '--help' else k
            try:
                reqv, n = opts[k][:2]
                kw[n] = argv.pop(0) if reqv else True
            except:
                if not argv:
                    kw['filename'] = k
                else:
                    die('Not understood: %s' % k)

        return kw


    try:
        from pygments import lex, token
        from pygments.lexers import get_lexer_by_name
        import pygments.lexers as pyg_guess_lexer
        have_pygments = True
    except ImportError:
        have_pygments = False

    if PY3:
        unichr = chr
        from html import unescape
        string_type = str
    else:
        from HTMLParser import HTMLParser
        unescape = HTMLParser.unescape
        string_type = basestring

        def breakpoint():
            import pdb
            pdb.set_trace()


    is_app = 0
    def_enc_set = False

    def fix_py2_default_encoding():
        """ can be switched off when used as library"""
        global def_enc_set
        if PY3:
            return
        if not def_enc_set:
            imp.reload(sys)
            sys.setdefaultencoding('utf-8')
            def_enc_set = True


    import logging
    md_logger = logging.getLogger('MARKDOWN')
    md_logger.setLevel(logging.WARNING)
    dir_mon_filepath_ph = '_fp_'
    dir_mon_content_raw = '_raw_'
    dir_mon_content_pretty = '_pretty_'

    def read_themes():
        if not themes:
            with open(j(mydir, 'ansi_tables.json')) as (f):
                themes.update(loads(f.read()))
        return themes


    you_like = 'You like this theme?'

    def make_sample():
        """ Generate the theme roller sample markdown """
        if md_sample:
            return md_sample
        _md = []
        for hl in range(1, 7):
            _md.append('#' * hl + ' ' + 'Header %s' % hl)

        sample_code = "class Foo:\n    bar = 'baz'\n    "
        _md.append('```python\n""" Doc String """\n%s\n```' % sample_code)
        _md.append('\n| Tables        | Fmt |\n| -- | -- |\n| !!! hint: wrapped | 0.1 **strong** |\n    ')
        for ad in list(admons.keys())[:1]:
            _md.append('!!! %s: title\n    this is a %s\n' % (ad, ad.capitalize()))

        globals()['md_sample'] = '\n'.join(_md) + '\n----\n!!! question: %s' % you_like


    code_hl_tokens = {}

    def build_hl_by_token():
        if not have_pygments:
            return
        for k, col in list(code_hl.items()):
            if '.' not in k:
                code_hl_tokens[getattr(token, k)] = globals()[col]
            else:
                ks = k.split('.')
                token2use = token
                for k in ks:
                    token2use = getattr(token2use, k)

                code_hl_tokens[token2use] = globals()[col]


    def clean_ansi(s):
        ansi_escape = re.compile('\\x1b[^m]*m')
        return ansi_escape.sub('', s)


    code_start, code_end = ('\x07', '\x08')
    stng_start, stng_end = ('\x16', '\x10')
    link_start, link_end = ('\x17', '\x18')
    emph_start, emph_end = ('\x11', '\x12')
    punctuationmark = '\x13'
    fenced_codemark = '\x14'
    hr_marker = '\x15'
    no_split = '\x19'

    def j(p, f):
        return os.path.join(p, f)


    mydir = os.path.realpath(__file__).rsplit(os.path.sep, 1)[0]

    def set_theme(theme=None, for_code=None, theme_info=None):
        """ set md and code theme """
        global CH1
        global CH2
        global CH3
        global CH4
        global CH5
        global H1
        global H2
        global H3
        global H4
        global H5
        dec = {False:{'dflt':None, 
          'on_dflt':'random', 
          'env':('MDV_THEME', 'AXC_THEME')}, 
         True:{'dflt':'default', 
          'on_dflt':None, 
          'env':('MDV_CODE_THEME', 'AXC_CODE_THEME')}}
        dec = dec[bool(for_code)]
        try:
            if theme == dec['dflt']:
                for k in dec['env']:
                    ek = envget(k)
                    if ek:
                        theme = ek
                        break

            else:
                if theme == dec['dflt']:
                    theme = dec['on_dflt']
                if not theme:
                    return
                    theme = str(theme)
                    themes = read_themes()
                    if theme == 'random':
                        rand = randint(0, len(themes) - 1)
                        theme = list(themes.keys())[rand]
                    t = themes.get(theme)
                    if not t or len(t.get('ct')) != 5:
                        return
                    _for = ''
                    if for_code:
                        _for = ' (code)'
                    if theme_info:
                        print(low('theme%s: %s (%s)' % (_for, theme, t.get('name'))))
                    t = t['ct']
                    cols = (t[0], t[1], t[2], t[3], t[4])
                    if for_code:
                        CH1, CH2, CH3, CH4, CH5 = cols
                else:
                    H1, H2, H3, H4, H5 = cols
        finally:
            if for_code:
                build_hl_by_token()


    def style_ansi(raw_code, lang=None):
        """ actual code hilite """
        global def_lexer
        global guess_lexer

        def lexer_alias(n):
            if n == 'markdown':
                return 'md'
            return n

        lexer = 0
        if lang:
            try:
                lexer = get_lexer_by_name(lexer_alias(lang))
            except ValueError:
                print(col(R, 'Lexer for %s not found' % lang))

        if not lexer:
            try:
                if guess_lexer:
                    lexer = pyg_guess_lexer(raw_code)
            except:
                pass

        if not lexer:
            for l in (def_lexer, 'yaml', 'python', 'c'):
                try:
                    lexer = get_lexer_by_name(lexer_alias(l))
                    break
                except:
                    continue

        tokens = lex(raw_code, lexer)
        cod = []
        for t, v in tokens:
            if not v:
                continue
            _col = code_hl_tokens.get(t) or C
            cod.append(col(v, _col))

        return ''.join(cod)


    def col_bg(c):
        """ colorize background """
        return '\x1b[48;5;%sm' % c


    def col(s, c, bg=0, no_reset=0):
        """
    print col('foo', 124) -> red 'foo' on the terminal
    c = color, s the value to colorize """
        global background
        reset = reset_col
        if no_reset:
            reset = ''
        for _strt, _end, _col in ((code_start, code_end, H2),
         (
          stng_start, stng_end, H2),
         (
          link_start, link_end, H2),
         (
          emph_start, emph_end, H3)):
            if _strt in s:
                uon, uoff = ('', '')
                if _strt == link_start:
                    uon, uoff = ('\x1b[4m', '\x1b[24m')
                s = s.replace(_strt, col('', _col, bg=background, no_reset=1) + uon)
                s = s.replace(_end, uoff + col('', c, no_reset=1))

        s = '\x1b[38;5;%sm%s%s' % (c, s, reset)
        if bg:
            pass
        return s


    reset_col = '\x1b[0m'

    def low(s):
        return col(s, L)


    def plain(s, **kw):
        return col(s, T)


    def sh(out):
        """ debug tool"""
        for l in out:
            print(l)


    header_nr = {'from':0, 
     'to':0}
    cur_header_state = {i:0 for i in range(1, 11)}

    def reset_cur_header_state():
        """after one document is complete"""
        [into(cur_header_state, i, 0) for i in range(1, 11)]


    def parse_header_nrs(nrs):
        """nrs e.g. "4-10" or "1-\""""
        if not nrs:
            return
            if isinstance(nrs, dict):
                return header_nr.update(nrs)
            if isinstance(nrs, string_type):
                if nrs.startswith('-'):
                    nrs = '1' + nrs
                if nrs.endswith('-'):
                    nrs += '10'
                if '-' not in nrs:
                    nrs += '-10'
                nrs = nrs.split('-')[0:2]
        else:
            try:
                if isinstance(nrs, (tuple, list)):
                    header_nr['from'] = int(nrs[0])
                    header_nr['to'] = int(nrs[1])
                    return
            except Extension as ex:
                try:
                    errout('header numbering not understood', nrs)
                    sys.exit(1)
                finally:
                    ex = None
                    del ex


    def into(m, k, v):
        m[k] = v


    class Tags:
        _last_header_level = 0

        def update_header_state(_, level):
            cur = cur_header_state
            if _._last_header_level > level:
                [into(cur, i, 0) for i in range(level + 1, 10)]
            for l in range(_._last_header_level + 1, level):
                if cur[l] == 0:
                    cur[l] = 1

            cur[level] += 1
            _._last_header_level = level
            ret = ''
            f, t = header_nr['from'], header_nr['to']
            if level >= f:
                if level <= t:
                    ret = '.'.join([str(cur[i]) for i in range(f, t + 1) if cur[i] > 0])
            return ret

        def h(_, s, level, **kw):
            """we set h1 to h10 formatters calling this when we do tag = Tag()"""
            nrstr = _.update_header_state(level)
            if nrstr:
                s = ' ' + s.lstrip()
            header_col = min(level, 5)
            return '\n%s%s%s' % (
             low(''),
             nrstr,
             col(s, globals()[('H%s' % header_col)]))

        def p(_, s, **kw):
            return col(s, T)

        def a(_, s, **kw):
            return col(s, L)

        def hr(_, s, **kw):
            hir = kw.get('hir', 1)
            ind = (hir - 1) * left_indent
            s = e = col(hr_ends, globals()[('H%s' % hir)])
            return low('\n%s%s%s%s%s\n' % (ind, s, hr_marker, e, ind))

        def code(_, s, from_fenced_block=None, **kw):
            """ md code AND ``` style fenced raw code ends here"""
            lang = kw.get('lang')
            if not from_fenced_block:
                s = ('\n' + s).replace('\n    ', '\n')[1:]
            raw_code = s.replace(':-', '\x01--')
            if have_pygments:
                s = style_ansi(raw_code, lang=lang)
            ind = ' ' * kw.get('hir', 2)
            firstl = s.split('\n')[0]
            del_spaces = ' ' * (len(firstl) - len(firstl.lstrip()))
            s = ('\n' + s).replace('\n%s' % del_spaces, '\n')[1:]
            code_lines = ('\n' + s).splitlines()
            prefix = '\n%s%s %s' % (ind, low(code_pref), col('', C, no_reset=1))
            code_lines.pop() if code_lines[(-1)] == '\x1b[0m' else None
            code = prefix.join(code_lines)
            code = code.replace('\x01--', ':-')
            return code + '\n' + reset_col


    if PY3:
        elstr = lambda el: etree.tostring(el).decode('utf-8')
    else:
        elstr = lambda el: etree.tostring(el)

def is_text_node(el):
    """ """
    s = elstr(el)
    html = s.split('<%s' % el.tag, 1)[1].split('>', 1)[1].rsplit('>', 1)[0]
    if not html.startswith('<'):
        return (
         1, html)
    for inline in ('<a', '<em>', '<code>', '<strong>'):
        if html.startswith(inline):
            return (
             1, html)

    return (0, 0)


def rewrap(el, t, ind, pref):
    """ Reasonably smart rewrapping checking punctuations """
    global term_columns
    cols = max(term_columns - len(ind + pref), 5)
    if el.tag == 'code' or len(t) <= cols:
        return t
    if t.startswith('\x02'):
        if t.endswith('\x03'):
            return t
    dedented = textwrap.dedent(t).strip()
    ret = textwrap.fill(dedented, width=cols)
    return ret


def split_blocks(text_block, w, cols, part_fmter=None):
    """ splits while multiline blocks vertically (for large tables) """
    ts = []
    for line in text_block.splitlines():
        parts = []
        line = line.ljust(w, ' ')
        parts.append(line[:cols])
        scols = cols - 2
        parts.extend([' ' + col(txt_block_cut, L, no_reset=1) + line[i:i + scols] for i in range(cols, len(line), scols)])
        ts.append(parts)

    blocks = []
    for block_part_nr in range(len(ts[0])):
        tpart = []
        for lines_block in ts:
            tpart.append(lines_block[block_part_nr])

        if part_fmter:
            part_fmter(tpart)
        tpart[1] = col(tpart[1], H3)
        blocks.append('\n'.join(tpart))

    t = '\n'.join(blocks)
    return '\n%s\n' % t


def replace_links(el, html):
    """digging through inline "<a href=..."
    """
    global show_links
    parts = html.split('<a ')
    if len(parts) == 1:
        return (
         None, html)
    else:
        links_list, cur_link = [], 0
        links = [l for l in el.getchildren() if 'href' in l.keys()]
        return len(parts) == len(links) + 1 or (
         None, html)
    cur = ''
    while parts:
        cur += parts.pop(0).rsplit('</a>')[(-1)]
        if not parts:
            break
        else:
            cur += link_start
            link = links[cur_link]
            cur += parts[0].split('>', 1)[1].split('</a', 1)[0] or ''
            cur += link_end
            if show_links != 'h':
                if show_links == 'i':
                    cur += low('(%s)' % link.get('href', ''))
                else:
                    try:
                        cur += '%s ' % unichr(link_start_ord + cur_link)
                    except NameError:
                        cur += '%s ' % chr(link_start_ord + cur_link)

                    links_list.append(link.get('href', ''))
        cur_link += 1

    return (
     links_list, cur)


class AnsiPrinter(Treeprocessor):
    header_tags = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8')

    def run(self, doc):
        tags = Tags()
        for h in cur_header_state:
            setattr(tags, 'h%s' % h, partial((tags.h), level=h))

        def get_attr(el, attr):
            for c in list(el.items()):
                if c[0] == attr:
                    return c[1]

            return ''

        def formatter--- This code section failed: ---

 L. 954         0  LOAD_FAST                'el'
                2  LOAD_ATTR                tag
                4  LOAD_STR                 'br'
                6  COMPARE_OP               ==
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L. 955        10  LOAD_FAST                'out'
               12  LOAD_METHOD              append
               14  LOAD_STR                 '\n'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  POP_TOP          

 L. 956        20  LOAD_CONST               None
               22  RETURN_VALUE     
             24_0  COME_FROM             8  '8'

 L. 958        24  LOAD_CONST               (None, 0)
               26  UNPACK_SEQUENCE_2     2 
               28  STORE_FAST               'links_list'
               30  STORE_FAST               'is_txt_and_inline_markup'

 L. 959        32  LOAD_GLOBAL              j
               34  POP_TOP          

 L. 960        36  LOAD_FAST                'el'
               38  LOAD_ATTR                tag
               40  LOAD_STR                 'blockquote'
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE   186  'to 186'

 L. 961        46  SETUP_LOOP          182  'to 182'
               48  LOAD_FAST                'el'
               50  LOAD_METHOD              getchildren
               52  CALL_METHOD_0         0  '0 positional arguments'
               54  GET_ITER         
               56  FOR_ITER            180  'to 180'
               58  STORE_FAST               'el1'

 L. 962        60  BUILD_LIST_0          0 
               62  STORE_FAST               'iout'

 L. 963        64  LOAD_DEREF               'formatter'
               66  LOAD_FAST                'el1'
               68  LOAD_FAST                'iout'
               70  LOAD_FAST                'hir'
               72  LOAD_CONST               2
               74  BINARY_ADD       
               76  LOAD_FAST                'el'
               78  LOAD_CONST               ('parent',)
               80  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               82  POP_TOP          

 L. 964        84  LOAD_GLOBAL              col
               86  LOAD_GLOBAL              bquote_pref
               88  LOAD_GLOBAL              H1
               90  CALL_FUNCTION_2       2  '2 positional arguments'
               92  STORE_FAST               'pr'

 L. 965        94  LOAD_STR                 ' '
               96  LOAD_FAST                'hir'
               98  LOAD_CONST               2
              100  BINARY_ADD       
              102  BINARY_MULTIPLY  
              104  STORE_FAST               'sp'

 L. 966       106  SETUP_LOOP          178  'to 178'
              108  LOAD_FAST                'iout'
              110  GET_ITER         
              112  FOR_ITER            176  'to 176'
              114  STORE_FAST               'l'

 L. 967       116  SETUP_LOOP          174  'to 174'
              118  LOAD_FAST                'l'
              120  LOAD_METHOD              splitlines
              122  CALL_METHOD_0         0  '0 positional arguments'
              124  GET_ITER         
              126  FOR_ITER            172  'to 172'
              128  STORE_FAST               'l1'

 L. 968       130  LOAD_FAST                'sp'
              132  LOAD_FAST                'l1'
              134  COMPARE_OP               in
              136  POP_JUMP_IF_FALSE   156  'to 156'

 L. 969       138  LOAD_STR                 ''
              140  LOAD_METHOD              join
              142  LOAD_FAST                'l1'
              144  LOAD_METHOD              split
              146  LOAD_FAST                'sp'
              148  LOAD_CONST               1
              150  CALL_METHOD_2         2  '2 positional arguments'
              152  CALL_METHOD_1         1  '1 positional argument'
              154  STORE_FAST               'l1'
            156_0  COME_FROM           136  '136'

 L. 970       156  LOAD_FAST                'out'
              158  LOAD_METHOD              append
              160  LOAD_FAST                'pr'
              162  LOAD_FAST                'l1'
              164  BINARY_ADD       
              166  CALL_METHOD_1         1  '1 positional argument'
              168  POP_TOP          
              170  JUMP_BACK           126  'to 126'
              172  POP_BLOCK        
            174_0  COME_FROM_LOOP      116  '116'
              174  JUMP_BACK           112  'to 112'
              176  POP_BLOCK        
            178_0  COME_FROM_LOOP      106  '106'
              178  JUMP_BACK            56  'to 56'
              180  POP_BLOCK        
            182_0  COME_FROM_LOOP       46  '46'

 L. 971       182  LOAD_CONST               None
              184  RETURN_VALUE     
            186_0  COME_FROM            44  '44'

 L. 973       186  LOAD_FAST                'el'
              188  LOAD_ATTR                tag
              190  LOAD_STR                 'hr'
              192  COMPARE_OP               ==
              194  POP_JUMP_IF_FALSE   216  'to 216'

 L. 974       196  LOAD_FAST                'out'
              198  LOAD_METHOD              append
              200  LOAD_DEREF               'tags'
              202  LOAD_ATTR                hr
              204  LOAD_STR                 ''
              206  LOAD_FAST                'hir'
              208  LOAD_CONST               ('hir',)
              210  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              212  CALL_METHOD_1         1  '1 positional argument'
              214  RETURN_VALUE     
            216_0  COME_FROM           194  '194'

 L. 977       216  LOAD_FAST                'el'
              218  LOAD_ATTR                text
          220_222  POP_JUMP_IF_TRUE    262  'to 262'

 L. 978       224  LOAD_FAST                'el'
              226  LOAD_ATTR                tag
              228  LOAD_STR                 'p'
              230  COMPARE_OP               ==
          232_234  POP_JUMP_IF_TRUE    262  'to 262'

 L. 979       236  LOAD_FAST                'el'
              238  LOAD_ATTR                tag
              240  LOAD_STR                 'li'
              242  COMPARE_OP               ==
          244_246  POP_JUMP_IF_TRUE    262  'to 262'

 L. 980       248  LOAD_FAST                'el'
              250  LOAD_ATTR                tag
              252  LOAD_METHOD              startswith
              254  LOAD_STR                 'h'
              256  CALL_METHOD_1         1  '1 positional argument'
          258_260  POP_JUMP_IF_FALSE  1094  'to 1094'
            262_0  COME_FROM           244  '244'
            262_1  COME_FROM           232  '232'
            262_2  COME_FROM           220  '220'

 L. 982       262  LOAD_FAST                'el'
              264  LOAD_ATTR                text
          266_268  JUMP_IF_TRUE_OR_POP   272  'to 272'
              270  LOAD_STR                 ''
            272_0  COME_FROM           266  '266'
              272  LOAD_FAST                'el'
              274  STORE_ATTR               text

 L. 985       276  LOAD_GLOBAL              is_text_node
              278  LOAD_FAST                'el'
              280  CALL_FUNCTION_1       1  '1 positional argument'
              282  UNPACK_SEQUENCE_2     2 
              284  STORE_FAST               'is_txt_and_inline_markup'
              286  STORE_FAST               'html'

 L. 987       288  LOAD_FAST                'is_txt_and_inline_markup'
          290_292  POP_JUMP_IF_FALSE   438  'to 438'

 L. 990       294  LOAD_FAST                'html'
              296  LOAD_METHOD              replace
              298  LOAD_STR                 '<br />'
              300  LOAD_STR                 '\n'
              302  CALL_METHOD_2         2  '2 positional arguments'
              304  STORE_FAST               'html'

 L. 992       306  LOAD_FAST                'html'
              308  LOAD_METHOD              rsplit
              310  LOAD_STR                 '<'
              312  LOAD_CONST               1
              314  CALL_METHOD_2         2  '2 positional arguments'
              316  LOAD_CONST               0
              318  BINARY_SUBSCR    
              320  STORE_FAST               't'

 L. 993       322  LOAD_GLOBAL              replace_links
              324  LOAD_FAST                'el'
              326  LOAD_FAST                't'
              328  LOAD_CONST               ('html',)
              330  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              332  UNPACK_SEQUENCE_2     2 
              334  STORE_FAST               'links_list'
              336  STORE_FAST               't'

 L. 994       338  SETUP_LOOP          428  'to 428'

 L. 995       340  LOAD_STR                 '<code>'
              342  LOAD_GLOBAL              code_start
              344  LOAD_GLOBAL              code_end
              346  BUILD_TUPLE_3         3 

 L. 996       348  LOAD_STR                 '<strong>'
              350  LOAD_GLOBAL              stng_start
              352  LOAD_GLOBAL              stng_end
              354  BUILD_TUPLE_3         3 

 L. 997       356  LOAD_STR                 '<em>'
              358  LOAD_GLOBAL              emph_start
              360  LOAD_GLOBAL              emph_end
              362  BUILD_TUPLE_3         3 
              364  BUILD_TUPLE_3         3 
              366  GET_ITER         
              368  FOR_ITER            426  'to 426'
              370  UNPACK_SEQUENCE_3     3 
              372  STORE_FAST               'tg'
              374  STORE_FAST               'start'
              376  STORE_FAST               'end'

 L. 999       378  LOAD_FAST                't'
              380  LOAD_METHOD              replace
              382  LOAD_STR                 '%s'
              384  LOAD_FAST                'tg'
              386  BINARY_MODULO    
              388  LOAD_FAST                'start'
              390  CALL_METHOD_2         2  '2 positional arguments'
              392  STORE_FAST               't'

 L.1000       394  LOAD_STR                 '</%s'
              396  LOAD_FAST                'tg'
              398  LOAD_CONST               1
              400  LOAD_CONST               None
              402  BUILD_SLICE_2         2 
              404  BINARY_SUBSCR    
              406  BINARY_MODULO    
              408  STORE_FAST               'close_tag'

 L.1001       410  LOAD_FAST                't'
              412  LOAD_METHOD              replace
              414  LOAD_FAST                'close_tag'
              416  LOAD_FAST                'end'
              418  CALL_METHOD_2         2  '2 positional arguments'
              420  STORE_FAST               't'
          422_424  JUMP_BACK           368  'to 368'
              426  POP_BLOCK        
            428_0  COME_FROM_LOOP      338  '338'

 L.1003       428  LOAD_GLOBAL              unescape
              430  LOAD_FAST                't'
              432  CALL_FUNCTION_1       1  '1 positional argument'
              434  STORE_FAST               't'
              436  JUMP_FORWARD        444  'to 444'
            438_0  COME_FROM           290  '290'

 L.1005       438  LOAD_FAST                'el'
              440  LOAD_ATTR                text
              442  STORE_FAST               't'
            444_0  COME_FROM           436  '436'

 L.1006       444  LOAD_FAST                't'
              446  LOAD_METHOD              strip
              448  CALL_METHOD_0         0  '0 positional arguments'
              450  STORE_FAST               't'

 L.1007       452  LOAD_STR                 ''
              454  STORE_FAST               'admon'

 L.1008       456  LOAD_STR                 ''
              458  DUP_TOP          
              460  STORE_FAST               'pref'
              462  STORE_FAST               'body_pref'

 L.1009       464  LOAD_FAST                't'
              466  LOAD_METHOD              startswith
              468  LOAD_STR                 '!!! '
              470  CALL_METHOD_1         1  '1 positional argument'
          472_474  POP_JUMP_IF_FALSE   608  'to 608'

 L.1011       476  LOAD_CONST               None
              478  STORE_FAST               '_ad'

 L.1012       480  SETUP_LOOP          522  'to 522'
              482  LOAD_GLOBAL              admons
              484  GET_ITER         
            486_0  COME_FROM           506  '506'
              486  FOR_ITER            520  'to 520'
              488  STORE_FAST               'k'

 L.1013       490  LOAD_FAST                't'
              492  LOAD_CONST               4
              494  LOAD_CONST               None
              496  BUILD_SLICE_2         2 
              498  BINARY_SUBSCR    
              500  LOAD_METHOD              startswith
              502  LOAD_FAST                'k'
              504  CALL_METHOD_1         1  '1 positional argument'
          506_508  POP_JUMP_IF_FALSE   486  'to 486'

 L.1014       510  LOAD_FAST                'k'
              512  STORE_FAST               '_ad'

 L.1015       514  BREAK_LOOP       
          516_518  JUMP_BACK           486  'to 486'
              520  POP_BLOCK        
            522_0  COME_FROM_LOOP      480  '480'

 L.1017       522  LOAD_FAST                '_ad'
          524_526  POP_JUMP_IF_TRUE    568  'to 568'

 L.1018       528  LOAD_FAST                't'
              530  LOAD_CONST               4
              532  LOAD_CONST               None
              534  BUILD_SLICE_2         2 
              536  BINARY_SUBSCR    
              538  LOAD_METHOD              split
              540  LOAD_STR                 ' '
              542  LOAD_CONST               1
              544  CALL_METHOD_2         2  '2 positional arguments'
              546  LOAD_CONST               0
              548  BINARY_SUBSCR    
              550  STORE_FAST               'k'

 L.1019       552  LOAD_GLOBAL              admons
              554  LOAD_METHOD              values
              556  CALL_METHOD_0         0  '0 positional arguments'
              558  LOAD_CONST               0
              560  BINARY_SUBSCR    
              562  LOAD_GLOBAL              admons
              564  LOAD_FAST                'k'
              566  STORE_SUBSCR     
            568_0  COME_FROM           524  '524'

 L.1021       568  LOAD_STR                 '┃ '
              570  DUP_TOP          
              572  STORE_FAST               'pref'
              574  STORE_FAST               'body_pref'

 L.1022       576  LOAD_FAST                'pref'
              578  LOAD_FAST                'k'
              580  LOAD_METHOD              capitalize
              582  CALL_METHOD_0         0  '0 positional arguments'
              584  INPLACE_ADD      
              586  STORE_FAST               'pref'

 L.1023       588  LOAD_FAST                'k'
              590  STORE_FAST               'admon'

 L.1024       592  LOAD_FAST                't'
              594  LOAD_METHOD              split
              596  LOAD_FAST                'k'
              598  LOAD_CONST               1
              600  CALL_METHOD_2         2  '2 positional arguments'
              602  LOAD_CONST               1
              604  BINARY_SUBSCR    
              606  STORE_FAST               't'
            608_0  COME_FROM           472  '472'

 L.1027       608  LOAD_FAST                'el'
              610  LOAD_METHOD              get
              612  LOAD_STR                 'pref'
              614  CALL_METHOD_1         1  '1 positional argument'
          616_618  POP_JUMP_IF_FALSE   654  'to 654'

 L.1029       620  LOAD_FAST                'el'
              622  LOAD_METHOD              get
              624  LOAD_STR                 'pref'
              626  CALL_METHOD_1         1  '1 positional argument'
              628  STORE_FAST               'pref'

 L.1031       630  LOAD_STR                 ' '
              632  LOAD_GLOBAL              len
              634  LOAD_FAST                'pref'
              636  CALL_FUNCTION_1       1  '1 positional argument'
              638  BINARY_MULTIPLY  
              640  STORE_FAST               'body_pref'

 L.1032       642  LOAD_FAST                'el'
              644  LOAD_METHOD              set
              646  LOAD_STR                 'pref'
              648  LOAD_STR                 ''
              650  CALL_METHOD_2         2  '2 positional arguments'
              652  POP_TOP          
            654_0  COME_FROM           616  '616'

 L.1034       654  LOAD_GLOBAL              left_indent
              656  LOAD_FAST                'hir'
              658  BINARY_MULTIPLY  
              660  STORE_FAST               'ind'

 L.1035       662  LOAD_FAST                'el'
              664  LOAD_ATTR                tag
              666  LOAD_DEREF               'self'
              668  LOAD_ATTR                header_tags
              670  COMPARE_OP               in
          672_674  POP_JUMP_IF_FALSE   714  'to 714'

 L.1037       676  LOAD_GLOBAL              int
              678  LOAD_FAST                'el'
              680  LOAD_ATTR                tag
              682  LOAD_CONST               1
              684  LOAD_CONST               None
              686  BUILD_SLICE_2         2 
              688  BINARY_SUBSCR    
              690  CALL_FUNCTION_1       1  '1 positional argument'
              692  STORE_FAST               'hl'

 L.1038       694  LOAD_STR                 ' '
              696  LOAD_FAST                'hl'
              698  LOAD_CONST               1
              700  BINARY_SUBTRACT  
              702  BINARY_MULTIPLY  
              704  STORE_FAST               'ind'

 L.1039       706  LOAD_FAST                'hir'
              708  LOAD_FAST                'hl'
              710  INPLACE_ADD      
              712  STORE_FAST               'hir'
            714_0  COME_FROM           672  '672'

 L.1041       714  LOAD_GLOBAL              rewrap
              716  LOAD_FAST                'el'
              718  LOAD_FAST                't'
              720  LOAD_FAST                'ind'
              722  LOAD_FAST                'pref'
              724  CALL_FUNCTION_4       4  '4 positional arguments'
              726  STORE_FAST               't'

 L.1044       728  LOAD_FAST                'admon'
          730_732  POP_JUMP_IF_FALSE   784  'to 784'

 L.1045       734  LOAD_FAST                'out'
              736  LOAD_METHOD              append
              738  LOAD_STR                 '\n'
              740  CALL_METHOD_1         1  '1 positional argument'
              742  POP_TOP          

 L.1046       744  LOAD_GLOBAL              col
              746  LOAD_FAST                'pref'
              748  LOAD_GLOBAL              globals
              750  CALL_FUNCTION_0       0  '0 positional arguments'
              752  LOAD_GLOBAL              admons
              754  LOAD_FAST                'admon'
              756  BINARY_SUBSCR    
              758  BINARY_SUBSCR    
              760  CALL_FUNCTION_2       2  '2 positional arguments'
              762  STORE_FAST               'pref'

 L.1047       764  LOAD_GLOBAL              col
              766  LOAD_FAST                'body_pref'
              768  LOAD_GLOBAL              globals
              770  CALL_FUNCTION_0       0  '0 positional arguments'
              772  LOAD_GLOBAL              admons
              774  LOAD_FAST                'admon'
              776  BINARY_SUBSCR    
              778  BINARY_SUBSCR    
              780  CALL_FUNCTION_2       2  '2 positional arguments'
              782  STORE_FAST               'body_pref'
            784_0  COME_FROM           730  '730'

 L.1049       784  LOAD_FAST                'pref'
          786_788  POP_JUMP_IF_FALSE   870  'to 870'

 L.1051       790  LOAD_GLOBAL              globals
              792  CALL_FUNCTION_0       0  '0 positional arguments'
              794  LOAD_STR                 'H%s'
              796  LOAD_FAST                'hir'
              798  LOAD_CONST               2
              800  BINARY_SUBTRACT  
              802  LOAD_CONST               5
              804  BINARY_MODULO    
              806  LOAD_CONST               1
              808  BINARY_ADD       
              810  BINARY_MODULO    
              812  BINARY_SUBSCR    
              814  STORE_FAST               'h'

 L.1052       816  LOAD_FAST                'pref'
              818  LOAD_GLOBAL              list_pref
              820  COMPARE_OP               ==
          822_824  POP_JUMP_IF_FALSE   838  'to 838'

 L.1053       826  LOAD_GLOBAL              col
              828  LOAD_FAST                'pref'
              830  LOAD_FAST                'h'
              832  CALL_FUNCTION_2       2  '2 positional arguments'
              834  STORE_FAST               'pref'
              836  JUMP_FORWARD        870  'to 870'
            838_0  COME_FROM           822  '822'

 L.1054       838  LOAD_FAST                'pref'
              840  LOAD_METHOD              split
              842  LOAD_STR                 '.'
              844  LOAD_CONST               1
              846  CALL_METHOD_2         2  '2 positional arguments'
              848  LOAD_CONST               0
              850  BINARY_SUBSCR    
              852  LOAD_METHOD              isdigit
              854  CALL_METHOD_0         0  '0 positional arguments'
          856_858  POP_JUMP_IF_FALSE   870  'to 870'

 L.1055       860  LOAD_GLOBAL              col
              862  LOAD_FAST                'pref'
              864  LOAD_FAST                'h'
              866  CALL_FUNCTION_2       2  '2 positional arguments'
              868  STORE_FAST               'pref'
            870_0  COME_FROM           856  '856'
            870_1  COME_FROM           836  '836'
            870_2  COME_FROM           786  '786'

 L.1057       870  LOAD_STR                 '\n'
              872  LOAD_FAST                'ind'
              874  BINARY_ADD       
              876  LOAD_FAST                'body_pref'
              878  BINARY_ADD       
              880  LOAD_METHOD              join
              882  LOAD_FAST                't'
              884  LOAD_METHOD              splitlines
              886  CALL_METHOD_0         0  '0 positional arguments'
              888  CALL_METHOD_1         1  '1 positional argument'
              890  STORE_FAST               't'

 L.1058       892  LOAD_FAST                'ind'
              894  LOAD_FAST                'pref'
              896  BINARY_ADD       
              898  LOAD_FAST                't'
              900  BINARY_ADD       
              902  STORE_FAST               't'

 L.1070       904  LOAD_GLOBAL              getattr
              906  LOAD_DEREF               'tags'
              908  LOAD_FAST                'el'
              910  LOAD_ATTR                tag
              912  LOAD_GLOBAL              plain
              914  CALL_FUNCTION_3       3  '3 positional arguments'
              916  STORE_FAST               'tag_fmt_func'

 L.1072       918  LOAD_GLOBAL              type
              920  LOAD_FAST                'parent'
              922  CALL_FUNCTION_1       1  '1 positional argument'
              924  LOAD_GLOBAL              type
              926  LOAD_FAST                'el'
              928  CALL_FUNCTION_1       1  '1 positional argument'
              930  COMPARE_OP               ==
          932_934  POP_JUMP_IF_FALSE  1002  'to 1002'

 L.1073       936  LOAD_FAST                'parent'
              938  LOAD_ATTR                tag
              940  LOAD_STR                 'li'
              942  COMPARE_OP               ==
          944_946  POP_JUMP_IF_FALSE  1002  'to 1002'

 L.1074       948  LOAD_FAST                'parent'
              950  LOAD_ATTR                text
          952_954  POP_JUMP_IF_TRUE   1002  'to 1002'

 L.1075       956  LOAD_FAST                'el'
              958  LOAD_ATTR                tag
              960  LOAD_STR                 'p'
              962  COMPARE_OP               ==
          964_966  POP_JUMP_IF_FALSE  1002  'to 1002'

 L.1077       968  LOAD_FAST                'tag_fmt_func'
              970  LOAD_FAST                't'
              972  LOAD_METHOD              lstrip
              974  CALL_METHOD_0         0  '0 positional arguments'
              976  LOAD_FAST                'hir'
              978  LOAD_CONST               ('hir',)
              980  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              982  STORE_FAST               '_out'

 L.1078       984  LOAD_FAST                'out'
              986  LOAD_CONST               -1
              988  DUP_TOP_TWO      
              990  BINARY_SUBSCR    
              992  LOAD_FAST                '_out'
              994  INPLACE_ADD      
              996  ROT_THREE        
              998  STORE_SUBSCR     
             1000  JUMP_FORWARD       1020  'to 1020'
           1002_0  COME_FROM           964  '964'
           1002_1  COME_FROM           952  '952'
           1002_2  COME_FROM           944  '944'
           1002_3  COME_FROM           932  '932'

 L.1080      1002  LOAD_FAST                'out'
             1004  LOAD_METHOD              append
             1006  LOAD_FAST                'tag_fmt_func'
             1008  LOAD_FAST                't'
             1010  LOAD_FAST                'hir'
             1012  LOAD_CONST               ('hir',)
             1014  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1016  CALL_METHOD_1         1  '1 positional argument'
             1018  POP_TOP          
           1020_0  COME_FROM          1000  '1000'

 L.1082      1020  LOAD_FAST                'admon'
         1022_1024  POP_JUMP_IF_FALSE  1036  'to 1036'

 L.1083      1026  LOAD_FAST                'out'
             1028  LOAD_METHOD              append
             1030  LOAD_STR                 '\n'
             1032  CALL_METHOD_1         1  '1 positional argument'
             1034  POP_TOP          
           1036_0  COME_FROM          1022  '1022'

 L.1085      1036  LOAD_FAST                'links_list'
         1038_1040  POP_JUMP_IF_FALSE  1094  'to 1094'

 L.1086      1042  LOAD_CONST               1
             1044  STORE_FAST               'i'

 L.1087      1046  SETUP_LOOP         1094  'to 1094'
             1048  LOAD_FAST                'links_list'
             1050  GET_ITER         
             1052  FOR_ITER           1092  'to 1092'
             1054  STORE_FAST               'l'

 L.1088      1056  LOAD_FAST                'out'
             1058  LOAD_METHOD              append
             1060  LOAD_GLOBAL              low
             1062  LOAD_STR                 '%s[%s] %s'
             1064  LOAD_FAST                'ind'
             1066  LOAD_FAST                'i'
             1068  LOAD_FAST                'l'
             1070  BUILD_TUPLE_3         3 
             1072  BINARY_MODULO    
             1074  CALL_FUNCTION_1       1  '1 positional argument'
             1076  CALL_METHOD_1         1  '1 positional argument'
             1078  POP_TOP          

 L.1089      1080  LOAD_FAST                'i'
             1082  LOAD_CONST               1
             1084  INPLACE_ADD      
             1086  STORE_FAST               'i'
         1088_1090  JUMP_BACK          1052  'to 1052'
             1092  POP_BLOCK        
           1094_0  COME_FROM_LOOP     1046  '1046'
           1094_1  COME_FROM          1038  '1038'
           1094_2  COME_FROM           258  '258'

 L.1093      1094  LOAD_FAST                'is_txt_and_inline_markup'
         1096_1098  POP_JUMP_IF_FALSE  1218  'to 1218'

 L.1094      1100  LOAD_FAST                'el'
             1102  LOAD_ATTR                tag
             1104  LOAD_STR                 'li'
             1106  COMPARE_OP               ==
         1108_1110  POP_JUMP_IF_FALSE  1214  'to 1214'

 L.1095      1112  LOAD_FAST                'el'
             1114  LOAD_METHOD              getchildren
             1116  CALL_METHOD_0         0  '0 positional arguments'
             1118  STORE_FAST               'childs'

 L.1096      1120  SETUP_LOOP         1214  'to 1214'
             1122  LOAD_CONST               ('ul', 'ol')
             1124  GET_ITER         
           1126_0  COME_FROM          1148  '1148'
           1126_1  COME_FROM          1132  '1132'
             1126  FOR_ITER           1212  'to 1212'
             1128  STORE_FAST               'nested'

 L.1097      1130  LOAD_FAST                'childs'
         1132_1134  POP_JUMP_IF_FALSE  1126  'to 1126'
             1136  LOAD_FAST                'childs'
             1138  LOAD_CONST               -1
             1140  BINARY_SUBSCR    
             1142  LOAD_ATTR                tag
             1144  LOAD_FAST                'nested'
             1146  COMPARE_OP               ==
         1148_1150  POP_JUMP_IF_FALSE  1126  'to 1126'

 L.1098      1152  LOAD_FAST                'childs'
             1154  LOAD_CONST               -1
             1156  BINARY_SUBSCR    
             1158  STORE_FAST               'ul'

 L.1103      1160  LOAD_FAST                'out'
             1162  LOAD_CONST               -1
             1164  BINARY_SUBSCR    
             1166  LOAD_METHOD              split
             1168  LOAD_STR                 '<%s>'
             1170  LOAD_FAST                'nested'
             1172  BINARY_MODULO    
             1174  LOAD_CONST               1
             1176  CALL_METHOD_2         2  '2 positional arguments'
             1178  LOAD_CONST               0
             1180  BINARY_SUBSCR    
             1182  LOAD_FAST                'out'
             1184  LOAD_CONST               -1
             1186  STORE_SUBSCR     

 L.1104      1188  LOAD_DEREF               'formatter'
             1190  LOAD_FAST                'ul'
             1192  LOAD_FAST                'out'
             1194  LOAD_FAST                'hir'
             1196  LOAD_CONST               1
             1198  BINARY_ADD       
             1200  LOAD_FAST                'el'
             1202  LOAD_CONST               ('parent',)
             1204  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1206  POP_TOP          
         1208_1210  JUMP_BACK          1126  'to 1126'
             1212  POP_BLOCK        
           1214_0  COME_FROM_LOOP     1120  '1120'
           1214_1  COME_FROM          1108  '1108'

 L.1105      1214  LOAD_CONST               None
             1216  RETURN_VALUE     
           1218_0  COME_FROM          1096  '1096'

 L.1107      1218  LOAD_FAST                'el'
             1220  LOAD_ATTR                tag
             1222  LOAD_STR                 'table'
             1224  COMPARE_OP               ==
         1226_1228  POP_JUMP_IF_FALSE  1574  'to 1574'

 L.1113      1230  LOAD_CODE                <code_object borders>
             1232  LOAD_STR                 'AnsiPrinter.run.<locals>.formatter.<locals>.borders'
             1234  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1236  STORE_FAST               'borders'

 L.1116      1238  LOAD_CLOSURE             'formatter'
             1240  BUILD_TUPLE_1         1 
             1242  LOAD_CODE                <code_object fmt>
             1244  LOAD_STR                 'AnsiPrinter.run.<locals>.formatter.<locals>.fmt'
             1246  MAKE_FUNCTION_8          'closure'
             1248  STORE_FAST               'fmt'

 L.1123      1250  BUILD_LIST_0          0 
             1252  STORE_FAST               't'

 L.1124      1254  SETUP_LOOP         1344  'to 1344'
             1256  LOAD_CONST               (0, 1)
             1258  GET_ITER         
             1260  FOR_ITER           1342  'to 1342'
             1262  STORE_FAST               'he_bo'

 L.1125      1264  SETUP_LOOP         1338  'to 1338'
             1266  LOAD_FAST                'el'
             1268  LOAD_FAST                'he_bo'
             1270  BINARY_SUBSCR    
             1272  LOAD_METHOD              getchildren
             1274  CALL_METHOD_0         0  '0 positional arguments'
             1276  GET_ITER         
             1278  FOR_ITER           1336  'to 1336'
             1280  STORE_FAST               'Row'

 L.1126      1282  BUILD_LIST_0          0 
             1284  STORE_FAST               'row'

 L.1127      1286  LOAD_FAST                't'
             1288  LOAD_METHOD              append
             1290  LOAD_FAST                'row'
             1292  CALL_METHOD_1         1  '1 positional argument'
             1294  POP_TOP          

 L.1128      1296  SETUP_LOOP         1332  'to 1332'
             1298  LOAD_FAST                'Row'
             1300  LOAD_METHOD              getchildren
             1302  CALL_METHOD_0         0  '0 positional arguments'
             1304  GET_ITER         
             1306  FOR_ITER           1330  'to 1330'
             1308  STORE_FAST               'cell'

 L.1129      1310  LOAD_FAST                'row'
             1312  LOAD_METHOD              append
             1314  LOAD_FAST                'fmt'
             1316  LOAD_FAST                'cell'
             1318  LOAD_FAST                'row'
             1320  CALL_FUNCTION_2       2  '2 positional arguments'
             1322  CALL_METHOD_1         1  '1 positional argument'
             1324  POP_TOP          
         1326_1328  JUMP_BACK          1306  'to 1306'
             1330  POP_BLOCK        
           1332_0  COME_FROM_LOOP     1296  '1296'
         1332_1334  JUMP_BACK          1278  'to 1278'
             1336  POP_BLOCK        
           1338_0  COME_FROM_LOOP     1264  '1264'
         1338_1340  JUMP_BACK          1260  'to 1260'
             1342  POP_BLOCK        
           1344_0  COME_FROM_LOOP     1254  '1254'

 L.1130      1344  LOAD_GLOBAL              term_columns
             1346  STORE_FAST               'cols'

 L.1132      1348  LOAD_GLOBAL              tabulate
             1350  LOAD_FAST                't'
             1352  CALL_FUNCTION_1       1  '1 positional argument'
             1354  STORE_FAST               'tbl'

 L.1136      1356  LOAD_GLOBAL              len
             1358  LOAD_FAST                'tbl'
             1360  LOAD_METHOD              split
             1362  LOAD_STR                 '\n'
             1364  LOAD_CONST               1
             1366  CALL_METHOD_2         2  '2 positional arguments'
             1368  LOAD_CONST               0
             1370  BINARY_SUBSCR    
             1372  CALL_FUNCTION_1       1  '1 positional argument'
             1374  STORE_FAST               'w'

 L.1137      1376  LOAD_FAST                'w'
             1378  LOAD_FAST                'cols'
             1380  COMPARE_OP               <=
         1382_1384  POP_JUMP_IF_FALSE  1472  'to 1472'

 L.1138      1386  LOAD_FAST                'tbl'
             1388  LOAD_METHOD              splitlines
             1390  CALL_METHOD_0         0  '0 positional arguments'
             1392  STORE_FAST               't'

 L.1139      1394  LOAD_FAST                'borders'
             1396  LOAD_FAST                't'
             1398  CALL_FUNCTION_1       1  '1 positional argument'
             1400  POP_TOP          

 L.1141      1402  LOAD_FAST                'cols'
             1404  LOAD_FAST                'w'
             1406  BINARY_SUBTRACT  
             1408  LOAD_CONST               2
             1410  BINARY_TRUE_DIVIDE
             1412  STORE_FAST               'ind'

 L.1143      1414  LOAD_FAST                'hir'
             1416  STORE_FAST               'ind'

 L.1144      1418  BUILD_LIST_0          0 
             1420  STORE_FAST               'tt'

 L.1145      1422  SETUP_LOOP         1460  'to 1460'
             1424  LOAD_FAST                't'
             1426  GET_ITER         
             1428  FOR_ITER           1458  'to 1458'
             1430  STORE_FAST               'line'

 L.1146      1432  LOAD_FAST                'tt'
             1434  LOAD_METHOD              append
             1436  LOAD_STR                 '%s%s'
             1438  LOAD_FAST                'ind'
             1440  LOAD_GLOBAL              left_indent
             1442  BINARY_MULTIPLY  
             1444  LOAD_FAST                'line'
             1446  BUILD_TUPLE_2         2 
             1448  BINARY_MODULO    
             1450  CALL_METHOD_1         1  '1 positional argument'
             1452  POP_TOP          
         1454_1456  JUMP_BACK          1428  'to 1428'
             1458  POP_BLOCK        
           1460_0  COME_FROM_LOOP     1422  '1422'

 L.1147      1460  LOAD_FAST                'out'
             1462  LOAD_METHOD              extend
             1464  LOAD_FAST                'tt'
             1466  CALL_METHOD_1         1  '1 positional argument'
             1468  POP_TOP          
             1470  JUMP_FORWARD       1570  'to 1570'
           1472_0  COME_FROM          1382  '1382'

 L.1155      1472  BUILD_LIST_0          0 
             1474  STORE_FAST               'tc'

 L.1156      1476  SETUP_LOOP         1540  'to 1540'
             1478  LOAD_FAST                't'
             1480  GET_ITER         
             1482  FOR_ITER           1538  'to 1538'
             1484  STORE_FAST               'row'

 L.1157      1486  LOAD_FAST                'tc'
             1488  LOAD_METHOD              append
             1490  BUILD_LIST_0          0 
             1492  CALL_METHOD_1         1  '1 positional argument'
             1494  POP_TOP          

 L.1158      1496  LOAD_FAST                'tc'
             1498  LOAD_CONST               -1
             1500  BINARY_SUBSCR    
             1502  STORE_FAST               'l'

 L.1159      1504  SETUP_LOOP         1534  'to 1534'
             1506  LOAD_FAST                'row'
             1508  GET_ITER         
             1510  FOR_ITER           1532  'to 1532'
             1512  STORE_FAST               'cell'

 L.1160      1514  LOAD_FAST                'l'
             1516  LOAD_METHOD              append
             1518  LOAD_GLOBAL              clean_ansi
             1520  LOAD_FAST                'cell'
             1522  CALL_FUNCTION_1       1  '1 positional argument'
             1524  CALL_METHOD_1         1  '1 positional argument'
             1526  POP_TOP          
         1528_1530  JUMP_BACK          1510  'to 1510'
             1532  POP_BLOCK        
           1534_0  COME_FROM_LOOP     1504  '1504'
         1534_1536  JUMP_BACK          1482  'to 1482'
             1538  POP_BLOCK        
           1540_0  COME_FROM_LOOP     1476  '1476'

 L.1163      1540  LOAD_GLOBAL              tabulate
             1542  LOAD_FAST                'tc'
             1544  CALL_FUNCTION_1       1  '1 positional argument'
             1546  STORE_FAST               'table'

 L.1164      1548  LOAD_FAST                'out'
             1550  LOAD_METHOD              append

 L.1165      1552  LOAD_GLOBAL              split_blocks
             1554  LOAD_FAST                'table'
             1556  LOAD_FAST                'w'
             1558  LOAD_FAST                'cols'
             1560  LOAD_FAST                'borders'
             1562  LOAD_CONST               ('part_fmter',)
             1564  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1566  CALL_METHOD_1         1  '1 positional argument'
             1568  POP_TOP          
           1570_0  COME_FROM          1470  '1470'

 L.1167      1570  LOAD_CONST               None
             1572  RETURN_VALUE     
           1574_0  COME_FROM          1226  '1226'

 L.1169      1574  LOAD_CONST               0
             1576  STORE_FAST               'nr'

 L.1170      1578  SETUP_LOOP         1680  'to 1680'
             1580  LOAD_FAST                'el'
             1582  GET_ITER         
             1584  FOR_ITER           1678  'to 1678'
             1586  STORE_FAST               'c'

 L.1171      1588  LOAD_FAST                'el'
             1590  LOAD_ATTR                tag
             1592  LOAD_STR                 'ul'
             1594  COMPARE_OP               ==
         1596_1598  POP_JUMP_IF_FALSE  1614  'to 1614'

 L.1172      1600  LOAD_FAST                'c'
             1602  LOAD_METHOD              set
             1604  LOAD_STR                 'pref'
             1606  LOAD_GLOBAL              list_pref
             1608  CALL_METHOD_2         2  '2 positional arguments'
             1610  POP_TOP          
             1612  JUMP_FORWARD       1654  'to 1654'
           1614_0  COME_FROM          1596  '1596'

 L.1173      1614  LOAD_FAST                'el'
             1616  LOAD_ATTR                tag
             1618  LOAD_STR                 'ol'
             1620  COMPARE_OP               ==
         1622_1624  POP_JUMP_IF_FALSE  1654  'to 1654'

 L.1174      1626  LOAD_FAST                'nr'
             1628  LOAD_CONST               1
             1630  INPLACE_ADD      
             1632  STORE_FAST               'nr'

 L.1175      1634  LOAD_FAST                'c'
             1636  LOAD_METHOD              set
             1638  LOAD_STR                 'pref'
             1640  LOAD_GLOBAL              str
             1642  LOAD_FAST                'nr'
             1644  CALL_FUNCTION_1       1  '1 positional argument'
             1646  LOAD_STR                 '. '
             1648  BINARY_ADD       
             1650  CALL_METHOD_2         2  '2 positional arguments'
             1652  POP_TOP          
           1654_0  COME_FROM          1622  '1622'
           1654_1  COME_FROM          1612  '1612'

 L.1178      1654  LOAD_DEREF               'formatter'
             1656  LOAD_FAST                'c'
             1658  LOAD_FAST                'out'
             1660  LOAD_FAST                'hir'
             1662  LOAD_CONST               1
             1664  BINARY_ADD       
             1666  LOAD_FAST                'el'
             1668  LOAD_CONST               ('parent',)
             1670  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1672  POP_TOP          
         1674_1676  JUMP_BACK          1584  'to 1584'
             1678  POP_BLOCK        
           1680_0  COME_FROM_LOOP     1578  '1578'

Parse error at or near `POP_BLOCK' instruction at offset 1678

        out = []
        formatter(doc, out)
        self.markdown.ansi = '\n'.join(out)


def set_hr_widths(result):
    """
    We want the hrs indented by hirarchy...
    A bit 2 much effort to calc, maybe just fixed with 10
    style seps would have been enough visually:
    ◈────────────◈
    """
    mw = 0
    hrs = []
    if hr_marker not in result:
        return result
    for line in result.splitlines():
        if hr_marker in line:
            hrs.append(line)
            continue
        if len(line) < mw:
            continue
        l = len(clean_ansi(line))
        if l > mw:
            mw = l

    for hr in hrs:
        hcl = clean_ansi(hr)
        ind = len(hcl) - len(hcl.split(hr_marker, 1)[1]) - 1
        w = min(term_columns, mw) - 2 * ind
        hrf = hr.replace(hr_marker, hr_sep * w)
        result = result.replace(hr, hrf)

    return result


class AnsiPrintExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        ansi_print_ext = AnsiPrinter(md)
        md.treeprocessors.add('ansi_print_ext', ansi_print_ext, '>inline')


def do_code_hilite(md, what='all'):
    """
    "inverse" mode for source code highlighting:
    the file contains mainly code and md is within docstrings
    what in  all, code, doc, mod
    """
    if what not in ('all', 'code', 'doc', 'mod'):
        what = 'all'
    code_mode, md_mode = (1, 2)
    blocks, block, mode = [], [], code_mode
    blocks.append([mode, block])
    lines = ('\n' + md).splitlines()
    mdstart = '\x01'
    while lines:
        line = lines.pop(0)
        if mode == code_mode:
            if line.rstrip() in ('"""_', "'''_", '/*_'):
                mdstart = line.rstrip()[:-1]
                mode = md_mode
                block = []
                if mdstart == '/*':
                    mdstart = '*/'
                blocks.append([md_mode, block])
                continue
            else:
                if line.rstrip() == mdstart:
                    if what == 'doc':
                        break
                    mode = code_mode
                    block = []
                    blocks.append([code_mode, block])
                    continue
            if mode == code_mode:
                if what in ('all', 'code'):
                    block.append(line)
        else:
            if what != 'code':
                block.append(line)

    out = []
    for mode, block in blocks:
        b = '\n'.join(block)
        if not b:
            continue
        if mode == code_mode:
            out.append('```\n%s\n```' % b)
        else:
            out.append('\n'.join(block))

    return '\n'.join(out)


def main(md=None, filename=None, cols=None, theme=None, c_theme=None, bg=None, c_no_guess=None, display_links=None, link_style=None, from_txt=None, do_html=None, code_hilite=None, c_def_lexer=None, theme_info=None, no_colors=None, tab_length=4, no_change_defenc=False, header_nrs=False, **kw):
    """ md is markdown string. alternatively we use filename and read """
    global background
    global color
    global def_lexer
    global guess_lexer
    global show_links
    global term_columns
    True if no_change_defenc else fix_py2_default_encoding()
    parse_header_nrs(header_nrs)
    tab_length = tab_length or 4
    if c_def_lexer:
        def_lexer = c_def_lexer
    else:
        py_config_file = os.path.expanduser('~/.mdv.py')
        if os.path.exists(py_config_file):
            exec_globals = {}
            exec(io.open(py_config_file, encoding='utf-8').read(), exec_globals)
            globals().update(exec_globals)
        args = locals()
        if not md:
            if not filename:
                print('Using sample markdown:')
                make_sample()
                md = args['md'] = md_sample
                print(md)
                print
                print('Styling Result')
            else:
                if filename == '-':
                    md = sys.stdin.read()
                else:
                    with open(filename) as (f):
                        md = f.read()
    if cols:
        term_columns = int(cols)
    if c_theme == 'all' or theme == 'all':
        if c_theme == 'all':
            os.environ['AXC_CODE_THEME'] = os.environ['MDV_CODE_THEME'] = ''
        if theme == 'all':
            os.environ['AXC_THEME'] = os.environ['MDV_THEME'] = ''
        args.pop('kw')
        themes = read_themes()
        for k, v in list(themes.items()):
            if not filename:
                yl = 'You like *%s*, *%s*?' % (k, v['name'])
                args['md'] = md_sample.replace(you_like, yl)
            else:
                print(col('%s%s%s' % ('\n\n', '=' * term_columns, '\n'), L))
                if theme == 'all':
                    args['theme'] = k
                else:
                    args['c_theme'] = k
            print(main(**args))

        return ''
    if display_links:
        show_links = 'i'
    if link_style:
        show_links = link_style
    if bg:
        if bg == 'light':
            background = BGL
            color = T
    set_theme(theme, theme_info=theme_info)
    guess_lexer = not c_no_guess
    if not c_theme:
        c_theme = theme or 'default'
    if c_theme == 'None':
        c_theme = None
    if c_theme:
        set_theme(c_theme, for_code=1, theme_info=theme_info)
    if c_theme:
        if not have_pygments:
            errout(col('No pygments, can not analyze code for hilite', R))
    MD = markdown.Markdown(tab_length=(int(tab_length)),
      extensions=[
     AnsiPrintExtension(),
     TableExtension(),
     fenced_code.FencedCodeExtension()])
    if code_hilite:
        md = do_code_hilite(md, code_hilite)
    the_html = MD.convert(md)
    reset_cur_header_state()
    if do_html:
        return the_html
    ansi = MD.ansi
    PH = markdown.util.HTML_PLACEHOLDER
    stash = MD.htmlStash
    nr = -1
    tags = Tags()
    for ph in stash.rawHtmlBlocks:
        nr += 1
        raw = unescape(ph)
        if raw[:3].lower() == '<br':
            raw = '\n'
        pre = '<pre><code'
        if raw.startswith(pre):
            _, raw = raw.split(pre, 1)
            lang = 'Python3'
            raw = raw.split('>', 1)[1].rsplit('</code>', 1)[0]
            raw = tags.code((raw.strip()), from_fenced_block=1, lang=lang)
        ansi = ansi.replace(PH % nr, raw)

    if from_txt:
        if from_txt.split(':', 1)[0] not in ansi:
            from_txt = ansi.strip()[1]
        from_txt, mon_lines = (from_txt + ':%s' % (term_rows - 6)).split(':')[:2]
        mon_lines = int(mon_lines)
        pre, post = ansi.split(from_txt, 1)
        post = '\n'.join(post.split('\n')[:mon_lines])
        ansi = '\n(...)%s%s%s' % (
         '\n'.join(pre.rsplit('\n', 2)[-2:]),
         from_txt,
         post)
    ansi = set_hr_widths(ansi) + '\n'
    if no_colors:
        return clean_ansi(ansi)
    return ansi + '\n'


def monitor(args):
    """ file monitor mode """
    filename = args.get('filename')
    if not filename:
        print(col('Need file argument', 2))
        raise SystemExit
    last_err = ''
    last_stat = 0
    while True:
        if not os.path.exists(filename):
            last_err = 'File %s not found. Will continue trying.' % filename
        else:
            try:
                stat = os.stat(filename)[8]
                if stat != last_stat:
                    parsed = main(**args)
                    print(str(parsed))
                    last_stat = stat
                last_err = ''
            except Exception as ex:
                try:
                    last_err = str(ex)
                finally:
                    ex = None
                    del ex

            if last_err:
                errout('Error: %s' % last_err)
            sleep()


def sleep():
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        errout('Have a nice day!')
        raise SystemExit


def run_changed_file_cmd(cmd, fp, pretty):
    """ running commands on changes.
        pretty the parsed file
    """
    with open(fp) as (f):
        raw = f.read()
    for ph in (
     dir_mon_filepath_ph,
     dir_mon_content_raw,
     dir_mon_content_pretty):
        if ph in cmd and '"%s"' % ph not in cmd and "'%s'" % ph not in cmd:
            cmd = cmd.replace(ph, '"%s"' % ph)

    cmd = cmd.replace(dir_mon_filepath_ph, fp)
    errout(col('Running %s' % cmd, H1))
    for r, what in (
     (
      dir_mon_content_raw, raw),
     (
      dir_mon_content_pretty, pretty)):
        cmd = cmd.replace(r, what.encode('base64'))

    if os.system(cmd):
        errout(col('(the command failed)', R))


def monitor_dir(args):
    """ displaying the changed files """

    def show_fp(fp):
        args['filename'] = fp
        pretty = main(**args)
        print(pretty)
        print('(%s)' % col(fp, L))
        cmd = args.get('change_cmd')
        if cmd:
            run_changed_file_cmd(cmd, fp=fp, pretty=pretty)

    ftree = {}
    d = args.get('monitor_dir')
    d += '::'
    d, args['change_cmd'] = d.split('::')[:2]
    args.pop('monitor_dir')
    args.pop('monitor_file')
    d, exts = (d + ':md,mdown,markdown').split(':')[:2]
    exts = exts.split(',')
    if not os.path.exists(d):
        print(col('Does not exist: %s' % d, R))
        sys.exit(2)
    dir_black_list = ['.', '..']

    def check_dir(d, ftree):
        check_latest = ftree.get('latest_ts')
        d = os.path.abspath(d)
        if d in dir_black_list:
            return
        if len(ftree) > mon_max_files:
            print(col('Max files (%s) reached' % col(mon_max_files, R)))
            dir_black_list.append(d)
            return
        try:
            files = os.listdir(d)
        except Exception as ex:
            try:
                print('%s when scanning dir %s' % (col(ex, R), d))
                dir_black_list.append(d)
                return
            finally:
                ex = None
                del ex

        for f in files:
            fp = j(d, f)
            if os.path.isfile(fp):
                f_ext = f.rsplit('.', 1)[(-1)]
                if f_ext == f:
                    f_ext == ''
                if f_ext not in exts:
                    continue
                old = ftree.get(fp)
                now = os.stat(fp)[6]
                if check_latest:
                    if os.stat(fp)[7] > ftree['latest_ts']:
                        ftree['latest'] = fp
                        ftree['latest_ts'] = os.stat(fp)[8]
                    if now == old:
                        continue
                    ftree[fp] = now
                    if not old:
                        continue
                    if 'text' in os.popen('file "%s"' % fp).read():
                        show_fp(fp)
                elif os.path.isdir(fp):
                    check_dir(j(d, fp), ftree)

    ftree['latest_ts'] = 1
    while True:
        check_dir(d, ftree)
        if 'latest_ts' in ftree:
            ftree.pop('latest_ts')
            fp = ftree.get('latest')
            if fp:
                show_fp(fp)
            else:
                print('sth went wrong, no file found')
        sleep()


def load_config(filename, s=None, yaml=None):
    fns = (filename,) if filename else ('.mdv', '.config/mdv')
    for f in fns:
        fn = os.path.expanduser('~/' + f) if f[0] == '.' else f
        if not os.path.exists(fn):
            if filename:
                die('Not found: %s' % filename)
            else:
                continue
            with open(fn) as (fd):
                s = fd.read()
                break

    if not s:
        return {}
    try:
        import yaml
        m = yaml.safe_load(s)
    except:
        import json
        try:
            m = json.loads(s)
        except:
            errout('could not parse config at %s. Have yaml: %s' % (fn, yaml))
            if filename:
                sys.exit(1)
            m = {}

    return m


load_yaml_config = load_config

def merge(a, b):
    c = a.copy()
    c.update(b)
    return c


def run():
    global is_app
    is_app = 1
    fix_py2_default_encoding() if not PY3 else None
    kw = load_config(None) or {}
    kw1 = parse_env_and_cli()
    fn = kw1.get('config_file')
    if fn:
        kw.update(load_config(filename=fn))
    else:
        kw.update(kw1)
        doc = __doc__[1:]
        if kw.get('sh_help'):
            d = dict(theme=671.1616,
              ctheme=526.9416,
              c_no_guess=True,
              c_def_lexer='md',
              header_nrs='1-',
              md=doc)
            d.update(kw)
            res = main(**d)
            d['header_nrs'] = '0-0'
            d['md'] = '-----' + doc.split('# Details', 1)[0]
            res += main(**d)
            print(res if PY3 else str(res))
            sys.exit(0)
        elif kw.get('monitor_file'):
            monitor(kw)
        else:
            if kw.get('monitor_dir'):
                monitor_dir(kw)
            else:
                print(main(**kw) if PY3 else str(main(**kw)))


if __name__ == '__main__':
    run()