# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/wikitext/commands.py
# Compiled at: 2016-07-03 23:28:12
__doc__ = '\nThis is a module that handles rendering wiki text into html, and reverting HTML back into wiki syntax.  You can see the examples below of how to use the syntax.\n\n== Syntax Formatting ==\n\n    th. Wiki Syntax                             | th. Rendered Output\n    <nowiki>\'\'italic\'\'</nowiki>                 |  \'\'italic\'\'\n    <nowiki>\'\'\'bold\'\'\'</nowiki>                 |  \'\'\'bold\'\'\'\n    <nowiki>___underline___</nowiki>            |  ___underline___\n    <nowiki>---strikeout---</nowiki>            |  ---strikeout---\n    <nowiki>\'\'\'\'\'bold italic\'\'\'\'\'</nowiki>      | \'\'\'\'\'bold italic\'\'\'\'\'\n    <nowiki>__\'\'\'bold underline\'\'\'__</nowiki>   | ___\'\'\'bold under\'\'\'___\n\n== Linebreaks ==\n\nHorizontal rules are created by having a blank line with a repeating dash of\nover 4 characters\n\n<nowiki>----------------</nowiki>\n\n----------------\n\nTable of contents can be created by specifying the toc key, as such:\n\n[toc]\n\n== Headers ==\n    \n    Headers are defined by padding some text with a \'=\' character.  The     number of \'=\' signs that you use will determine the header level.\n    \n    Headers need to be on their own line to work\n    \n    <nowiki> = Header 1 = </nowiki>\n    = Header 1 =\n    \n    <nowiki> == Header 2 == </nowiki>\n    == Header 2 ==\n    \n    <nowiki> === Header 3 === </nowiki>\n    === Header 3 ===\n    \n    <nowiki> ==== Header 4 ==== </nowiki>\n    ==== Header 4 ====\n    \n    etc.\n    \n== Alignment ==\n    \n    Aligning can be done by using --> and <--- flags.  They need to be at the\n    beginning and end of each line.\n    \n<nowiki>--> Align to Center <--</nowiki>\n\n--> Align to Center <--\n\n<nowiki>--> Align to the Right</nowiki>\n\n--> Align to the Right.\n\n    Floating can be achieved in the same way, only using ==> and <== flags.\n\n<nowiki>~~> Float to Center <~~</nowiki>\n\n~~> Float to Center <~~\n\n<nowiki>~~> Float to the Right</nowiki>\n\n~~> Float to the Right\n\n== Sections ==\n    \n    Sections are defined by putting a \':\' in front of any word.  These are\n    used when putting information into groups.  It will create a <div> object\n    and any following lines will be incorporated into your section.\n    \n    Sections need to be a word (can be separated by underscores), and will\n    automatically be rendered into capitalized words.  For example,\n    \'example_section\' will become \'Example Section\' when rendered.\n    \n    Some predefined sections are:\n    \n    th. Section | Description th.\n    note        | Creates a styled text box with your note text.\n    warning     | Creates a styled text box for warnings (red box & text)\n    todo        | Creates a styled text box for todo coding items\n    sa          | Gets expanded as \'See also\', and tries to match the parts                   to another wiki page.\n    see_also    | Same as the above.\n    param       | Gets expanded as \'Parameters\', used to define coding params\n    sdk_history | Will get slurped up for internal use with the docgen                   system.\n    \n    <nowiki>\n    :custom_section     This is a custom section.  To wrap lines around a\n                        section, just include a single slash character at the\n                        end of a line.\n                        \n                        As long as you type text with the same tab/space\n                        level they will be joined together in the same section.\n                        \n                        \n    To exit a section, just break out of the tab flow, or start a new section.\n    </nowiki>\n    \n    :custom_section     This is a custom section.  To wrap lines around a                         section, just include a single slash character at the                        end of a line.\n                        \n                        As long as you type text with the same tab/space                        level they will be joined together in the same section.\n                        \n                        \n    To exit a section, just break out of the tab flow, or start a new section.\n    \n    <nowiki>\n    :note           This is a simple note\n    </nowiki>\n    \n    :note           This is a simple note\n    \n    <nowiki>\n    :todo           This is a todo note.\n    </nowiki>\n    \n    :todo           This is a todo note.\n    \n    <nowiki>\n    :info           This is an info note.\n    </nowiki>\n    \n    :info           This is an info note.\n    \n    <nowiki>\n    :warning        This is a warning message.\n    </nowiki>\n    \n    :warning        This is a warning message.\n    \n    <nowiki>\n    :error          This is an error message.\n    </nowiki>\n    \n    :error          This is an error message.\n\n== Links ==\n\n    External:\n    \n    <nowiki>[http://projexsoftware.github.io/ Projex Software]</nowiki>\n    \n    [http://projexsoftware.github.io/ Projex Software]\n    \n    Internal:\n    \n    <nowiki>[[Internal:Path|Internal Text]]</nowiki>\n    \n    [[Internal:Path|Internal Text]]\n    \n    <nowiki>[img:path/to/image.png]</nowiki>\n    \n    [img:/path/to/image.png]\n\n== Tables ==\n    \n    Tables are created by splitting a line up with pipes.  You need to have\n    at least 1 space between your \'|\' cell to let the system know that you\n    are trying to make a table.\n    \n    To make a table with no header, just do:\n    \n    <nowiki>\n    cell01          |  cell02\n    cell03          |  cell04\n    </nowiki>\n    \n    cell01          | cell02\n    cell03          | cell04\n    \n    Additional cell options can be added to a cell by adding style information\n    in a list with a td. flag somewhere in the cell.\n    \n    <nowiki>\n    td.[text-align:right;min-width:150px] cell01   |  cell02   td.[align:left]\n    td.[text-align:right] cell03                   |  cell04   td.[align:left]\n    </nowiki>\n    \n    td.[text-align:right;min-width:150px] cell01   |  cell02   td.[align:left]\n    td.[text-align:right] cell03                   |  cell04   td.[align:left]\n    \n    To make a table with a header, just add a row that uses the th. formatter:\n    \n    <nowiki>\n    th. Left Header              | Right Header th.\n    td.[text-align:right] cell01 |  cell02\n    td.[text-align:right] cell03 |  cell04\n    </nowiki>\n    \n    th. Left Header | Right Header th.\n    td.[text-align:right] cell01 |  cell02\n    td.[text-align:right] cell03 |  cell04\n\n== Lists ==\n    \n    <nowiki>\n    *. Unordered list item\n    *. Another unordered list item\n    **. Sub list item\n    **. Another sub list item\n    *. Another top level item\n    </nowiki>\n    \n    *. Unordered list item\n    *. Another unordered list item\n    **. Sub list item\n    **. Another sub list item\n    *. Another top level item\n    \n    <nowiki>\n    #. Ordered list item\n    #. Another ordered list item\n    ##. Sub list item\n    ##. Another sub list item\n    #. Another top level item\n    </nowiki>\n    \n    #. Ordered list item\n    #. Another ordered list item\n    ##. Sub list item\n    ##. Another sub list item\n    #. Another top level item\n    \n    Creating a mixed list\n    <nowiki>\n    *. Ordered list item\n    *. Another ordered list item\n    *#. Sub list item\n    *#*. Test middle \\\n         with breaklines\n    *#. Another sub list item\n    *. Another top level item\n    </nowiki>\n    \n    *. Ordered list item\n    *. Another ordered list item\n    *#. Sub list item\n    *#*. Test middle          with breaklines\n    *#. Another sub list item\n    *. Another top level item\n    \n== Syntax Highlighting ==\n    \n    Code examples (will default to python, but can be set with the lang: key)\n    \n    <nowiki>\n    |>>> print "testing"\n    |testing\n    </nowiki>\n    \n    |>>> print "testing"\n    |testing\n    \n    <nowiki>\n    |lang: html\n    |<html>\n    |  <body>\n    |   <h1>Test</h1>\n    |  </body>\n    |</html>\n    </nowiki>\n    \n    |lang: html\n    |<html>\n    |  <body>\n    |   <h1>Test</h1>\n    |  </body>\n    |</html>\n    \n    Simple coloring can be achieved with the color syntax:\n    <nowiki>\n    [color:red|this is some red text]\n    </nowiki>\n    [color:red|this is some red text]\n    \n'
import logging, projex.text, projex.makotext, re, xml.sax.saxutils
from projex.wikitext.urlhandler import UrlHandler
from projex.wikitext import styles as WIKI_STYLES
from projex.text import nativestring as nstr
logger = logging.getLogger(__name__)
EXPR_SECTION = re.compile('^\\s*(:)([^\\s]+)')
EXPR_CENTER = re.compile('^(--|~~)>(.*)<(--|~~)$')
EXPR_RIGHT = re.compile('^(--|~~)>(.*)$')
EXPR_LEFT = re.compile('^(.*)<(--|~~)$')
EXPR_HEADER = re.compile('^(=+\\s+)(.*)(?=\\s+=+)(\\s+=+)$')
EXPR_TOC = re.compile('(\\[toc([^\\]]*)\\])')
EXPR_INTLINK = re.compile('(\\[{2}([^\\]]*)\\]{2})')
EXPR_EXTLINK = re.compile('(\\[(\\w+://[^\\]]*)\\])')
EXPR_IMG = re.compile('(\\[img:([^\\]]*)\\])')
EXPR_COLOR = re.compile('(\\[color:([^\\]]*)\\])')
EXPR_SPAN = re.compile('(\\[span:([^\\]]*)\\])')
EXPR_INLINE_CODE = re.compile('(?<=`)(.*?)(?=`)')
EXPR_CODE = re.compile('^\\s*\\|(.*)$')
EXPR_LANG = re.compile('lang:\\s*(.*)$')
EXPR_ITALIC = re.compile("(?<='{2})(.*?)(?='{2})'{2}")
EXPR_BOLD = re.compile("(?<='{3})(.*?)(?='{3})'{3}")
EXPR_UNDERLINE = re.compile('(?<=_{3})(.*?)(?=_{3})_{3}')
EXPR_STRIKEOUT = re.compile('(?<=-{3})(.*?)(?=-{3})-{3}')
EXPR_NOWIKI = re.compile('(?<=<nowiki>)(.*?)(?=</nowiki>)</nowiki>')
EXPR_LIST = re.compile('^\\s*([\\*#\\d]+)\\.\\s*(.*)$')
EXPR_TABLE_CELL = re.compile('((td|th)\\.(\\[[^]]*\\])?)')
EXPR_HR = re.compile('^----+$')
EXPR_CLASS_LINK = re.compile('&lt;(\\w[^&]+)&gt;')
SECTION_MAP = {'sa': 'See also', 
   'param': 'Parameters'}
