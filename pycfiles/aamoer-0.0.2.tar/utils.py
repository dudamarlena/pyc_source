# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/aam/utils.py
# Compiled at: 2014-06-05 07:01:35
import os, mistune
from reader.markdown import MyRenderer

def to_unicode(value):
    if isinstance(value, unicode):
        return value
    if isinstance(value, basestring):
        return value.decode('utf-8')
    if isinstance(value, int):
        return str(value)
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return value


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def md_to_html(text):
    text = to_unicode(text)
    renderer = MyRenderer()
    md = mistune.Markdown(renderer=renderer)
    return md.render(text)