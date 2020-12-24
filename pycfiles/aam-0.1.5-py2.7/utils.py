# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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