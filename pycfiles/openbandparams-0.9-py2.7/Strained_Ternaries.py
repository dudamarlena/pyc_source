# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/examples/Strained_Ternaries.py
# Compiled at: 2015-04-09 02:47:55
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from openbandparams import *
unstrained = GaInAs(In=0.3)
print 'unstrained Eg', unstrained.Eg()
strained = unstrained.strained_001(GaAs)
print '  strained Eg', strained.Eg()
print
rows = []
num_cols = 3
rows.append(['Parameter', 'Unstrained', 'Strained'])
rows.append(['latex', unstrained.latex(), strained.latex()])
for parameter in ['strain_out_of_plane', 'strain_in_plane',
 'CBO_strain_shift',
 'VBO_hh_strain_shift', 'VBO_lh_strain_shift']:
    s = getattr(strained, parameter)()
    rows.append([parameter, '', ('{:g}').format(s)])

for parameter in ['CBO', 'VBO', 'Eg']:
    u = getattr(unstrained, parameter)()
    s = getattr(strained, parameter)()
    rows.append([parameter, ('{:g}').format(u), ('{:g}').format(s)])

col_widths = [ max([ len(row[col]) for row in rows ]) for col in xrange(num_cols) ]
import string
print (' | ').join([ string.ljust(rows[0][col], col_widths[col]) for col in xrange(num_cols) ])
print '-' * (sum(col_widths) + len(' | ') * (num_cols - 1))
for row in rows[1:]:
    print (' | ').join([ string.ljust(row[col], col_widths[col]) for col in xrange(num_cols) ])