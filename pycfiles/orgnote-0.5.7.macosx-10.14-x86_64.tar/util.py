# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/LeslieZhu/.pyenv/versions/2.7.15/Python.framework/Versions/2.7/lib/python2.7/site-packages/orgnote/util.py
# Compiled at: 2019-11-27 20:06:24
"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""
from __future__ import absolute_import
from bs4 import BeautifulSoup

def gen_title(link=''):
    """ Filter Title from HTML metadata """
    import re
    html_data = BeautifulSoup(open(link, 'r').read(), 'html.parser')
    title = html_data.find('h1', {'class': 'title'}).text
    return title


def to_page_mk2(notename=''):
    import codecs, os
    from orgnote.markdown import Markdown
    css = '\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n<style type="text/css">\n</style>\n'
    print 'to_page_mk2(%s)' % notename
    input_file = codecs.open(notename, mode='r', encoding='utf-8')
    text = input_file.read()
    mk = Markdown()
    html = mk.mk2html(text)
    output_file = codecs.open(notename.replace('.md', '.html'), 'w', encoding='utf-8', errors='xmlcharrefreplace')
    output_file.write(css + html)


def to_page_mk(notename=''):
    """
    convert markdown to html
    """
    import os, markdown, codecs
    css = '\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n<style type="text/css">\n</style>\n'
    input_file = codecs.open(notename, mode='r', encoding='utf-8')
    text = input_file.read()
    if notename.endswith('.md'):
        print notename
        print text
    html = markdown.markdown(text)
    output_file = codecs.open(notename.replace('.md', '.html'), 'w', encoding='utf-8', errors='xmlcharrefreplace')
    output_file.write(css + html)


def to_page(notename=''):
    import os, os.path
    try:
        emacs_version = [ int(i) for i in get_emacs_version() ]
        if emacs_version[0] >= 24:
            cmd = 'emacs -l scripts/ox-html.el --batch %s --funcall org-html-export-to-html 2>/dev/null' % notename
        else:
            cmd = 'emacs -l scripts/init-orgnote.el --batch %s --funcall org-export-as-html 2>/dev/null' % notename
        os.system(cmd)
    except Exception as ex:
        pass

    html_file = notename.replace('.org', '.html')
    if not os.path.exists(html_file):
        print '\x1b[31m[ERROR]\x1b[0m: %s generate FAILED' % html_file


def add_note(notename='', srcdir='notes/'):
    try:
        import os
        if not notename.endswith('.org'):
            notename += '.org'
        if not notename.startswith(srcdir):
            notename = srcdir + '/' + notename
        if not os.path.exists(notename):
            import orgnote.init
            note_name = orgnote.init.create_default_note(notename)
            note_name = note_name.replace('././', './').replace('//', '/')
            if note_name != None:
                print '%s init done' % note_name
        else:
            print '%s exists, please use other name or delete it' % notename
    except Exception as ex:
        pass

    return


def publish_note(notename='', srcdir='./notes/'):
    try:
        import glob, os.path
        if notename.startswith(srcdir):
            glob_re = notename
        else:
            glob_re = srcdir + '/????/??/??/%s' % os.path.basename(notename)
        for _file in reversed(sorted(glob.glob(glob_re))):
            if _file.endswith('.org'):
                _html = _file.replace('.org', '.html')
                if not os.path.exists(_html):
                    to_page(_file)
            else:
                _html = _file.replace('.md', '.html')
                if not os.path.exists(_html):
                    to_page_mk2(_file)
            _title = gen_title(_html)
            return _file

        return
    except Exception as ex:
        pass

    return


def get_emacs_version():
    import os
    return os.popen('emacs --version').readline().strip().split()[(-1)].split('.')