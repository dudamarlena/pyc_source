# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/Parameters.py
# Compiled at: 2015-04-09 03:43:25
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import *
import string
params = {}
for binary in iii_v_zinc_blende_binaries:
    for param in binary.get_unique_parameters():
        if param.name not in params:
            params[param.name] = param

names = [ n for n, p in sorted(params.items()) ]
descriptions = [ p.description for n, p in sorted(params.items()) ]
max_name_width = max([ len(name) for name in names ])
max_desc_width = max([ len(desc) for desc in descriptions ])
print '=' * max_name_width + '   ' + '=' * max_desc_width
print ('{}   {}').format(string.ljust('Parameter', max_name_width), 'Description')
print '=' * max_name_width + '   ' + '=' * max_desc_width
for name, desc in zip(names, descriptions):
    print ('{}   {}').format(string.ljust(name, max_name_width), desc)

print '=' * max_name_width + '   ' + '=' * max_desc_width