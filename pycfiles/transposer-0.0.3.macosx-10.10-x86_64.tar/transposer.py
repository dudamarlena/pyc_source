# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/transposer/transposer.py
# Compiled at: 2015-01-24 01:07:12
"""
takes contents of delimited file and transposes columns and rows
outputs to txt file
"""
import argparse

def transpose(i, o=None, d=','):
    f = open(i, 'r')
    file_contents = f.readlines()
    f.close()
    out_data = map(lambda x: d.join([ y for y in x ]), zip(*[ x.strip().split(d) for x in file_contents if x ]))
    if o:
        f = open(o, 'w')
        f.write(('\n').join(out_data))
        f.close()
    return out_data