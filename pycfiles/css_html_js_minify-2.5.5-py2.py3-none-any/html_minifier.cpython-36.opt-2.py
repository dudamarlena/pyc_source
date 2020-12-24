# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /css_html_js_minify/html_minifier.py
# Compiled at: 2018-04-14 09:30:35
# Size of source mod 2**32: 5719 bytes
"""HTML Minifier functions for CSS-HTML-JS-Minify."""
import re
__all__ = ('html_minify', )

def condense_html_whitespace--- This code section failed: ---

 L.  20         0  BUILD_LIST_0          0 
                2  STORE_FAST               'tagsStack'

 L.  21         4  LOAD_GLOBAL              re
                6  LOAD_ATTR                split
                8  LOAD_STR                 '(<\\s*pre.*>|<\\s*/\\s*pre\\s*>|<\\s*textarea.*>|<\\s*/\\s*textarea\\s*>)'
               10  LOAD_FAST                'html'
               12  LOAD_GLOBAL              re
               14  LOAD_ATTR                IGNORECASE
               16  LOAD_CONST               ('flags',)
               18  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               20  STORE_FAST               'split'

 L.  22        22  SETUP_LOOP          168  'to 168'
               24  LOAD_GLOBAL              range
               26  LOAD_CONST               0
               28  LOAD_GLOBAL              len
               30  LOAD_FAST                'split'
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  CALL_FUNCTION_2       2  '2 positional arguments'
               36  GET_ITER         
               38  FOR_ITER            166  'to 166'
               40  STORE_FAST               'i'

 L.  24        42  LOAD_FAST                'i'
               44  LOAD_CONST               1
               46  BINARY_ADD       
               48  LOAD_CONST               2
               50  BINARY_MODULO    
               52  LOAD_CONST               0
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE   124  'to 124'

 L.  25        58  LOAD_GLOBAL              rawtag
               60  LOAD_FAST                'split'
               62  LOAD_FAST                'i'
               64  BINARY_SUBSCR    
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  STORE_FAST               'tag'

 L.  26        70  LOAD_FAST                'tag'
               72  LOAD_ATTR                startswith
               74  LOAD_STR                 '/'
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  POP_JUMP_IF_FALSE   112  'to 112'

 L.  27        80  LOAD_FAST                'tagsStack'
               82  UNARY_NOT        
               84  POP_JUMP_IF_TRUE    102  'to 102'
               86  LOAD_STR                 '/'
               88  LOAD_FAST                'tagsStack'
               90  LOAD_ATTR                pop
               92  CALL_FUNCTION_0       0  '0 positional arguments'
               94  BINARY_ADD       
               96  LOAD_FAST                'tag'
               98  COMPARE_OP               !=
            100_0  COME_FROM            84  '84'
              100  POP_JUMP_IF_FALSE   122  'to 122'

 L.  28       102  LOAD_GLOBAL              Exception
              104  LOAD_STR                 'Some tag is not closed properly'
              106  CALL_FUNCTION_1       1  '1 positional argument'
              108  RAISE_VARARGS_1       1  'exception'
              110  JUMP_BACK            38  'to 38'
              112  ELSE                     '122'

 L.  30       112  LOAD_FAST                'tagsStack'
              114  LOAD_ATTR                append
              116  LOAD_FAST                'tag'
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  POP_TOP          
            122_0  COME_FROM           100  '100'

 L.  31       122  CONTINUE             38  'to 38'

 L.  34       124  LOAD_FAST                'tagsStack'
              126  POP_JUMP_IF_TRUE     38  'to 38'

 L.  35       128  LOAD_GLOBAL              re
              130  LOAD_ATTR                sub
              132  LOAD_STR                 '>\\s+<'
              134  LOAD_STR                 '> <'
              136  LOAD_FAST                'split'
              138  LOAD_FAST                'i'
              140  BINARY_SUBSCR    
              142  CALL_FUNCTION_3       3  '3 positional arguments'
              144  STORE_FAST               'temp'

 L.  36       146  LOAD_GLOBAL              re
              148  LOAD_ATTR                sub
              150  LOAD_STR                 '\\s{2,}|[\\r\\n]'
              152  LOAD_STR                 ' '
              154  LOAD_FAST                'temp'
              156  CALL_FUNCTION_3       3  '3 positional arguments'
              158  LOAD_FAST                'split'
              160  LOAD_FAST                'i'
              162  STORE_SUBSCR     
              164  JUMP_BACK            38  'to 38'
              166  POP_BLOCK        
            168_0  COME_FROM_LOOP       22  '22'

 L.  37       168  LOAD_STR                 ''
              170  LOAD_ATTR                join
              172  LOAD_FAST                'split'
              174  CALL_FUNCTION_1       1  '1 positional argument'
              176  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 166


