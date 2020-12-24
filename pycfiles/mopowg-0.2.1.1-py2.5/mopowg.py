# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/mopowg/mopowg.py
# Compiled at: 2007-08-02 04:13:45
r"""
mopowg
======

mopowg is an easy to install, cross-platform doc generator which is based on docutils.

mopowg could generate full documents with figures, styles, and syntax highlighting blocks.

fredlin 2007, gasolin+mopowg@gmail.com

    - Scanner
    - Generator
        - Convertor
            - Formater
                - high_lighter
        - Processor
            - Templater (genshi)
            - Saver
                - css_writer

----

doc processing
--------------

Diagram::

    ___________
    |         |
    |  files  |
    |         |
   \|_________|/
    \         /
      Scanner  -> file_list
        |||
     Generator - Formater -> contents
        |||
     Processor   -> files (content, presentation)
        \|/
    ___________
    |         |
    |   docs  |
    |         |
    |_________|

----

doc hosting[1]
--------------

Runner is the build in server which host the documents;

Plugins:

Interpreter is the crunchy interpreter that allow you to execute the demo codes on doc;

Commenter is append fields for comment

Diagram::

    ___________
    |         |
    |  files  |
    |         |
    |_________|
         |
  ----------------
  |doc processing|
  ----------------
         |
       Runner - plugins
                   |
                   |- Interpreter
                   |
                   |_ Commenter

----

doc collaborative [1]
---------------------

Diagram::

    ___________
    |         |
    |  files  |--hg repository
    |         |
    |_________|
         |
  ----------------
  |doc processing|
  ----------------
         |         
  ----------------
  | doc hosting  |
  ----------------
         |
       wikier

----

[1]: not implemented yet

----

This is the MIT license:
http://www.opensource.org/licenses/mit-license.php

Copyright (c) 2007 Fred Lin and contributors. Mopowg is a trademark of Fred Lin.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os

def proc_dir(file_list, dirName, files):
    """
    The callback function of os.path.walk() to get the list of scanned
    files.
    """
    for i in files:
        fn = os.path.join(dirName, i)
        if os.path.isdir(fn):
            continue
        elif os.path.isfile(fn):
            file_list.append(fn)


def scanner(path=None):
    """scan a folder
    
    scanner is a preprocess class to collect files
    
    scanner currently allow single layer only
    """
    if path:
        if os.path.isdir(path):
            pass
        else:
            path = os.path.join(os.getcwd, path)
    else:
        path = os.getcwd()
    file_list = []
    os.path.walk(path, proc_dir, file_list)
    return file_list


default_style = 'body {\n    margin: 0;\n    padding: 0;\n    font-family: Verdana, "Lucida Grande", sans-serif;\n    text-align: left; \n    /*text-align: center;*/\n    line-height: 1.3em;\n    color: #333;\n    background: #fff;\n    padding: 20px 20px 0 20px;\n}\n.literal-block { background: #fff0f0; border: solid 1px #ccc;\npadding:2px 2px 2px 10px; margin: 5px 5px 5px 5px; line-height:1.2em; }  /* Block */\n.note { background: #f0ff00; border: solid 1px #ccc;\npadding:2px 2px 2px 10px; margin: 5px 5px 5px 5px; line-height:1.2em; }  /* Notes */\n.highlight  { background: #f0f0f0; border: solid 1px #ccc;\npadding:2px 2px 2px 10px; margin: 5px 5px 5px 5px; line-height:1.2em; }\n.highlight .c { color: #60a0b0; font-style: italic } /* Comment */\n.highlight .err { border: 1px solid #FF0000 } /* Error */\n.highlight .k { color: #007020; font-weight: bold } /* Keyword */\n.highlight .o { color: #666666 } /* Operator */\n.highlight .cm { color: #60a0b0; font-style: italic } /* Comment.Multiline */\n.highlight .cp { color: #007020 } /* Comment.Preproc */\n.highlight .c1 { color: #60a0b0; font-style: italic } /* Comment.Single */\n.highlight .cs { color: #60a0b0; background-color: #fff0f0 } /* Comment.Special */\n.highlight .gd { color: #A00000 } /* Generic.Deleted */\n.highlight .ge { font-style: italic } /* Generic.Emph */\n.highlight .gr { color: #FF0000 } /* Generic.Error */\n.highlight .gh { color: #000080; font-weight: bold } /* Generic.Heading */\n.highlight .gi { color: #00A000 } /* Generic.Inserted */\n.highlight .go { color: #808080 } /* Generic.Output */\n.highlight .gp { color: #c65d09; font-weight: bold } /* Generic.Prompt */\n.highlight .gs { font-weight: bold } /* Generic.Strong */\n.highlight .gu { color: #800080; font-weight: bold } /* Generic.Subheading */\n.highlight .gt { color: #0040D0 } /* Generic.Traceback */\n.highlight .kc { color: #007020; font-weight: bold } /* Keyword.Constant */\n.highlight .kd { color: #007020; font-weight: bold } /* Keyword.Declaration */\n.highlight .kp { color: #007020 } /* Keyword.Pseudo */\n.highlight .kr { color: #007020; font-weight: bold } /* Keyword.Reserved */\n.highlight .kt { color: #007020; font-weight: bold } /* Keyword.Type */\n.highlight .m { color: #40a070 } /* Literal.Number */\n.highlight .s { color: #4070a0 } /* Literal.String */\n.highlight .na { color: #4070a0 } /* Name.Attribute */\n.highlight .nb { color: #007020 } /* Name.Builtin */\n.highlight .nc { color: #0e84b5; font-weight: bold } /* Name.Class */\n.highlight .no { color: #60add5 } /* Name.Constant */\n.highlight .nd { color: #555555; font-weight: bold } /* Name.Decorator */\n.highlight .ni { color: #d55537; font-weight: bold } /* Name.Entity */\n.highlight .ne { color: #007020 } /* Name.Exception */\n.highlight .nf { color: #06287e } /* Name.Function */\n.highlight .nl { color: #002070; font-weight: bold } /* Name.Label */\n.highlight .nn { color: #0e84b5; font-weight: bold } /* Name.Namespace */\n.highlight .nt { color: #062873; font-weight: bold } /* Name.Tag */\n.highlight .nv { color: #bb60d5 } /* Name.Variable */\n.highlight .ow { color: #007020; font-weight: bold } /* Operator.Word */\n.highlight .mf { color: #40a070 } /* Literal.Number.Float */\n.highlight .mh { color: #40a070 } /* Literal.Number.Hex */\n.highlight .mi { color: #40a070 } /* Literal.Number.Integer */\n.highlight .mo { color: #40a070 } /* Literal.Number.Oct */\n.highlight .sb { color: #4070a0 } /* Literal.String.Backtick */\n.highlight .sc { color: #4070a0 } /* Literal.String.Char */\n.highlight .sd { color: #4070a0; font-style: italic } /* Literal.String.Doc */\n.highlight .s2 { color: #4070a0 } /* Literal.String.Double */\n.highlight .se { color: #4070a0; font-weight: bold } /* Literal.String.Escape */\n.highlight .sh { color: #4070a0 } /* Literal.String.Heredoc */\n.highlight .si { color: #70a0d0; font-style: italic } /* Literal.String.Interpol */\n.highlight .sx { color: #c65d09 } /* Literal.String.Other */\n.highlight .sr { color: #235388 } /* Literal.String.Regex */\n.highlight .s1 { color: #4070a0 } /* Literal.String.Single */\n.highlight .ss { color: #517918 } /* Literal.String.Symbol */\n.highlight .bp { color: #007020 } /* Name.Builtin.Pseudo */\n.highlight .vc { color: #bb60d5 } /* Name.Variable.Class */\n.highlight .vg { color: #bb60d5 } /* Name.Variable.Global */\n.highlight .vi { color: #bb60d5 } /* Name.Variable.Instance */\n.highlight .il { color: #40a070 } /* Literal.Number.Integer.Long */\n'

def css_writer(output, style, filename='style.css'):
    """write css
    
    output:
        output path
    style:
        custom style string
    filename:
        output filename
    """
    outpath = os.path.join(output, filename)
    if not os.path.exists(outpath):
        print 'saved to %s' % outpath
        fd = file(outpath, 'w')
        fd.write(style)
        fd.close()


def saver(path, content, output, style='', nostyle=False, ext='.html'):
    """save content to file
    
    output: dir

    saver is the processor which is used to store contents to actual files;
    
    nostyle:
        not generate the css style
    ext: 
        the file extension. default value is '.html'.
    """
    filename = os.path.splitext(os.path.split(path)[1])[0] + ext
    if not output:
        output = os.path.split(path)[0]
    if not os.path.exists(output):
        os.mkdir(output)
    sav = os.path.join(output, filename)
    print 'saved to %s' % sav
    fd = file(sav, 'w')
    fd.write(content)
    fd.close()
    if os.path.exists(os.path.join(path, style)) or os.path.exists(style):
        fd = file(style, 'r')
        style = fd.read()
        fd.close()
    if not nostyle:
        css_writer(output, style)


default_template = '\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n                      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml"\n      xmlns:py="http://genshi.edgewall.org/"\n      xmlns:xi="http://www.w3.org/2001/XInclude">\n<head>\n    <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>\n    <title>Doc generated by mopowg</title>\n    <link rel="stylesheet" type="text/css" media="screen" href="style.css" />\n</head>\n<body>\n<div id="content" py:content="Markup(content)">\nhello world\n</div>\n</body>\n</html>\n'

def templater(input, content, template):
    """
    generate with genshi template
    """
    from genshi.template import MarkupTemplate
    if os.path.exists(os.path.join(input, template)) or os.path.exists(template):
        fd = file(style, 'r')
        template = fd.read()
        fd.close()
    tmpl = MarkupTemplate(template)
    stream = tmpl.generate(content=content)
    data = stream.render('html')
    return data


def processor(input, content, output, template, style, preview=False):
    """process the content
    """
    content = templater(input, content, template)
    if not preview:
        saver(input, content, output, style)
    else:
        return content


from docutils import nodes
from docutils.parsers.rst import directives
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def pygments_directive(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine):
    """register the docutils highlight function"""
    try:
        lexer = get_lexer_by_name(arguments[0])
    except ValueError:
        lexer = get_lexer_by_name('text')

    formater = HtmlFormatter()
    parsed = highlight(('\n').join(content), lexer, formater)
    return [nodes.raw('', parsed, format='html')]


pygments_directive.arguments = (1, 0, 1)
pygments_directive.content = 1
directives.register_directive('code', pygments_directive)
import re
wikiwords = re.compile('\\b([A-Z]\\w+[A-Z]+\\w+)')

def convertor(path, *arg, **kw):
    """
    Convert file to target format, include syntax highlight function

    input: path
    output: content
    
    support features:
    rich(rich content), wikiword, wikipattern
    """
    try:
        from docutils.core import publish_parts
        import pygments
    except ImportError, e:
        print e

    fd = file(path, 'r')
    data = fd.read()
    fd.close()
    if kw.get('rich', False):
        content = publish_parts(data, writer_name='html')['html_body']
        if kw.get('wikiword', False):
            pattern = kw.get('wikipattern', '<a href="\\1.html">\\1</a>')
            content = wikiwords.sub(pattern, content)
    else:
        content = data
    return content


def generator(input, filter=[
 '.rst', '.txt'], output=None, rich=True, wikiword=True, template=default_template, style=default_style, preview=False):
    """generate docs
    
    generator is used to generate docs;
    """
    for i in input:
        if os.path.isfile(i) and os.path.splitext(i)[(-1)] in filter:
            content = convertor(path=i, rich=rich, wikiword=wikiword)
            processor(i, content, output, template, style, preview)


def cmdtool():
    from optparse import OptionParser
    print 'Please use --help to get more information'
    parser = OptionParser(usage='mopowg [input] [output]')
    parser.add_option('-i', '--input', help='speficy the input folder', dest='input')
    parser.add_option('-o', '--output', help='speficy the output folder', dest='output')
    parser.add_option('-r', '--rich', help='use rich content', action='store_true', dest='rich', default=True)
    parser.add_option('-w', '--wikiword', help='Convert WikiWord to Urls', action='store_true', dest='wikiword', default=True)
    parser.add_option('-t', '--template', help='speficy a custom template', dest='template', default=default_template)
    parser.add_option('-s', '--style', help='speficy a custom css style', dest='style', default=default_style)
    parser.add_option('-p', '--preview', help='preview the content', action='store_true', dest='preview', default=False)
    (options, args) = parser.parse_args()
    ld = scanner(path=options.input)
    generator(input=ld, output=options.output, rich=options.rich, wikiword=options.wikiword, template=options.template, style=options.style, preview=options.preview)


__all__ = [
 'scanner', 'processor', 'default_style', 'default_template',
 'generator', 'convertor', 'css_writer']
if __name__ == '__main__':
    cmdtool()