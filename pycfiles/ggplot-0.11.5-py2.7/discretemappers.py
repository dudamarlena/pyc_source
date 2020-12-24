# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/discretemappers.py
# Compiled at: 2016-07-28 18:33:46
from __future__ import absolute_import, division, print_function, unicode_literals
from .colors import palettes
import itertools
SHAPES = [
 b'o',
 b'^',
 b'D',
 b'v',
 b's',
 b'*',
 b'p',
 b'8',
 b'_',
 b'|',
 b'_']

def shape_gen():
    while True:
        for shape in SHAPES:
            yield shape


def size_gen(uniq_values):
    n = len(uniq_values)
    low = 10
    for i in range(low, low + n * 10, 10):
        yield i


def color_gen(n_colors, colors=None):
    if colors:
        pal = colors
    else:
        pal = palettes.color_palette(name=b'husl', n_colors=n_colors)
    generator = itertools.cycle(pal)
    while True:
        yield next(generator)


def identity_gen(uniq_values):
    for value in uniq_values:
        yield value


LINETYPES = [
 b'solid',
 b'dashed',
 b'dashdot',
 b'dotted']

def linetype_gen():
    while True:
        for line in LINETYPES:
            yield line