SECTION_ALERTS = ('note', 'warning', 'info', 'error', 'todo')
PRE_ESCAPE_REPLACE = {'%': '%%'}
POST_ESCAPE_REPLACE = {'(C)': '&copy;', 
   '(c)': '&copy;'}

def render(plain, urlHandler=None, templatePaths=None, options=None, defaultTag='div', wikiStyle='basic'):
    """
    Renders the inputted plain text wiki information into HTML rich text.
    
    :param      plain       |  <str> |                                Include some additional documentation
                urlHandler  |  <UlrHandler> || None
    
    :return     <str> html
    """
    if not plain:
        return ''
    __style = WIKI_STYLES.styles.get(wikiStyle, WIKI_STYLES.styles['basic'])
    if not urlHandler:
        urlHandler = UrlHandler.current()
    plain = projex.makotext.render(plain, options=options, templatePaths=templatePaths, silent=True)
    lines = re.split('\n\r|\r\n|\n|\r', plain)
    curr_section = ''
    curr_section_level = 0
    html = []
    skip = []
    nowiki_stack = []
    nowiki_mode = 'pre'
    code_stack = []
    table_stack = []
    list_stack = []
    section_stack = []
    toc_data = []
    align_div = ''
    list_indent = None
    ignore_list_stack = False
    html.append(__style['wiki_open'].format(tag=defaultTag))
    for i, line in enumerate(lines):
        ignore_list_stack = False
        sline = line.strip()
        if list_indent:
            line_indent = len(re.match('\\s*', line).group())
            if line_indent < list_indent:
                list_indent = None
                html.append(__style['list_item_close'])
            else:
                ignore_list_stack = True
                if not sline:
                    html.append(__style['spacer'])
                    continue
        if i in skip:
            continue
        center = EXPR_CENTER.match(sline)
        right = EXPR_RIGHT.match(sline)
        left = EXPR_LEFT.match(sline)
        if center:
            style = center.groups()[0]
            line = center.groups()[1].strip()
            if align_div and align_div != 'center':
                html.append(__style['align_close'])
                align_div = ''
            if not align_div:
                if style == '--':
                    html.append(__style['align_center'])
                else:
                    html.append(__style['align_center_floated'])
                align_div = 'center'
            else:
                html.append(__style['newline'])
        else:
            if right:
                style = right.groups()[0]
                line = right.groups()[1]
                if align_div and align_div != 'right':
                    html.append(__style['align_close'])
                    align_div = ''
                if not align_div:
                    if style == '--':
                        html.append(__style['align_right'])
                    else:
                        html.append(__style['align_right_floated'])
                    align_div = 'right'
                else:
                    html.append(__style['newline'])
            else:
                if left:
                    style = left.groups()[1]
                    line = left.groups()[0]
                    if align_div and align_div != 'left':
                        html.append(__style['align_close'])
                        align_div = ''
                    if not align_div:
                        if style == '--':
                            html.append(__style['align_left'])
                        else:
                            html.append(__style['align_left_floated'])
                        align_div = 'left'
                    else:
                        html.append(__style['newline'])
                else:
                    if align_div:
                        html.append(__style['align_close'])
                        align_div = ''
                    if curr_section and sline and len(line) - len(line.lstrip()) < curr_section_level:
                        html += section_stack
                        section_stack = []
                        curr_section = ''
                        curr_section_level = 0
                    count = i
                    while sline.endswith('\\') and count + 1 < len(lines):
                        sline += ' ' + lines[(count + 1)].strip()
                        skip.append(count)
                        count += 1

                    if sline.startswith('<nowiki'):
                        mode = re.search('mode="(\\w*)"', sline)
                        if mode:
                            nowiki_mode = nstr(mode.group(1))
                        else:
                            nowiki_mode = None
                        if not ignore_list_stack:
                            html += list_stack
                            list_stack = []
                        html += table_stack
                        table_stack = []
                        if nowiki_mode is None:
                            html.append(__style['nowiki_open'])
                            nowiki_stack.append(__style['nowiki_close'])
                        else:
                            nowiki_stack.append('')
                        continue
                    else:
                        if sline == '</nowiki>':
                            html += nowiki_stack
                            nowiki_stack = []
                            continue
                        else:
                            if nowiki_stack:
                                if nowiki_mode == 'safe':
                                    html.append(line)
                                else:
                                    html.append(xml.sax.saxutils.escape(line))
                                continue
                            parts = line.split(' | ')
                            if len(parts) == 1:
                                html += table_stack
                                table_stack = []
                            for key, repl in PRE_ESCAPE_REPLACE.items():
                                line = line.replace(key, repl)

                            nowiki_dict = {}
                            count = 0
                            for section in EXPR_NOWIKI.findall(line)[::2]:
                                nowiki_dict['nowiki_%i' % count] = section
                                newtext = '%%(nowiki_%i)s' % count
                                line = line.replace('<nowiki>%s</nowiki>' % section, newtext)
                                count += 1

                            section = EXPR_SECTION.match(sline)
                            if section:
                                html += code_stack
                                code_stack = []
                                name = section.group(2)
                                if name != curr_section:
                                    html += section_stack
                                    section_stack = []
                                    if name not in SECTION_ALERTS:
                                        section_stack.append(__style['section_close'])
                                        display = projex.text.capitalizeWords(name)
                                        mapped = SECTION_MAP.get(name, display)
                                        html.append(__style['section_open'].format(name=name, title=mapped))
                                    else:
                                        display = projex.text.capitalizeWords(name)
                                        mapped = SECTION_MAP.get(name, display)
                                        section_stack.append(__style['section_alert_close'])
                                        url, success = urlHandler.resolve('img:%s.png' % name)
                                        html.append(__style['section_alert_open'].format(name=name, title=mapped))
                                    curr_section = name
                                else:
                                    html.append(__style['newline'])
                                sline = sline.replace(section.group(), '')
                                line = line.replace(section.group(), ' ' * len(section.group()))
                                curr_section_level = len(line) - len(line.lstrip())
                            code = EXPR_CODE.match(sline)
                            if code:
                                templ = ''
                                code_line = code.groups()[0]
                                if not code_stack:
                                    lang = 'python'
                                    lang_search = EXPR_LANG.search(code_line)
                                    if lang_search:
                                        lang = lang_search.groups()[0]
                                        code_line = code_line.replace(lang_search.group(), '')
                                    templ = __style['code_open'].format(lang=lang)
                                    code_stack.append(__style['code_close'])
                                escaped = xml.sax.saxutils.escape(code_line)
                                if not ignore_list_stack:
                                    html += list_stack
                                    list_stack = []
                                html += table_stack
                                table_stack = []
                                html.append(templ + escaped)
                                continue
                            else:
                                html += code_stack
                                code_stack = []
                            if not sline:
                                html.append(__style['paragraph_close'])
                                html.append(__style['paragraph_open'])
                                continue
                            if EXPR_HR.match(sline):
                                style = ''
                                html.append(__style['hr'].format(style=style))
                                continue
                            header = EXPR_HEADER.match(sline)
                            if header:
                                hopen, title, hclose = header.groups()
                                hopencount = len(hopen)
                                title = title.strip()
                                if hopencount == len(hclose):
                                    name = projex.text.underscore(title)
                                    add = __style['header'].format(name=name, title=title, size=len(hopen))
                                    spacing = '#' * hopencount
                                    opts = (spacing, name, title)
                                    toc_data.append('%s. [[#%s|%s]]' % opts)
                                    if not ignore_list_stack:
                                        html += list_stack
                                        list_stack = []
                                    html += table_stack
                                    table_stack = []
                                    html.append(add)
                                    continue
                            line = xml.sax.saxutils.escape(line)
                            for key, repl in POST_ESCAPE_REPLACE.items():
                                line = line.replace(key, repl)

                            for result in EXPR_CLASS_LINK.findall(line):
                                opts = result.split()
                                for o, cls in enumerate(opts):
                                    if '.' not in cls:
                                        continue
                                    url, success = urlHandler.resolveClass(cls)
                                    if success:
                                        opts[o] = __style['link_class'].format(url=url, text=cls.split('.')[(-1)])

                                info = __style['span_class'].format(crumbs=(' ').join(opts))
                                line = line.replace('&lt;' + result + '&gt;', info)

                            for section in EXPR_UNDERLINE.findall(line)[::2]:
                                text = __style['underline'].format(text=section)
                                line = line.replace('___%s___' % section, text)

                            for section in EXPR_INLINE_CODE.findall(line)[::2]:
                                text = __style['inline_code'].format(text=section)
                                line = line.replace('`%s`' % section, text)

                            for section in EXPR_STRIKEOUT.findall(line)[::2]:
                                text = __style['strikeout'].format(text=section)
                                line = line.replace('---%s---' % section, text)

                            for section in EXPR_BOLD.findall(line)[::2]:
                                text = __style['bold'].format(text=section)
                                line = line.replace("'''%s'''" % section, text)

                            for section in EXPR_ITALIC.findall(line)[::2]:
                                text = __style['italic'].format(text=section)
                                line = line.replace("''%s''" % section, text)

                            for grp, url in EXPR_IMG.findall(line):
                                urlsplit = url.split('|')
                                last_word = re.findall('\\w+', urlsplit[0])[(-1)]
                                if len(urlsplit) == 1:
                                    urlsplit.append('')
                                url, _ = urlHandler.resolveImage(urlsplit[0])
                                line = line.replace(grp, __style['img'].format(url=url, style=urlsplit[1], title=last_word))

                        for grp, coloring in EXPR_COLOR.findall(line):
                            splt = coloring.split('|')
                            if len(splt) == 1:
                                splt.append('')
                            line = line.replace(grp, __style['color'].format(color=splt[0], text=splt[1]))

                    for grp, coloring in EXPR_SPAN.findall(line):
                        splt = coloring.split('|')
                        if len(splt) == 1:
                            splt.append('')
                        templ = '<span style="%s">%s</span>' % (splt[0], splt[1])
                        line = line.replace(grp, __style['span'].format(style=splt[0], text=splt[1]))

                for result in EXPR_EXTLINK.findall(line):
                    grp = result[0]
                    url = result[1]
                    urlsplit = url.split()
                    if len(urlsplit) == 1:
                        urlsplit.append(urlsplit[0])
                    url = urlsplit[0]
                    urltext = (' ').join(urlsplit[1:])
                    line = line.replace(grp, __style['link_ext'].format(url=url, text=urltext))

            for grp, url in EXPR_INTLINK.findall(line):
                urlsplit = url.split('|')
                if len(urlsplit) == 1:
                    last_word = re.findall('\\w+', urlsplit[0])[(-1)]
                    urlsplit.append(last_word)
                url = urlsplit[0]
                title = ('|').join(urlsplit[1:])
                found = True
                tagsplit = url.split('#')
                if len(tagsplit) == 1:
                    url = url
                    tag = ''
                else:
                    url = tagsplit[0]
                    tag = ('#').join(tagsplit[1:])
                if url:
                    url, exists = urlHandler.resolve(url)
                    if not exists:
                        found = False
                if tag:
                    url = url + '#' + tag
                if found:
                    templ = __style['link_found'].format(url=url, text=title)
                else:
                    templ = __style['link_not_found'].format(url=url, text=title)
                line = line.replace(grp, templ)

        results = EXPR_LIST.match(line)
        if results:
            level, linetext = results.groups()
            level_count = len(level)
            level_type = 'unordered' if level[(-1)] == '*' else 'ordered'
            while level_count > len(list_stack):
                html.append(__style[(level_type + '_list_open')])
                list_stack.append(__style[(level_type + '_list_close')])

            while len(list_stack) > level_count:
                html.append(list_stack[(-1)])
                list_stack = list_stack[:-1]

            space_line = line.replace(level + '.', ' ' * (len(level) + 1))
            list_indent = len(re.match('\\s*', space_line).group())
            html.append(__style['list_item_open'])
            html.append(linetext)
            continue
        elif not ignore_list_stack:
            html += list_stack
            list_stack = []
        parts = line.split(' | ')
        if len(parts) > 1:
            if not table_stack:
                table_stack.append(__style['table_close'])
                html.append(__style['table_open'])
            cell_type = 'td'
            styles = ''
            cells = []
            for part in parts:
                results = EXPR_TABLE_CELL.search(part)
                if not results:
                    cells.append(__style['table_cell'].format(tag='td', style='', text=part.strip()))
                else:
                    grp, cell_type, styles = results.groups()
                    if not styles:
                        styles = ''
                    else:
                        styles = styles.strip('[]')
                    part = part.replace(grp, '').strip()
                    opts = (cell_type, styles, part, cell_type)
                    cells.append(__style['table_cell'].format(tag=cell_type, style=styles, text=part))

            line = __style['table_row'].format(text=('').join(cells))
            html.append(line % nowiki_dict)
        else:
            html += table_stack
            table_stack = []
            html.append(line % nowiki_dict)

    if align_div:
        html.append(__style['align_close'])
    if list_indent:
        html.append(__style['list_item_close'])
    html += table_stack
    html += list_stack
    html += code_stack
    html += nowiki_stack
    html += section_stack
    html.append(__style['wiki_close'].format(tag=defaultTag))
    html_txt = ('\n').join(html)
    for toc, options in EXPR_TOC.findall(html_txt):
        toc_wiki = ('\n\t').join(toc_data)
        toc_html = __style['toc_open']
        toc_html += render(toc_wiki, urlHandler, templatePaths, options, 'div', wikiStyle)
        toc_html += __style['toc_close']
        html_txt = html_txt.replace(toc, toc_html)

    html_txt = html_txt.replace('\\[', '[').replace('\\]', ']')
    return html_txt