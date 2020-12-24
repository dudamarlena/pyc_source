# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devel/thasso/git/github/gemtools/python/test/hash_and_junctions_tests.py
# Compiled at: 2013-10-01 07:20:46
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
def test_junction_filter():
    result = results_dir + '/test_xs.gem'
    index = gem.index(testfiles['test_xs.fa'], result)
    jf = gem.splits.append_xs_filter(index)
    of = open(testfiles['test_xs.sam'])

    def get_xs(l):
        for f in l.split('\t'):
            if f.startswith('XS'):
                return f[(-1)]

        return

    for line in of:
        if line[0] == '@':
            continue
        source_xs = get_xs(line)
        filter_xs = get_xs(jf.filter(line))
        assert source_xs == filter_xs