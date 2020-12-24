# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jsonclient\mako_render_tools.py
# Compiled at: 2012-03-09 07:36:45
import re, simplejson

def mako_preprocessor(text):
    text = re.sub('<mako:', '<%', text)
    text = re.sub('</mako:', '</%', text)
    return text


def json(text):
    print type(text)
    return text