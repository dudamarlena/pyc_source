# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\starscreamlib\handout.py
# Compiled at: 2008-03-31 08:36:31
import re, string, codecs
from lxml import etree
from docutilslib import publish_parts
import common

def build_handout(filename):
    """From the reST file ``filename``, generate the following
    ``handout.html`` file"""
    parts = publish_parts(filename)
    tree = etree.fromstring('<root>%s</root>' % parts['body'])
    common.remove_timestamps(tree)
    modify_notes_nodes(tree)
    parts['body'] = etree.tostring(tree)[6:-7]
    parts['csslinks'] = common.get_css_links(parts['cssfiles'])
    codecs.open('handout.html', 'w', 'utf-8').write(template.substitute(**parts))


def modify_notes_nodes(tree):
    """Visit all non-top-level nodes, change their class attribute to 'notes'"""
    nodes = tree.xpath("div//div[@class='section']")
    for node in nodes:
        node.set('class', 'notes')
        node.remove(node[0])


template = string.Template('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n<title>${title}</title>\n<link rel="stylesheet" type="text/css" href="handout.css" />\n$csslinks\n<body>\n<div id="info">\n    <div id="title">${title}</div>\n    <div id="author">${author}</div>\n    <div id="venue">${venue}</div>\n    <div id="location">${location}</div>\n    <div id="date">${date}</div>\n</div>\n${body}\n</body>\n</html>\n')
if __name__ == '__main__':
    build_handout('slides.txt')
    print '\nDone!\n'