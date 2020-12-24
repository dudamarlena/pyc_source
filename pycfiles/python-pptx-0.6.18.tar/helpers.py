# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/scanny/Dropbox/src/python-pptx/features/steps/helpers.py
# Compiled at: 2019-05-01 23:03:34
"""
Helper methods and variables for acceptance tests.
"""
import os

def absjoin(*paths):
    return os.path.abspath(os.path.join(*paths))


thisdir = os.path.split(__file__)[0]
scratch_dir = absjoin(thisdir, '../_scratch')
test_pptx_dir = absjoin(thisdir, 'test_files')
no_core_props_pptx_path = absjoin(thisdir, '../../tests/test_files', 'no-core-props.pptx')
saved_pptx_path = absjoin(scratch_dir, 'test_out.pptx')
test_text = 'python-pptx was here!'

def cls_qname(obj):
    module_name = obj.__module__
    cls_name = obj.__class__.__name__
    qname = '%s.%s' % (module_name, cls_name)
    return qname


def count(start=0, step=1):
    """
    Local implementation of `itertools.count()` to allow v2.6 compatibility.
    """
    n = start
    while True:
        yield n
        n += step


def test_file(filename):
    """
    Return the absolute path to the file having *filename* in acceptance
    test_files directory.
    """
    return absjoin(thisdir, 'test_files', filename)


def test_image(filename):
    """
    Return the absolute path to image file having *filename* in test_files
    directory.
    """
    return absjoin(thisdir, 'test_files', filename)


def test_pptx(name):
    """
    Return the absolute path to test .pptx file with root name *name*.
    """
    return absjoin(thisdir, 'test_files', '%s.pptx' % name)