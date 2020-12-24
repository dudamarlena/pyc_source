# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devel/thasso/git/github/gemtools/python/test/indexer_tests.py
# Compiled at: 2013-04-17 04:25:02
import os, shutil
from nose.tools import with_setup
import gem
from gem import files
from gem import filter
from gem import junctions
from testfiles import testfiles
__author__ = 'Thasso Griebel <thasso.griebel@gmail.com>'
index = testfiles['genome.gem']
results_dir = None

def setup_func():
    global results_dir
    results_dir = 'test_results'
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)
    results_dir = os.path.abspath(results_dir)


def cleanup():
    shutil.rmtree(results_dir, ignore_errors=True)


@with_setup(setup_func, cleanup)
def test_indexer():
    result = results_dir + '/genome_index'
    input = testfiles['genome.fa']
    index = gem.index(input, result)
    assert index == result + '.gem'
    assert os.path.exists(result + '.gem')


@with_setup(setup_func, cleanup)
def test_indexer_output_suffix():
    result = results_dir + '/genome_index.gem'
    input = testfiles['genome.fa']
    index = gem.index(input, result)
    assert index == result, 'Result should be %s.gem but is %s' % (result, index)
    assert os.path.exists(result)