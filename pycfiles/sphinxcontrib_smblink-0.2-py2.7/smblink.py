# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/sphinxcontrib/smblink.py
# Compiled at: 2013-03-30 22:40:08
"""
smblink role for Sphinx.

"""
from docutils import nodes
import re, string

def convertToWSLStyle(text):
    replaceDic = {'\\^': '%5E', 
       '\\~': '%7E', 
       '{': '%7B', 
       '}': '%7D', 
       '\\[': '%5B', 
       '\\]': '%5D', 
       ';': '%3B', 
       '@': '%40', 
       '=': '%3D', 
       '\\&': '%26', 
       '\\$': '%24', 
       '#': '%23', 
       ' ': '%20', 
       '\\\\': '/'}
    text = re.sub('%', '%25', text)
    for reg, rep in replaceDic.items():
        text = re.sub(reg, rep, text)

    return text


def smblink_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Role to create link addresses.
    """
    text = rawtext
    if '`' in text:
        text = text.split('`')[1]
    if '<' in text and '>' in text:
        name, path = text.split('<')
        path = path.split('>')[0]
        name = re.sub('[ ]+$', '', name)
    else:
        name = text
        path = name
    href = '<a href="file:' + convertToWSLStyle(path) + '">' + name + '</a>'
    node = nodes.raw('', href, format='html')
    return ([node], [])


def setup(app):
    app.add_role('smblink', smblink_role)