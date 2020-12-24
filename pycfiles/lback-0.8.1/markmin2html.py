# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mdipierro/make_web2py/web2py/gluon/contrib/markmin/markmin2html.py
# Compiled at: 2013-10-14 11:16:24
import re
from cgi import escape
from string import maketrans
try:
    from ast import parse as ast_parse
    import ast
except ImportError:
    from compiler import parse
    import compiler.ast as ast

__all__ = [
 'render', 'markmin2html', 'markmin_escape']
__doc__ = '\n# Markmin markup language\n\n## About\n\nThis is a new markup language that we call markmin designed to produce high quality scientific papers and books and also put them online. We provide serializers for html, latex and pdf. It is implemented in the ``markmin2html`` function in the ``markmin2html.py``.\n\nExample of usage:\n\n``\nm = "Hello **world** [[link http://web2py.com]]"\nfrom markmin2html import markmin2html\nprint markmin2html(m)\nfrom markmin2latex import markmin2latex\nprint markmin2latex(m)\nfrom markmin2pdf import markmin2pdf # requires pdflatex\nprint markmin2pdf(m)\n``\n====================\n# This is a test block\n  with new features:\nThis is a blockquote with\na list with tables in it:\n-----------\n  This is a paragraph before list.\n  You can continue paragraph on the\n  next lines.\n\n  This is an ordered list with tables:\n  + Item 1\n  + Item 2\n  + --------\n    aa|bb|cc\n    11|22|33\n    --------:tableclass1[tableid1]\n  + Item 4\n    -----------\n     T1| T2| t3\n    ===========\n    aaa|bbb|ccc\n    ddd|fff|ggg\n    123|0  |5.0\n    -----------:tableclass1\n-----------:blockquoteclass[blockquoteid]\n\nThis this a new paragraph\nwith a followed table.\nTable has header, footer, sections,\nodd and even rows:\n-------------------------------\n**Title 1**|**Title 2**|**Title 3**\n==============================\ndata 1     | data 2    |  2.00\ndata 3     |data4(long)| 23.00\n           |data 5     | 33.50\n==============================\nNew section|New data   |  5.00\ndata 1     |data2(long)|100.45\n           |data 3     | 12.50\ndata 4     | data 5    |   .33\ndata 6     |data7(long)|  8.01\n           |data 8     |   514\n==============================\nTotal:     | 9 items   |698,79\n------------------------------:tableclass1[tableid2]\n\n## Multilevel\n   lists\n\nNow lists can be multilevel:\n\n+ Ordered item 1 on level 1.\n  You can continue item text on\n  next strings\n\n. paragraph in an item\n\n++. Ordered item 1 of sublevel 2 with\n    a paragraph (paragraph can start\n    with point after plus or minus\n    characters, e.g. **++.** or **--.**)\n\n++. This is another item. But with 3 paragraphs,\n    blockquote and sublists:\n\n.. This is the second paragraph in the item. You\n   can add paragraphs to an item, using point\n   notation, where first characters in the string\n   are sequence of points with space between\n   them and another string. For example, this\n   paragraph (in sublevel 2) starts with two points:\n   ``.. This is the second paragraph...``\n\n.. ----------\n     ### this is a blockquote in a list\n\n     You can use blockquote with headers, paragraphs,\n     tables and lists in it:\n\n     Tables can have or have not header and footer.\n     This table is defined without any header\n     and footer in it:\n     ---------------------\n     red  |fox     | 0\n     blue |dolphin | 1000\n     green|leaf    | 10000\n     ---------------------\n   ----------\n\n.. This is yet another paragraph in the item.\n\n--- This is an item of unordered list **(sublevel 3)**\n--- This is the second item of the unordered list \'\'(sublevel 3)\'\'\n\n++++++ This is a single item of ordered list in sublevel 6\n.... and this is a paragraph in sublevel 4\n---. This is a new item with paragraph in sublevel 3.\n++++ Start ordered list in sublevel 4 with code block: ``\nline 1\n  line 2\n     line 3\n``\n++++. Yet another item with code block (we need to indent \\`\\` to add code block as part of item):\n ``\n  line 1\nline 2\n  line 3\n``\n This item finishes with this paragraph.\n\n... Item in sublevel 3 can be continued with paragraphs.\n\n... ``\n  this is another\ncode block\n    in the\n  sublevel 3 item\n``\n\n+++ The last item in sublevel 3\n.. This is a continuous paragraph for item 2 in sublevel 2.\n   You can use such structure to create difficult structured\n   documents.\n\n++ item 3 in sublevel 2\n-- item 1 in sublevel 2 (new unordered list)\n-- item 2 in sublevel 2\n-- item 3 in sublevel 2\n\n++ item 1 in sublevel 2 (new ordered list)\n++ item 2 in sublevel 2\n++ item 3 in sublevle 2\n\n+ item 2 in level 1\n+ item 3 in level 1\n- new unordered list (item 1 in level 1)\n- level 2 in level 1\n\n- level 3 in level 1\n- level 4 in level 1\n## This is the last section of the test\n\nSingle paragraph with \'----\' in it will be turned into separator:\n\n-----------\n\nAnd this is the last paragraph in\nthe test. Be happy!\n\n====================\n\n## Why?\n\nWe wanted a markup language with the following requirements:\n- less than 300 lines of functional code\n- easy to read\n- secure\n- support table, ul, ol, code\n- support html5 video and audio elements (html serialization only)\n- can align images and resize them\n- can specify class for tables, blockquotes and code elements\n- can add anchors\n- does not use _ for markup (since it creates odd behavior)\n- automatically links urls\n- fast\n- easy to extend\n- supports latex and pdf including references\n- allows to describe the markup in the markup (this document is generated from markmin syntax)\n\n(results depend on text but in average for text ~100K markmin is 30% faster than markdown, for text ~10K it is 10x faster)\n\nThe [[web2py book http://www.lulu.com/product/paperback/web2py-%283rd-edition%29/12822827]] published by lulu, for example, was entirely generated with markmin2pdf from the online [[web2py wiki http://www.web2py.com/book]]\n\n## Download\n\n- http://web2py.googlecode.com/hg/gluon/contrib/markmin/markmin2html.py\n- http://web2py.googlecode.com/hg/gluon/contrib/markmin/markmin2latex.py\n- http://web2py.googlecode.com/hg/gluon/contrib/markmin/markmin2pdf.py\n\nmarkmin2html.py and markmin2latex.py are single files and have no web2py dependence. Their license is BSD.\n\n## Examples\n\n### Bold, italic, code and links\n\n------------------------------------------------------------------------------\n**SOURCE**                                    | **OUTPUT**\n==============================================================================\n``# title``                                   | **title**\n``## section``                                | **section**\n``### subsection``                            | **subsection**\n``**bold**``                                  | **bold**\n``\'\'italic\'\'``                                | \'\'italic\'\'\n``~~strikeout~~``                             | ~~strikeout~~\n``!`!`verbatim`!`!``                          | ``verbatim``\n``\\`\\`color with **bold**\\`\\`:red``           | ``color with **bold**``:red\n``\\`\\`many colors\\`\\`:color[blue:#ffff00]``   | ``many colors``:color[blue:#ffff00]\n``http://google.com``                         | http://google.com\n``[[**click** me #myanchor]]``                | [[**click** me #myanchor]]\n``[[click me [extra info] #myanchor popup]]`` | [[click me [extra info] #myanchor popup]]\n-------------------------------------------------------------------------------\n\n### More on links\n\nThe format is always ``[[title link]]`` or ``[[title [extra] link]]``. Notice you can nest bold, italic, strikeout and code inside the link ``title``.\n\n### Anchors [[myanchor]]\n\nYou can place an anchor anywhere in the text using the syntax ``[[name]]`` where \'\'name\'\' is the name of the anchor.\nYou can then link the anchor with [[link #myanchor]], i.e. ``[[link #myanchor]]`` or [[link with an extra info [extra info] #myanchor]], i.e.\n``[[link with an extra info [extra info] #myanchor]]``.\n\n### Images\n\n[[alt-string for the image [the image title] http://www.web2py.com/examples/static/web2py_logo.png right 200px]]\nThis paragraph has an image aligned to the right with a width of 200px. Its is placed using the code\n\n``[[alt-string for the image [the image title] http://www.web2py.com/examples/static/web2py_logo.png right 200px]]``.\n\n### Unordered Lists\n\n``\n- Dog\n- Cat\n- Mouse\n``\n\nis rendered as\n- Dog\n- Cat\n- Mouse\n\nTwo new lines between items break the list in two lists.\n\n### Ordered Lists\n\n``\n+ Dog\n+ Cat\n+ Mouse\n``\n\nis rendered as\n+ Dog\n+ Cat\n+ Mouse\n\n\n### Multilevel Lists\n\n``\n+ Dogs\n -- red\n -- brown\n -- black\n+ Cats\n -- fluffy\n -- smooth\n -- bald\n+ Mice\n -- small\n -- big\n -- huge\n``\n\nis rendered as\n+ Dogs\n -- red\n -- brown\n -- black\n+ Cats\n -- fluffy\n -- smooth\n -- bald\n+ Mice\n -- small\n -- big\n -- huge\n\n\n### Tables (with optional header and/or footer)\n\nSomething like this\n``\n-----------------\n**A**|**B**|**C**\n=================\n  0  |  0  |  X\n  0  |  X  |  0\n  X  |  0  |  0\n=================\n**D**|**F**|**G**\n-----------------:abc[id]\n``\nis a table and is rendered as\n-----------------\n**A**|**B**|**C**\n=================\n0 | 0 | X\n0 | X | 0\nX | 0 | 0\n=================\n**D**|**F**|**G**\n-----------------:abc[id]\nFour or more dashes delimit the table and | separates the columns.\nThe ``:abc``, ``:id[abc_1]`` or ``:abc[abc_1]`` at the end sets the class and/or id for the table and it is optional.\n\n### Blockquote\n\nA table with a single cell is rendered as a blockquote:\n\n-----\nHello world\n-----\n\nBlockquote can contain headers, paragraphs, lists and tables:\n\n``\n-----\n  This is a paragraph in a blockquote\n\n  + item 1\n  + item 2\n  -- item 2.1\n  -- item 2.2\n  + item 3\n\n  ---------\n  0 | 0 | X\n  0 | X | 0\n  X | 0 | 0\n  ---------:tableclass1\n-----\n``\n\nis rendered as:\n-----\n  This is a paragraph in a blockquote\n\n  + item 1\n  + item 2\n  -- item 2.1\n  -- item 2.2\n  + item 3\n\n  ---------\n  0 | 0 | X\n  0 | X | 0\n  X | 0 | 0\n  ---------:tableclass1\n-----\n\n\n### Code, ``<code>``, escaping and extra stuff\n\n``\ndef test():\n    return "this is Python code"\n``:python\n\nOptionally a ` inside a ``!`!`...`!`!`` block can be inserted escaped with !`!.\n\n**NOTE:** You can escape markmin constructions (\\\'\\\',\\`\\`,\\*\\*,\\~\\~,\\[,\\{,\\]\\},\\$,\\@) with \'\\\\\' character:\n so \\\\`\\\\` can replace !`!`! escape string\n\nThe ``:python`` after the markup is also optional. If present, by default, it is used to set the class of the <code> block.\nThe behavior can be overridden by passing an argument ``extra`` to the ``render`` function. For example:\n\n``\nmarkmin2html("!`!!`!aaa!`!!`!:custom",\n             extra=dict(custom=lambda text: \'x\'+text+\'x\'))\n``:python\n\ngenerates\n\n``\'xaaax\'``:python\n\n(the ``!`!`...`!`!:custom`` block is rendered by the ``custom=lambda`` function passed to ``render``).\n\n### Line breaks\n\n``[[NEWLINE]]`` tag is used to break lines:\n``\n#### Multiline [[NEWLINE]]\n   title\nparagraph [[NEWLINE]]\nwith breaks[[NEWLINE]]in it\n``\ngenerates:\n\n#### Multiline [[NEWLINE]]\n   title\nparagraph [[NEWLINE]]\nwith breaks[[NEWLINE]]in it\n\n\n### Html5 support\n\nMarkmin also supports the <video> and <audio> html5 tags using the notation:\n``\n[[message link video]]\n[[message link audio]]\n\n[[message [title] link video]]\n[[message [title] link audio]]\n``\nwhere ``message`` will be shown in browsers without HTML5 video/audio tags support.\n\n### Latex and other extensions\n\nFormulas can be embedded into HTML with \'\'\\$\\$``formula``\\$\\$\'\'.\nYou can use Google charts to render the formula:\n\n``\nLATEX = \'<img src="http://chart.apis.google.com/chart?cht=tx&chl=%s" />\'\nmarkmin2html(text,{\'latex\':lambda code: LATEX % code.replace(\'"\',\'\\\\"\')})\n``\n\n### Code with syntax highlighting\n\nThis requires a syntax highlighting tool, such as the web2py CODE helper.\n\n``\nextra={\'code_cpp\':lambda text: CODE(text,language=\'cpp\').xml(),\n       \'code_java\':lambda text: CODE(text,language=\'java\').xml(),\n       \'code_python\':lambda text: CODE(text,language=\'python\').xml(),\n       \'code_html\':lambda text: CODE(text,language=\'html\').xml()}\n``\nor simple:\n``\nextra={\'code\':lambda text,lang=\'python\': CODE(text,language=lang).xml()}\n``\n``\nmarkmin2html(text,extra=extra)\n``\n\nCode can now be marked up as in this example:\n``\n!`!`\n<html><body>example</body></html>\n!`!`:code_html\n``\nOR\n``\n!`!`\n<html><body>example</body></html>\n!`!`:code[html]\n``\n\n### Citations and References\n\nCitations are treated as internal links in html and proper citations in latex if there is a final section called "References". Items like\n\n``\n- [[key]] value\n``\n\nin the References will be translated into Latex\n\n``\n\\bibitem{key} value\n``\n\nHere is an example of usage:\n\n``\nAs shown in Ref.!`!`mdipierro`!`!:cite\n\n## References\n\n- [[mdipierro]] web2py Manual, 3rd Edition, lulu.com\n``\n\n### Caveats\n\n``<ul/>``, ``<ol/>``, ``<code/>``, ``<table/>``, ``<blockquote/>``, ``<h1/>``, ..., ``<h6/>`` do not have ``<p>...</p>`` around them.\n\n'
html_colors = ['aqua', 'black', 'blue', 'fuchsia', 'gray', 'green',
 'lime', 'maroon', 'navy', 'olive', 'purple', 'red',
 'silver', 'teal', 'white', 'yellow']
