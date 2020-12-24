# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yate/json_theme_parser.py
# Compiled at: 2012-01-19 20:54:27
import os, json
from style import Style
default = {}
styles = {}

def loadTheme(filename):
    global default
    global styles
    theme = json.load(open(os.path.join(os.path.dirname(__file__), filename)))
    default = theme['defaults']
    for name in theme['styles']:
        style = theme['styles'][name]
        fore = None
        back = None
        fontStyle = None
        if 'foreground' in style:
            fore = style['foreground']
        if 'background' in style:
            back = style['background']
        if 'fontStyle' in style:
            fontStyle = style['fontStyle']
        styles[name] = Style(name, fore, back, fontStyle)

    return