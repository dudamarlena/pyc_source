# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/no_cloud/formatter.py
# Compiled at: 2017-01-06 13:00:18
import markdown

def make_html(text):
    md = markdown.Markdown(extensions=[
     'markdown.extensions.extra',
     'markdown.extensions.meta'])
    return md.convert(text)