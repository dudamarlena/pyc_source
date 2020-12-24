# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devel/thasso/git/github/gemtools/python/test/filters_tests.py
# Compiled at: 2013-10-01 07:20:46
import os, shutil
from nose.tools import with_setup
import sys, gem.gemtools as gt
from gem import files
from gem import filter
from testfiles import testfiles
__author__ = 'Thasso Griebel <thasso.griebel@gmail.com>'
results_dir = None

def setup_func():
    global results_dir
    results_dir = 'test_results'
    if not os.path.exists(results_dir):
        os.mkdir(results_dir)
    results_dir = os.path.abspath(results_dir)


def cleanup():
    shutil.rmtree(results_dir, ignore_errors=True)


def test_cat():
    reads_1 = files.open(testfiles['reads_1.fastq'])
    reads_2 = files.open(testfiles['reads_2.fastq'])
    num_reads = sum(1 for r in filter.cat([reads_1, reads_2]))
    assert num_reads == 20000


@with_setup(setup_func, cleanup)
def test_cat_to_file():
    target = results_dir + '/catted.fastq'
    reads_1 = files.open(testfiles['reads_1.fastq'])
    reads_2 = files.open(testfiles['reads_2.fastq'])
    out = gt.OutputFile(target)
    gt.cat([reads_1, reads_2]).write_stream(out)
    c = 0
    ids = []
    with open(target) as (f):
        for l in f:
            if c % 4 == 0:
                ids.append(l.strip())
            c += 1

    assert len(set(ids)) == 20000


def test_only_split_maps_filter_paired_stream():
    infile = testfiles['split_filter_test_paired.map']
    filtered = filter.only_split_maps(infile)
    assert filtered is not None
    all_maps = 0
    for template in filtered:
        all_maps += template.get_num_maps()

    assert all_maps == 1
    return


@with_setup(setup_func, cleanup)
def test_only_split_maps_filter_paired_compress_file():
    target = results_dir + '/filtered.map.gz'
    target_uncompressed = results_dir + '/filtered.map'
    infile = testfiles['split_filter_test_paired.map']
    filtered = filter.only_split_maps(infile, output=target, compress=True)
    assert filtered is not None
    all_maps = 0
    for template in filtered:
        all_maps += template.get_num_maps()

    assert os.path.exists(target)
    import subprocess
    assert subprocess.Popen(['gunzip', '-f', target]).wait() == 0
    assert os.path.exists(target_uncompressed)
    with open(target_uncompressed) as (f):
        lines = f.readlines()
        print lines
        assert len(lines) == 3
    return