META = '\x06'
LINK = '\x07'
DISABLED_META = '\x08'
LATEX = '<img src="http://chart.apis.google.com/chart?cht=tx&chl=%s" />'
regex_URL = re.compile('@/(?P<a>\\w*)/(?P<c>\\w*)/(?P<f>\\w*(\\.\\w+)?)(/(?P<args>[\\w\\.\\-/]+))?')
regex_env2 = re.compile('@\\{(?P<a>[\\w\\-\\.]+?)(\\:(?P<b>.*?))?\\}')
regex_expand_meta = re.compile('(' + META + '|' + DISABLED_META + '|````)')
regex_dd = re.compile('\\$\\$(?P<latex>.*?)\\$\\$')
regex_code = re.compile('(' + META + '|' + DISABLED_META + '|````)|(``(?P<t>.+?)``(?::(?P<c>[a-zA-Z][_a-zA-Z\\-\\d]*)(?:\\[(?P<p>[^\\]]*)\\])?)?)', re.S)
regex_strong = re.compile('\\*\\*(?P<t>[^\\s*]+( +[^\\s*]+)*)\\*\\*')
regex_del = re.compile('~~(?P<t>[^\\s*]+( +[^\\s*]+)*)~~')
regex_em = re.compile("''(?P<t>[^\\s']+(?: +[^\\s']+)*)''")
regex_num = re.compile('^\\s*[+-]?((\\d+(\\.\\d*)?)|\\.\\d+)([eE][+-]?[0-9]+)?\\s*$')
regex_list = re.compile('^(?:(?:(#{1,6})|(?:(\\.+|\\++|\\-+)(\\.)?))\\s*)?(.*)$')
regex_bq_headline = re.compile('^(?:(\\.+|\\++|\\-+)(\\.)?\\s+)?(-{3}-*)$')
regex_tq = re.compile('^(-{3}-*)(?::(?P<c>[a-zA-Z][_a-zA-Z\\-\\d]*)(?:\\[(?P<p>[a-zA-Z][_a-zA-Z\\-\\d]*)\\])?)?$')
regex_proto = re.compile('(?<!["\\w>/=])(?P<p>\\w+):(?P<k>\\w+://[\\w\\d\\-+=?%&/:.]+)', re.M)
regex_auto = re.compile('(?<!["\\w>/=])(?P<k>\\w+://[\\w\\d\\-+_=?%&/:.,;#]+\\w)', re.M)
regex_link = re.compile('(' + LINK + ')|\\[\\[(?P<s>.+?)\\]\\]', re.S)
regex_link_level2 = re.compile('^(?P<t>\\S.*?)?(?:\\s+\\[(?P<a>.+?)\\])?(?:\\s+(?P<k>\\S+))?(?:\\s+(?P<p>popup))?\\s*$', re.S)
regex_media_level2 = re.compile('^(?P<t>\\S.*?)?(?:\\s+\\[(?P<a>.+?)\\])?(?:\\s+(?P<k>\\S+))?\\s+(?P<p>img|IMG|left|right|center|video|audio|blockleft|blockright)(?:\\s+(?P<w>\\d+px))?\\s*$', re.S)
regex_markmin_escape = re.compile("(\\\\*)(['`:*~\\\\[\\]{}@\\$+\\-.#\\n])")
regex_backslash = re.compile("\\\\(['`:*~\\\\[\\]{}@\\$+\\-.#\\n])")
ttab_in = maketrans("'`:*~\\[]{}@$+-.#\n", '\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x05')
ttab_out = maketrans('\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x05', "'`:*~\\[]{}@$+-.#\n")
regex_quote = re.compile('(?P<name>\\w+?)\\s*\\=\\s*')

