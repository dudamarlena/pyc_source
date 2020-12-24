# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/test/test_colorizer.py
# Compiled at: 2006-03-14 17:35:23
__doc__ = 'colorizer tests'
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