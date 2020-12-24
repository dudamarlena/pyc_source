# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/adminish/md.py
# Compiled at: 2009-02-25 17:54:23
from adminish import markdown, mdx_enhanced_image

def md(text):
    return markdown.markdown(text, [mdx_enhanced_image])