def make_dict(b):
    return '{%s}' % regex_quote.sub("'\\g<name>':", b)


def safe_eval(node_or_string, env):
    """
    Safely evaluate an expression node or a string containing a Python
    expression.  The string or node provided may only consist of the following
    Python literal structures: strings, numbers, tuples, lists, dicts, booleans,
    and None.
    """
    _safe_names = {'None': None, 'True': True, 'False': False}
    _safe_names.update(env)
    if isinstance(node_or_string, basestring):
        node_or_string = ast_parse(node_or_string, mode='eval')
    if isinstance(node_or_string, ast.Expression):
        node_or_string = node_or_string.body

    def _convert(node):
        if isinstance(node, ast.Str):
            return node.s
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.Tuple):
            return tuple(map(_convert, node.elts))
        if isinstance(node, ast.List):
            return list(map(_convert, node.elts))
        if isinstance(node, ast.Dict):
            return dict((_convert(k), _convert(v)) for k, v in zip(node.keys, node.values))
        if isinstance(node, ast.Name):
            if node.id in _safe_names:
                return _safe_names[node.id]
        elif isinstance(node, ast.BinOp) and isinstance(node.op, (Add, Sub)) and isinstance(node.right, Num) and isinstance(node.right.n, complex) and isinstance(node.left, Num):
            if isinstance(node.left.n, (int, long, float)):
                left = node.left.n
                right = node.right.n
                if isinstance(node.op, Add):
                    return left + right
                return left - right
        raise ValueError('malformed string')

    return _convert(node_or_string)


def markmin_escape(text):
    r""" insert \ before markmin control characters: '`:*~[]{}@$ """
    return regex_markmin_escape.sub(lambda m: '\\' + m.group(0).replace('\\', '\\\\'), text)


def replace_autolinks(text, autolinks):
    return regex_auto.sub(lambda m: autolinks(m.group('k')), text)


