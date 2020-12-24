# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/adminish/md.py
# Compiled at: 2009-02-25 17:54:23
from adminish import markdown, mdx_enhanced_image

def md(text):
    return markdown.markdown(text, [mdx_enhanced_image])