# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/style.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 5758 bytes
"""
    pygments.style
    ~~~~~~~~~~~~~~

    Basic style object.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.token import Token, STANDARD_TYPES
from pygments.util import add_metaclass
_ansimap = {'ansiblack':'000000', 
 'ansired':'7f0000', 
 'ansigreen':'007f00', 
 'ansiyellow':'7f7fe0', 
 'ansiblue':'00007f', 
 'ansimagenta':'7f007f', 
 'ansicyan':'007f7f', 
 'ansigray':'e5e5e5', 
 'ansibrightblack':'555555', 
 'ansibrightred':'ff0000', 
 'ansibrightgreen':'00ff00', 
 'ansibrightyellow':'ffff00', 
 'ansibrightblue':'0000ff', 
 'ansibrightmagenta':'ff00ff', 
 'ansibrightcyan':'00ffff', 
 'ansiwhite':'ffffff'}
_deprecated_ansicolors = {'#ansiblack':'ansiblack', 
 '#ansidarkred':'ansired', 
 '#ansidarkgreen':'ansigreen', 
 '#ansibrown':'ansiyellow', 
 '#ansidarkblue':'ansiblue', 
 '#ansipurple':'ansimagenta', 
 '#ansiteal':'ansicyan', 
 '#ansilightgray':'ansigray', 
 '#ansidarkgray':'ansibrightblack', 
 '#ansired':'ansibrightred', 
 '#ansigreen':'ansibrightgreen', 
 '#ansiyellow':'ansibrightyellow', 
 '#ansiblue':'ansibrightblue', 
 '#ansifuchsia':'ansibrightmagenta', 
 '#ansiturquoise':'ansibrightcyan', 
 '#ansiwhite':'ansiwhite'}
ansicolors = set(_ansimap)

class StyleMeta(type):

    def __new__(mcs, name, bases, dct):
        obj = type.__new__(mcs, name, bases, dct)
        for token in STANDARD_TYPES:
            if token not in obj.styles:
                obj.styles[token] = ''

        def colorformat(text):
            if text in ansicolors:
                return text
            else:
                if text[0:1] == '#':
                    col = text[1:]
                    if len(col) == 6:
                        return col
                    if len(col) == 3:
                        return col[0] * 2 + col[1] * 2 + col[2] * 2
                else:
                    if text == '':
                        return ''
                if text.startswith('var') or text.startswith('calc'):
                    return text
                assert False, 'wrong color format %r' % text

        _styles = obj._styles = {}
        for ttype in obj.styles:
            for token in ttype.split():
                if token in _styles:
                    pass
                else:
                    ndef = _styles.get(token.parent, None)
                    styledefs = obj.styles.get(token, '').split()
                    if not ndef or token is None:
                        ndef = [
                         '', 0, 0, 0, '', '', 0, 0, 0]
                    elif 'noinherit' in styledefs:
                        if token is not Token:
                            ndef = _styles[Token][:]
                    else:
                        ndef = ndef[:]
                    _styles[token] = ndef
                    for styledef in obj.styles.get(token, '').split():
                        if styledef == 'noinherit':
                            continue
                        else:
                            if styledef == 'bold':
                                ndef[1] = 1
                            else:
                                if styledef == 'nobold':
                                    ndef[1] = 0
                                else:
                                    if styledef == 'italic':
                                        ndef[2] = 1
                                    else:
                                        if styledef == 'noitalic':
                                            ndef[2] = 0
                                        else:
                                            if styledef == 'underline':
                                                ndef[3] = 1
                                            else:
                                                if styledef == 'nounderline':
                                                    ndef[3] = 0
                                                else:
                                                    if styledef[:3] == 'bg:':
                                                        ndef[4] = colorformat(styledef[3:])
                                                    else:
                                                        if styledef[:7] == 'border:':
                                                            ndef[5] = colorformat(styledef[7:])
                                                        else:
                                                            if styledef == 'roman':
                                                                ndef[6] = 1
                                                            else:
                                                                if styledef == 'sans':
                                                                    ndef[7] = 1
                                                                else:
                                                                    if styledef == 'mono':
                                                                        ndef[8] = 1
                                                                    else:
                                                                        ndef[0] = colorformat(styledef)

        return obj

    def style_for_token(cls, token):
        t = cls._styles[token]
        ansicolor = bgansicolor = None
        color = t[0]
        if color in _deprecated_ansicolors:
            color = _deprecated_ansicolors[color]
        if color in ansicolors:
            ansicolor = color
            color = _ansimap[color]
        bgcolor = t[4]
        if bgcolor in _deprecated_ansicolors:
            bgcolor = _deprecated_ansicolors[color]
        if bgcolor in ansicolors:
            bgansicolor = bgcolor
            bgcolor = _ansimap[bgcolor]
        return {'color':color or None, 
         'bold':bool(t[1]), 
         'italic':bool(t[2]), 
         'underline':bool(t[3]), 
         'bgcolor':bgcolor or None, 
         'border':t[5] or None, 
         'roman':bool(t[6]) or None, 
         'sans':bool(t[7]) or None, 
         'mono':bool(t[8]) or None, 
         'ansicolor':ansicolor, 
         'bgansicolor':bgansicolor}

    def list_styles(cls):
        return list(cls)

    def styles_token(cls, ttype):
        return ttype in cls._styles

    def __iter__(cls):
        for token in cls._styles:
            yield (token, cls.style_for_token(token))

    def __len__(cls):
        return len(cls._styles)


@add_metaclass(StyleMeta)
class Style(object):
    background_color = '#ffffff'
    highlight_color = '#ffffcc'
    styles = {}