def replace_at_urls(text, url):

    def u1(match, url=url):
        a, c, f, args = match.group('a', 'c', 'f', 'args')
        return url(a=a or None, c=c or None, f=f or None, args=(args or '').split('/'), scheme=True, host=True)

    return regex_URL.sub(u1, text)


def replace_components(text, env):

    def u2(match, env=env):
        f = env.get(match.group('a'), match.group(0))
        if callable(f):
            b = match.group('b')
            try:
                b = safe_eval(make_dict(b), env)
            except:
                pass

            try:
                f = f(**b) if isinstance(b, dict) else f(b)
            except Exception as e:
                f = 'ERROR: %s' % e

            return str(f)

    text = regex_env2.sub(u2, text)
    return text


def autolinks_simple(url):
    """
    it automatically converts the url to link,
    image, video or audio tag
    """
    u_url = url.lower()
    if u_url.endswith(('.jpg', '.jpeg', '.gif', '.png')):
        return '<img src="%s" controls />' % url
    if u_url.endswith(('.mp4', '.mpeg', '.mov', '.ogv')):
        return '<video src="%s" controls></video>' % url
    if u_url.endswith(('.mp3', '.wav', '.ogg')):
        return '<audio src="%s" controls></audio>' % url
    return '<a href="%s">%s</a>' % (url, url)


def protolinks_simple(proto, url):
    """
    it converts url to html-string using appropriate proto-prefix:
    Uses for construction "proto:url", e.g.:
        "iframe:http://www.example.com/path" will call protolinks()
        with parameters:
            proto="iframe"
            url="http://www.example.com/path"
    """
    if proto in ('iframe', 'embed'):
        return '<iframe src="%s" frameborder="0" allowfullscreen></iframe>' % url
    if proto == 'qr':
        return '<img style="width:100px" src="http://chart.apis.google.com/chart?cht=qr&chs=100x100&chl=%s&choe=UTF-8&chld=H" alt="QR Code" title="QR Code" />' % url
    return proto + ':' + url


