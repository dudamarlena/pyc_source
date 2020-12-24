# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/test/test_colorizer.py
# Compiled at: 2006-03-14 16:35:23
"""colorizer tests"""
from pudge.colorizer import Parser
import os.path as path, os
from setupenv import *

def get_output_file(*filenames):
    file = path.join(test_output_dir, 'colorizer', *filenames)
    if not path.exists(path.dirname(file)):
        os.makedirs(path.dirname(file))
    return file


def check_xml(file):
    from xml.dom.minidom import parse
    parse(file)


def test_colorizer():
    import os, sys, pprint
    fin = get_test_file('medium.py')
    fout = get_output_file('medium.html')
    p = Parser(fin, open(fout, 'wt'))
    p.format()
    print fout
    check_xml(fout)