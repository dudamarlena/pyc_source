# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\starscreamlib\common.py
# Compiled at: 2008-05-09 23:12:09
import re

def remove_timestamps(tree):
    """Remove timestamps of the form <1:30> from the section titles"""
    pattern = re.compile('\\<\\d+\\:\\d+\\>')

    def get_new_title(text):
        m = pattern.search(text)
        return text[:m.start()].strip() if m else text

    for h1 in tree.xpath('div/h1'):
        a = h1.xpath('a')
        if a:
            title = get_new_title(a[0].text)
            h1.remove(a[0])
            h1.text = title


def get_css_links(cssfiles):
    """``cssfiles`` is a list of CSS file names. Return a chunk of HTML
    markup that links to each CSS file."""
    return ('\n').join(('<link rel="stylesheet" type="text/css" href="%s" />' % f for f in cssfiles))


def get_javascript_links(jsfiles):
    """``jsfiles`` is a list of JavaScript file names. Return a chunk of HTML
    markup that links to each JavaScript file."""
    return ('\n').join(('<script type="text/javascript" src="%s"></script>' % f for f in jsfiles))