def render(text, extra={}, allowed={}, sep='p', URL=None, environment=None, latex='google', autolinks='default', protolinks='default', class_prefix='', id_prefix='markmin_', pretty_print=False):
    r"""
    Arguments:
    - text is the text to be processed
    - extra is a dict like extra=dict(custom=lambda value: value) that process custom code
      as in " ``this is custom code``:custom "
    - allowed is a dictionary of list of allowed classes like
      allowed = dict(code=('python','cpp','java'))
    - sep can be 'p' to separate text in <p>...</p>
      or can be 'br' to separate text using <br />
    - URL -
    - environment is a dictionary of environment variables (can be accessed with @{variable}
    - latex -
    - autolinks is a function to convert auto urls to html-code (default is autolinks(url) )
    - protolinks is a function to convert proto-urls (e.g."proto:url") to html-code
      (default is protolinks(proto,url))
    - class_prefix is a prefix for ALL classes in markmin text. E.g. if class_prefix='my_'
      then for ``test``:cls class will be changed to "my_cls" (default value is '')
    - id_prefix is prefix for ALL ids in markmin text (default value is 'markmin_'). E.g.:
        -- [[id]] will be converted to <span class="anchor" id="markmin_id"></span>
        -- [[link #id]] will be converted to <a href="#markmin_id">link</a>
        -- ``test``:cls[id] will be converted to <code class="cls" id="markmin_id">test</code>

    >>> render('this is\n# a section\n\nparagraph')
    '<p>this is</p><h1>a section</h1><p>paragraph</p>'
    >>> render('this is\n## a subsection\n\nparagraph')
    '<p>this is</p><h2>a subsection</h2><p>paragraph</p>'
    >>> render('this is\n### a subsubsection\n\nparagraph')
    '<p>this is</p><h3>a subsubsection</h3><p>paragraph</p>'
    >>> render('**hello world**')
    '<p><strong>hello world</strong></p>'
    >>> render('``hello world``')
    '<code>hello world</code>'
    >>> render('``hello world``:python')
    '<code class="python">hello world</code>'
    >>> render('``\nhello\nworld\n``:python')
    '<pre><code class="python">hello\nworld</code></pre>'
    >>> render('``hello world``:python[test_id]')
    '<code class="python" id="markmin_test_id">hello world</code>'
    >>> render('``hello world``:id[test_id]')
    '<code id="markmin_test_id">hello world</code>'
    >>> render('``\nhello\nworld\n``:python[test_id]')
    '<pre><code class="python" id="markmin_test_id">hello\nworld</code></pre>'
    >>> render('``\nhello\nworld\n``:id[test_id]')
    '<pre><code id="markmin_test_id">hello\nworld</code></pre>'
    >>> render("''hello world''")
    '<p><em>hello world</em></p>'
    >>> render('** hello** **world**')
    '<p>** hello** <strong>world</strong></p>'

    >>> render('- this\n- is\n- a list\n\nand this\n- is\n- another')
    '<ul><li>this</li><li>is</li><li>a list</li></ul><p>and this</p><ul><li>is</li><li>another</li></ul>'

    >>> render('+ this\n+ is\n+ a list\n\nand this\n+ is\n+ another')
    '<ol><li>this</li><li>is</li><li>a list</li></ol><p>and this</p><ol><li>is</li><li>another</li></ol>'

    >>> render("----\na | b\nc | d\n----\n")
    '<table><tbody><tr class="first"><td>a</td><td>b</td></tr><tr class="even"><td>c</td><td>d</td></tr></tbody></table>'

    >>> render("----\nhello world\n----\n")
    '<blockquote>hello world</blockquote>'

    >>> render('[[myanchor]]')
    '<p><span class="anchor" id="markmin_myanchor"></span></p>'

    >>> render('[[ http://example.com]]')
    '<p><a href="http://example.com">http://example.com</a></p>'

    >>> render('[[bookmark [http://example.com] ]]')
    '<p><span class="anchor" id="markmin_bookmark"><a href="http://example.com">http://example.com</a></span></p>'

    >>> render('[[this is a link http://example.com]]')
    '<p><a href="http://example.com">this is a link</a></p>'

    >>> render('[[this is an image http://example.com left]]')
    '<p><img src="http://example.com" alt="this is an image" style="float:left" /></p>'

    >>> render('[[this is an image http://example.com left 200px]]')
    '<p><img src="http://example.com" alt="this is an image" style="float:left;width:200px" /></p>'

    >>> render("[[Your browser doesn't support <video> HTML5 tag http://example.com video]]")
    '<p><video controls="controls"><source src="http://example.com" />Your browser doesn\'t support &lt;video&gt; HTML5 tag</video></p>'

    >>> render("[[Your browser doesn't support <audio> HTML5 tag http://example.com audio]]")
    '<p><audio controls="controls"><source src="http://example.com" />Your browser doesn\'t support &lt;audio&gt; HTML5 tag</audio></p>'

    >>> render("[[Your\nbrowser\ndoesn't\nsupport\n<audio> HTML5 tag http://exam\\\nple.com\naudio]]")
    '<p><audio controls="controls"><source src="http://example.com" />Your browser doesn\'t support &lt;audio&gt; HTML5 tag</audio></p>'

    >>> render('[[this is a **link** http://example.com]]')
    '<p><a href="http://example.com">this is a <strong>link</strong></a></p>'

    >>> render("``aaa``:custom", extra=dict(custom=lambda text: 'x'+text+'x'))
    'xaaax'

    >>> print render(r"$$\int_a^b sin(x)dx$$")
    <img src="http://chart.apis.google.com/chart?cht=tx&chl=\int_a^b sin(x)dx" />

    >>> markmin2html(r"use backslash: \[\[[[mess\[[ag\]]e link]]\]]")
    '<p>use backslash: [[<a href="link">mess[[ag]]e</a>]]</p>'

    >>> markmin2html("backslash instead of exclamation sign: \``probe``")
    '<p>backslash instead of exclamation sign: ``probe``</p>'

    >>> render(r"simple image: [[\[[this is an image\]] http://example.com IMG]]!!!")
    '<p>simple image: <img src="http://example.com" alt="[[this is an image]]" />!!!</p>'

    >>> render(r"simple link no anchor with popup: [[ http://example.com popup]]")
    '<p>simple link no anchor with popup: <a href="http://example.com" target="_blank">http://example.com</a></p>'

    >>> render("auto-url: http://example.com")
    '<p>auto-url: <a href="http://example.com">http://example.com</a></p>'

    >>> render("auto-image: (http://example.com/image.jpeg)")
    '<p>auto-image: (<img src="http://example.com/image.jpeg" controls />)</p>'

    >>> render("qr: (qr:http://example.com/image.jpeg)")
    '<p>qr: (<img style="width:100px" src="http://chart.apis.google.com/chart?cht=qr&chs=100x100&chl=http://example.com/image.jpeg&choe=UTF-8&chld=H" alt="QR Code" title="QR Code" />)</p>'

    >>> render("embed: (embed:http://example.com/page)")
    '<p>embed: (<iframe src="http://example.com/page" frameborder="0" allowfullscreen></iframe>)</p>'

    >>> render("iframe: (iframe:http://example.com/page)")
    '<p>iframe: (<iframe src="http://example.com/page" frameborder="0" allowfullscreen></iframe>)</p>'

    >>> render("title1: [[test message [simple \[test\] title] http://example.com ]] test")
    '<p>title1: <a href="http://example.com" title="simple [test] title">test message</a> test</p>'

    >>> render("title2: \[\[[[test message [simple title] http://example.com popup]]\]]")
    '<p>title2: [[<a href="http://example.com" title="simple title" target="_blank">test message</a>]]</p>'

    >>> render("title3: [[ [link w/o anchor but with title] http://www.example.com ]]")
    '<p>title3: <a href="http://www.example.com" title="link w/o anchor but with title">http://www.example.com</a></p>'

    >>> render("title4: [[ [simple title] http://www.example.com popup]]")
    '<p>title4: <a href="http://www.example.com" title="simple title" target="_blank">http://www.example.com</a></p>'

    >>> render("title5: [[test message [simple title] http://example.com IMG]]")
    '<p>title5: <img src="http://example.com" alt="test message" title="simple title" /></p>'

    >>> render("title6: [[[test message w/o title] http://example.com IMG]]")
    '<p>title6: <img src="http://example.com" alt="[test message w/o title]" /></p>'

    >>> render("title7: [[[this is not a title] [this is a title] http://example.com IMG]]")
    '<p>title7: <img src="http://example.com" alt="[this is not a title]" title="this is a title" /></p>'

    >>> render("title8: [[test message [title] http://example.com center]]")
    '<p>title8: <p style="text-align:center"><img src="http://example.com" alt="test message" title="title" /></p></p>'

    >>> render("title9: [[test message [title] http://example.com left]]")
    '<p>title9: <img src="http://example.com" alt="test message" title="title" style="float:left" /></p>'

    >>> render("title10: [[test message [title] http://example.com right 100px]]")
    '<p>title10: <img src="http://example.com" alt="test message" title="title" style="float:right;width:100px" /></p>'

    >>> render("title11: [[test message [title] http://example.com center 200px]]")
    '<p>title11: <p style="text-align:center"><img src="http://example.com" alt="test message" title="title" style="width:200px" /></p></p>'

    >>> render(r"\[[probe]]")
    '<p>[[probe]]</p>'

    >>> render(r"\\[[probe]]")
    '<p>\\<span class="anchor" id="markmin_probe"></span></p>'

    >>> render(r"\\\[[probe]]")
    '<p>\\[[probe]]</p>'

    >>> render(r"\\\\[[probe]]")
    '<p>\\\\<span class="anchor" id="markmin_probe"></span></p>'

    >>> render(r"\\\\\[[probe]]")
    '<p>\\\\[[probe]]</p>'

    >>> render(r"\\\\\\[[probe]]")
    '<p>\\\\\\<span class="anchor" id="markmin_probe"></span></p>'

    >>> render("``[[ [\[[probe\]\]] URL\[x\]]]``:red[dummy_params]")
    '<span style="color: red"><a href="URL[x]" title="[[probe]]">URL[x]</a></span>'

    >>> render("the \**text**")
    '<p>the **text**</p>'

    >>> render("the \``text``")
    '<p>the ``text``</p>'

    >>> render("the \\''text''")
    "<p>the ''text''</p>"

    >>> render("the [[link [**with** ``<b>title</b>``:red] http://www.example.com]]")
    '<p>the <a href="http://www.example.com" title="**with** ``&lt;b&gt;title&lt;/b&gt;``:red">link</a></p>'

    >>> render("the [[link \[**without** ``<b>title</b>``:red\] http://www.example.com]]")
    '<p>the <a href="http://www.example.com">link [<strong>without</strong> <span style="color: red">&lt;b&gt;title&lt;/b&gt;</span>]</a></p>'

    >>> render("aaa-META-``code``:text[]-LINK-[[link http://www.example.com]]-LINK-[[image http://www.picture.com img]]-end")
    '<p>aaa-META-<code class="text">code</code>-LINK-<a href="http://www.example.com">link</a>-LINK-<img src="http://www.picture.com" alt="image" />-end</p>'

    >>> render("[[<a>test</a> [<a>test2</a>] <a>text3</a>]]")
    '<p><a href="&lt;a&gt;text3&lt;/a&gt;" title="&lt;a&gt;test2&lt;/a&gt;">&lt;a&gt;test&lt;/a&gt;</a></p>'

    >>> render("[[<a>test</a> [<a>test2</a>] <a>text3</a> IMG]]")
    '<p><img src="&lt;a&gt;text3&lt;/a&gt;" alt="&lt;a&gt;test&lt;/a&gt;" title="&lt;a&gt;test2&lt;/a&gt;" /></p>'

    >>> render("**bold** ''italic'' ~~strikeout~~")
    '<p><strong>bold</strong> <em>italic</em> <del>strikeout</del></p>'

    >>> render("this is ``a red on yellow text``:c[#FF0000:#FFFF00]")
    '<p>this is <span style="color: #FF0000;background-color: #FFFF00;">a red on yellow text</span></p>'

    >>> render("this is ``a text with yellow background``:c[:yellow]")
    '<p>this is <span style="background-color: yellow;">a text with yellow background</span></p>'

    >>> render("this is ``a colored text (RoyalBlue)``:color[rgb(65,105,225)]")
    '<p>this is <span style="color: rgb(65,105,225);">a colored text (RoyalBlue)</span></p>'

    >>> render("this is ``a green text``:color[green:]")
    '<p>this is <span style="color: green;">a green text</span></p>'

    >>> render("**@{probe:1}**", environment=dict(probe=lambda t:"test %s" % t))
    '<p><strong>test 1</strong></p>'

    >>> render("**@{probe:t=a}**", environment=dict(probe=lambda t:"test %s" % t, a=1))
    '<p><strong>test 1</strong></p>'

    >>> render('[[id1 [span **messag** in ''markmin''] ]] ... [[**link** to id [link\'s title] #mark1]]')
    '<p><span class="anchor" id="markmin_id1">span <strong>messag</strong> in markmin</span> ... <a href="#markmin_mark1" title="link\'s title"><strong>link</strong> to id</a></p>'

    >>> render('# Multiline[[NEWLINE]]\n title\nParagraph[[NEWLINE]]\nwith breaks[[NEWLINE]]\nin it')
    '<h1>Multiline<br /> title</h1><p>Paragraph<br /> with breaks<br /> in it</p>'

    >>> render("anchor with name 'NEWLINE': [[NEWLINE [ ] ]]")
    '<p>anchor with name \'NEWLINE\': <span class="anchor" id="markmin_NEWLINE"></span></p>'

    >>> render("anchor with name 'NEWLINE': [[NEWLINE [newline] ]]")
    '<p>anchor with name \'NEWLINE\': <span class="anchor" id="markmin_NEWLINE">newline</span></p>'
    """
    if autolinks == 'default':
        autolinks = autolinks_simple
    if protolinks == 'default':
        protolinks = protolinks_simple
    pp = '\n' if pretty_print else ''
    if isinstance(text, unicode):
        text = text.encode('utf8')
    text = str(text or '')
    text = regex_backslash.sub(lambda m: m.group(1).translate(ttab_in), text)
    text = text.replace('\x05', '')
    if URL is not None:
        text = replace_at_urls(text, URL)
    if latex == 'google':
        text = regex_dd.sub('``\\g<latex>``:latex ', text)
    segments = []

    def mark_code(m):
        g = m.group(0)
        if g in (META, DISABLED_META):
            segments.append((None, None, None, g))
            return m.group()
        else:
            if g == '````':
                segments.append((None, None, None, ''))
                return m.group()
            c = m.group('c') or ''
            p = m.group('p') or ''
            if 'code' in allowed and c not in allowed['code']:
                c = ''
            code = m.group('t').replace('!`!', '`')
            segments.append((code, c, p, m.group(0)))
            return META

    text = regex_code.sub(mark_code, text)
    links = []

    def mark_link(m):
        links.append(None if m.group() == LINK else m.group('s'))
        return LINK

    text = regex_link.sub(mark_link, text)
    text = escape(text)
    if protolinks:
        text = regex_proto.sub(lambda m: protolinks(*m.group('p', 'k')), text)
    if autolinks:
        text = replace_autolinks(text, autolinks)
    strings = text.split('\n')

    def parse_title(t, s):
        hlevel = str(len(t))
        out.extend(etags[::-1])
        out.append('<h%s>%s' % (hlevel, s))
        etags[:] = ['</h%s>%s' % (hlevel, pp)]
        lev = 0
        ltags[:] = []
        tlev[:] = []
        return (lev, 'h')

    def parse_list(t, p, s, tag, lev, mtag, lineno):
        lent = len(t)
        if lent < lev:
            while ltags[(-1)] > lent:
                ltags.pop()
                out.append(etags.pop())

            lev = lent
            tlev[lev:] = []
        if lent > lev:
            if lev == 0:
                out.extend(etags[::-1])
                ltags[:] = []
                tlev[:] = []
                etags[:] = []
            if pend and mtag == '.':
                out.append(etags.pop())
                ltags.pop()
            for i in xrange(lent - lev):
                out.append('<' + tag + '>' + pp)
                etags.append('</' + tag + '>' + pp)
                lev += 1
                ltags.append(lev)
                tlev.append(tag)

        elif lent == lev:
            if tlev[(-1)] != tag:
                for i in xrange(ltags.count(lent)):
                    ltags.pop()
                    out.append(etags.pop())

                tlev[-1] = tag
                out.append('<' + tag + '>' + pp)
                etags.append('</' + tag + '>' + pp)
                ltags.append(lev)
            elif ltags.count(lev) > 1:
                out.append(etags.pop())
                ltags.pop()
        mtag = 'l'
        out.append('<li>')
        etags.append('</li>' + pp)
        ltags.append(lev)
        if s[:1] == '-':
            s, mtag, lineno = parse_table_or_blockquote(s, mtag, lineno)
        if p and mtag == 'l':
            lev, mtag, lineno = parse_point(t, s, lev, '', lineno)
        else:
            out.append(s)
        return (lev, mtag, lineno)

    def parse_point(t, s, lev, mtag, lineno):
        """ paragraphs in lists """
        lent = len(t)
        if lent > lev:
            return parse_list(t, '.', s, 'ul', lev, mtag, lineno)
        if lent < lev:
            while ltags[(-1)] > lent:
                ltags.pop()
                out.append(etags.pop())

            lev = lent
            tlev[lev:] = []
            mtag = ''
        elif lent == lev:
            if pend and mtag == '.':
                out.append(etags.pop())
                ltags.pop()
        if br and mtag in ('l', '.'):
            out.append(br)
        if s == META:
            mtag = ''
        else:
            mtag = '.'
            if s[:1] == '-':
                s, mtag, lineno = parse_table_or_blockquote(s, mtag, lineno)
            if mtag == '.':
                out.append(pbeg)
                if pend:
                    etags.append(pend)
                    ltags.append(lev)
        out.append(s)
        return (lev, mtag, lineno)

    def parse_table_or_blockquote(s, mtag, lineno):
        if lineno + 1 >= strings_len or not (s.count('-') == len(s) and len(s) > 3):
            return (s, mtag, lineno)
        lineno += 1
        s = strings[lineno].strip()
        if s:
            if '|' in s:
                tout = []
                thead = []
                tbody = []
                rownum = 0
                t_id = ''
                t_cls = ''
                while lineno < strings_len:
                    s = strings[lineno].strip()
                    if s[:1] == '=':
                        if s.count('=') == len(s) and len(s) > 3:
                            if not thead:
                                thead = tout
                            else:
                                tbody.extend(tout)
                            tout = []
                            rownum = 0
                            lineno += 1
                            continue
                    m = regex_tq.match(s)
                    if m:
                        t_cls = m.group('c') or ''
                        t_id = m.group('p') or ''
                        break
                    if rownum % 2:
                        tr = '<tr class="even">'
                    else:
                        tr = '<tr class="first">' if rownum == 0 else '<tr>'
                    tout.append(tr + ('').join([ '<td%s>%s</td>' % (' class="num"' if regex_num.match(f) else '', f.strip()) for f in s.split('|') ]) + '</tr>' + pp)
                    rownum += 1
                    lineno += 1

                t_cls = ' class="%s%s"' % (class_prefix, t_cls) if t_cls and t_cls != 'id' else ''
                t_id = ' id="%s%s"' % (id_prefix, t_id) if t_id else ''
                s = ''
                if thead:
                    s += '<thead>' + pp + ('').join([ l for l in thead ]) + '</thead>' + pp
                if not tbody:
                    tbody = tout
                    tout = []
                if tbody:
                    s += '<tbody>' + pp + ('').join([ l for l in tbody ]) + '</tbody>' + pp
                if tout:
                    s += '<tfoot>' + pp + ('').join([ l for l in tout ]) + '</tfoot>' + pp
                s = '<table%s%s>%s%s</table>%s' % (t_cls, t_id, pp, s, pp)
                mtag = 't'
            else:
                bq_begin = lineno
                t_mode = False
                t_cls = ''
                t_id = ''
                while lineno < strings_len:
                    s = strings[lineno].strip()
                    if not t_mode:
                        m = regex_tq.match(s)
                        if m:
                            if lineno + 1 == strings_len or '|' not in strings[(lineno + 1)]:
                                t_cls = m.group('c') or ''
                                t_id = m.group('p') or ''
                                break
                        if regex_bq_headline.match(s):
                            if lineno + 1 < strings_len and strings[(lineno + 1)].strip():
                                t_mode = True
                            lineno += 1
                            continue
                    elif regex_tq.match(s):
                        t_mode = False
                        lineno += 1
                        continue
                    lineno += 1

                t_cls = ' class="%s%s"' % (class_prefix, t_cls) if t_cls and t_cls != 'id' else ''
                t_id = ' id="%s%s"' % (id_prefix, t_id) if t_id else ''
                s = '<blockquote%s%s>%s</blockquote>%s' % (
                 t_cls,
                 t_id,
                 ('\n').join(strings[bq_begin:lineno]), pp)
                mtag = 'q'
        else:
            s = '<hr />'
            lineno -= 1
            mtag = 'q'
        return (
         s, 'q', lineno)

    if sep == 'p':
        pbeg = '<p>'
        pend = '</p>' + pp
        br = ''
    else:
        pbeg = pend = ''
        br = '<br />' + pp if sep == 'br' else ''
    lev = 0
    c0 = ''
    out = []
    etags = []
    ltags = []
    tlev = []
    mtag = ''
    lineno = 0
    strings_len = len(strings)
    while lineno < strings_len:
        s0 = strings[lineno][:1]
        s = strings[lineno].strip()
        pc0 = c0
        c0 = s[:1]
        if c0:
            if c0 in '#+-.':
                t1, t2, p, ss = regex_list.findall(s)[0]
                if t1 or t2:
                    if c0 == '#':
                        lev, mtag = parse_title(t1, ss)
                        lineno += 1
                        continue
                    elif c0 == '+':
                        lev, mtag, lineno = parse_list(t2, p, ss, 'ol', lev, mtag, lineno)
                        lineno += 1
                        continue
                    elif c0 == '-':
                        if p or ss:
                            lev, mtag, lineno = parse_list(t2, p, ss, 'ul', lev, mtag, lineno)
                            lineno += 1
                            continue
                        else:
                            s, mtag, lineno = parse_table_or_blockquote(s, mtag, lineno)
                    elif lev > 0:
                        lev, mtag, lineno = parse_point(t2, ss, lev, mtag, lineno)
                        lineno += 1
                        continue
            if lev == 0 and (mtag == 'q' or s == META):
                pc0 = ''
            if pc0 == '' or mtag != 'p' and s0 not in (' ', '\t'):
                out.extend(etags[::-1])
                etags = []
                ltags = []
                tlev = []
                lev = 0
                if br and mtag == 'p':
                    out.append(br)
                if mtag != 'q' and s != META:
                    if pend:
                        etags = [pend]
                    out.append(pbeg)
                    mtag = 'p'
                else:
                    mtag = ''
                out.append(s)
            elif lev > 0 and mtag == '.' and s == META:
                out.append(etags.pop())
                ltags.pop()
                out.append(s)
                mtag = ''
            else:
                out.append(' ' + s)
        lineno += 1

    out.extend(etags[::-1])
    text = ('').join(out)
    text = regex_strong.sub('<strong>\\g<t></strong>', text)
    text = regex_del.sub('<del>\\g<t></del>', text)
    text = regex_em.sub('<em>\\g<t></em>', text)

    def sub_media(m):
        t, a, k, p, w = m.group('t', 'a', 'k', 'p', 'w')
        if not k:
            return m.group(0)
        k = escape(k)
        t = t or ''
        style = 'width:%s' % w if w else ''
        title = ' title="%s"' % escape(a).replace(META, DISABLED_META) if a else ''
        p_begin = p_end = ''
        if p == 'center':
            p_begin = '<p style="text-align:center">'
            p_end = '</p>' + pp
        else:
            if p == 'blockleft':
                p_begin = '<p style="text-align:left">'
                p_end = '</p>' + pp
            elif p == 'blockright':
                p_begin = '<p style="text-align:right">'
                p_end = '</p>' + pp
            elif p in ('left', 'right'):
                style = 'float:%s' % p + (';%s' % style if style else '')
            if t and regex_auto.match(t):
                p_begin = p_begin + '<a href="%s">' % t
                p_end = '</a>' + p_end
                t = ''
            if style:
                style = ' style="%s"' % style
            if p in ('video', 'audio'):
                t = render(t, {}, {}, 'br', URL, environment, latex, autolinks, protolinks, class_prefix, id_prefix, pretty_print)
                return '<%(p)s controls="controls"%(title)s%(style)s><source src="%(k)s" />%(t)s</%(p)s>' % dict(p=p, title=title, style=style, k=k, t=t)
        alt = ' alt="%s"' % escape(t).replace(META, DISABLED_META) if t else ''
        return '%(begin)s<img src="%(k)s"%(alt)s%(title)s%(style)s />%(end)s' % dict(begin=p_begin, k=k, alt=alt, title=title, style=style, end=p_end)

    def sub_link(m):
        t, a, k, p = m.group('t', 'a', 'k', 'p')
        if not k and not t:
            return m.group(0)
        else:
            t = t or ''
            a = escape(a) if a else ''
            if k:
                if '#' in k and ':' not in k.split('#')[0]:
                    k = k.replace('#', '#' + id_prefix)
                k = escape(k)
                title = ' title="%s"' % a.replace(META, DISABLED_META) if a else ''
                target = ' target="_blank"' if p == 'popup' else ''
                t = render(t, {}, {}, 'br', URL, environment, latex, None, None, class_prefix, id_prefix, pretty_print) if t else k
                return '<a href="%(k)s"%(title)s%(target)s>%(t)s</a>' % dict(k=k, title=title, target=target, t=t)
            if t == 'NEWLINE' and not a:
                return '<br />' + pp
            return '<span class="anchor" id="%s">%s</span>' % (
             escape(id_prefix + t),
             render(a, {}, {}, 'br', URL, environment, latex, autolinks, protolinks, class_prefix, id_prefix, pretty_print))

    parts = text.split(LINK)
    text = parts[0]
    for i, s in enumerate(links):
        if s == None:
            html = LINK
        else:
            html = regex_media_level2.sub(sub_media, s)
            if html == s:
                html = regex_link_level2.sub(sub_link, html)
            if html == s:
                html = '[[%s]]' % s
        text += html + parts[(i + 1)]

    def expand_meta(m):
        code, b, p, s = segments.pop(0)
        if code == None or m.group() == DISABLED_META:
            return escape(s)
        else:
            if b in extra:
                if code[:1] == '\n':
                    code = code[1:]
                if code[-1:] == '\n':
                    code = code[:-1]
                if p:
                    return str(extra[b](code, p))
                return str(extra[b](code))
            else:
                if b == 'cite':
                    return '[' + (',').join('<a href="#%s" class="%s">%s</a>' % (id_prefix + d, b, d) for d in escape(code).split(',')) + ']'
                if b == 'latex':
                    return LATEX % code.replace('"', '"').replace('\n', ' ')
                if b in html_colors:
                    return '<span style="color: %s">%s</span>' % (
                     b,
                     render(code, {}, {}, 'br', URL, environment, latex, autolinks, protolinks, class_prefix, id_prefix, pretty_print))
                if b in ('c', 'color') and p:
                    c = p.split(':')
                    fg = 'color: %s;' % c[0] if c[0] else ''
                    bg = 'background-color: %s;' % c[1] if len(c) > 1 and c[1] else ''
                    return '<span style="%s%s">%s</span>' % (
                     fg, bg,
                     render(code, {}, {}, 'br', URL, environment, latex, autolinks, protolinks, class_prefix, id_prefix, pretty_print))
            cls = ' class="%s%s"' % (class_prefix, b) if b and b != 'id' else ''
            id = ' id="%s%s"' % (id_prefix, escape(p)) if p else ''
            beg = code[:1] == '\n'
            end = [None, -1][(code[-1:] == '\n')]
            if beg and end:
                return '<pre><code%s%s>%s</code></pre>%s' % (cls, id, escape(code[1:-1]), pp)
            return '<code%s%s>%s</code>' % (cls, id, escape(code[beg:end]))

    text = regex_expand_meta.sub(expand_meta, text)
    if environment:
        text = replace_components(text, environment)
    return text.translate(ttab_out)


