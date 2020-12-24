# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/bokeh_templating/keyword_map.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 1031 bytes
"""
Created on Thu Jul 19 09:54:47 2018

@author: gkanarek
"""
from bokeh import layouts, models, palettes, plotting, transform
from inspect import getmembers, isclass, isfunction
from .bokeh_surface import Surface3d
bokeh_sequences = {}
bokeh_mappings = {'Surface3d': Surface3d}

def parse_module(module):
    test = lambda nm, mem: not nm.startswith('_') and module.__name__ in mem.__module__
    seqs = {nm:mem for nm, mem in getmembers(module, isfunction) if test(nm, mem)}
    maps = {nm:mem for nm, mem in getmembers(module, isclass) if test(nm, mem)}
    if 'gridplot' in seqs:
        maps['gridplot'] = seqs.pop('gridplot')
    if 'Donut' in seqs:
        maps['Donut'] = seqs.pop('Donut')
    return (
     seqs, maps)


for module in [models, plotting, layouts, palettes, transform]:
    seqs, maps = parse_module(module)
    bokeh_sequences.update(seqs)
    bokeh_mappings.update(maps)