def rawtag(str):
    if re.match('<\\s*pre.*>', str, flags=(re.IGNORECASE)):
        return 'pre'
    else:
        if re.match('<\\s*textarea.*>', str, flags=(re.IGNORECASE)):
            return 'txt'
        if re.match('<\\s*/\\s*pre\\s*>', str, flags=(re.IGNORECASE)):
            return '/pre'
        if re.match('<\\s*/\\s*textarea\\s*>', str, flags=(re.IGNORECASE)):
            return '/txt'


def condense_style(html):
    """Condense style html tags.

    >>> condense_style('<style type="text/css">*{border:0}</style><p>a b c')
    '<style>*{border:0}</style><p>a b c'
    """
    return html.replace'<style type="text/css">''<style>'.replace"<style type='text/css'>"'<style>'.replace'<style type=text/css>''<style>'


def condense_script(html):
    """Condense script html tags.

    >>> condense_script('<script type="text/javascript"> </script><p>a b c')
    '<script> </script><p>a b c'
    """
    return html.replace'<script type="text/javascript">''<script>'.replace"<style type='text/javascript'>"'<script>'.replace'<style type=text/javascript>''<script>'


def clean_unneeded_html_tags(html):
    """Clean unneeded optional html tags.

    >>> clean_unneeded_html_tags('a<body></img></td>b</th></tr></hr></br>c')
    'abc'
    """
    for tag_to_remove in '</area> </base> <body> </body> </br> </col>\n        </colgroup> </dd> </dt> <head> </head> </hr> <html> </html> </img>\n        </input> </li> </link> </meta> </option> </param> <tbody> </tbody>\n        </td> </tfoot> </th> </thead> </tr> </basefont> </isindex> </param>\n            '.split:
        html = html.replacetag_to_remove''

    return html


def remove_html_comments(html):
    """Remove all HTML comments, Keep all for Grunt, Grymt and IE.

    >>> _="<!-- build:dev -->a<!-- endbuild -->b<!--[if IE 7]>c<![endif]--> "
    >>> _+= "<!-- kill me please -->keep" ; remove_html_comments(_)
    '<!-- build:dev -->a<!-- endbuild -->b<!--[if IE 7]>c<![endif]--> keep'
    """
    return re.compile'<!-- .*? -->'re.I.sub''html


def unquote_html_attributes(html):
    """Remove all HTML quotes on attibutes if possible.

    >>> unquote_html_attributes('<img   width="9" height="5" data-foo="0"  >')
    '<img width=9 height=5 data-foo=0 >'
    """
    any_tag = re.compile'<\\w.*?>'re.I | re.MULTILINE | re.DOTALL
    space = re.compile' \\s+|\\s +'re.MULTILINE
    space1 = re.compile'\\w\\s+\\w're.MULTILINE
    space2 = re.compile'"\\s+>'re.MULTILINE
    space3 = re.compile"'\\s+>"re.MULTILINE
    space4 = re.compile'"\\s\\s+\\w+="|\'\\s\\s+\\w+=\'|"\\s\\s+\\w+=|\'\\s\\s+\\w+='re.MULTILINE
    space6 = re.compile'\\d\\s+>'re.MULTILINE
    quotes_in_tag = re.compile'([a-zA-Z]+)="([a-zA-Z0-9-_\\.]+)"'
    for tag in iterany_tag.findallhtml:
        if not tag.startswith'<!':
            if tag.find'</' > -1:
                pass
            else:
                original = tag
                tag = space2.sub'" >'tag
                tag = space3.sub"' >"tag
                for each in space1.findalltag + space6.findalltag:
                    tag = tag.replaceeachspace.sub' 'each

                for each in space4.findalltag:
                    tag = tag.replaceeacheach[0] + ' ' + each[1:].lstrip

                tag = quotes_in_tag.sub'\\1=\\2 'tag
                if original != tag:
                    html = html.replaceoriginaltag

    return html.strip


def html_minify(html, comments=False):
    """Minify HTML main function.

    >>> html_minify(' <p  width="9" height="5"  > <!-- a --> b </p> c <br> ')
    '<p width=9 height=5 > b c <br>'
    """
    html = remove_html_commentshtml if not comments else html
    html = condense_stylehtml
    html = condense_scripthtml
    html = clean_unneeded_html_tagshtml
    html = condense_html_whitespacehtml
    html = unquote_html_attributeshtml
    return html.strip