def markmin2html(text, extra={}, allowed={}, sep='p', autolinks='default', protolinks='default', class_prefix='', id_prefix='markmin_', pretty_print=False):
    return render(text, extra, allowed, sep, autolinks=autolinks, protolinks=protolinks, class_prefix=class_prefix, id_prefix=id_prefix, pretty_print=pretty_print)


def run_doctests():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    import sys, doctest
    from textwrap import dedent
    html = dedent('\n         <!doctype html>\n         <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n         <head>\n         <meta http-equiv="content-type" content="text/html; charset=utf-8" />\n         %(style)s\n         <title>%(title)s</title>\n         </head>\n         <body>\n         %(body)s\n         </body>\n         </html>')[1:]
    if sys.argv[1:2] == ['-h']:
        style = dedent('\n              <style>\n                blockquote { background-color: #FFFAAE; padding: 7px; }\n                table { border-collapse: collapse; }\n                thead td { border-bottom: 1px solid; }\n                tfoot td { border-top: 1px solid; }\n                .tableclass1 { background-color: lime; }\n                .tableclass1 thead { color: yellow; background-color: green; }\n                .tableclass1 tfoot { color: yellow; background-color: green; }\n                .tableclass1 .even td { background-color: #80FF7F; }\n                .tableclass1 .first td {border-top: 1px solid; }\n\n                td.num { text-align: right; }\n                pre { background-color: #E0E0E0; padding: 5px; }\n              </style>')[1:]
        print html % dict(title='Markmin markup language', style=style, body=markmin2html(__doc__, pretty_print=True))
    elif sys.argv[1:2] == ['-t']:
        from timeit import Timer
        loops = 1000
        ts = Timer('markmin2html(__doc__)', 'from markmin2html import markmin2html')
        print 'timeit "markmin2html(__doc__)":'
        t = min([ ts.timeit(loops) for i in range(3) ])
        print '%s loops, best of 3: %.3f ms per loop' % (loops, t / 1000 * loops)
    elif len(sys.argv) > 1:
        fargv = open(sys.argv[1], 'r')
        try:
            markmin_text = fargv.read()
            if len(sys.argv) > 2:
                if sys.argv[2].startswith('@'):
                    markmin_style = '<link rel="stylesheet" href="' + sys.argv[2][1:] + '"/>'
                else:
                    fargv2 = open(sys.argv[2], 'r')
                    try:
                        markmin_style = '<style>\n' + fargv2.read() + '</style>'
                    finally:
                        fargv2.close()

            else:
                markmin_style = ''
            print html % dict(title=sys.argv[1], style=markmin_style, body=markmin2html(markmin_text, pretty_print=True))
        finally:
            fargv.close()

    else:
        print 'Usage: ' + sys.argv[0] + ' -h | -t | file.markmin [file.css|@path_to/css]'
        print 'where: -h  - print __doc__'
        print '       -t  - timeit __doc__ (for testing purpuse only)'
        print '       file.markmin  [file.css] - process file.markmin + built in file.css (optional)'
        print '       file.markmin  [@path_to/css] - process file.markmin + link path_to/css (optional)'
        run_doctests()