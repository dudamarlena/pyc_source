# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devel/thasso/git/github/gemtools/python/test/conversion_tests.py
# Compiled at: 2013-10-16 05:11:38
import os, shutil
from nose.tools.nontrivial import with_setup
import gem, gem.gemtools as gt
from testfiles import testfiles
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
def test_gem2sam_execution():
    input = gem.files.open(testfiles['reads_1.fastq'])
    mappings = gem.mapper(input, index)
    sam = gem.gem2sam(mappings, index, compact=True)
    assert sam is not None
    assert sam.process is not None
    assert sam.filename is None
    count = 0
    for read in sam:
        count += 1

    assert count == 10000, 'Count 10000!=%d' % count
    return


@with_setup(setup_func, cleanup)
def test_gem2sam_execution_to_file():
    input = gem.files.open(testfiles['reads_1.fastq'])
    mappings = gem.mapper(input, index)
    result = results_dir + '/test_sam.sam'
    sam = gem.gem2sam(mappings, index, output=result, compact=True)
    assert sam is not None
    assert sam.process is not None
    assert sam.filename == result
    assert os.path.exists(result)
    return


@with_setup(setup_func, cleanup)
def test_gem2sam_sam2bam():
    input = gem.files.open(testfiles['reads_1.fastq'])
    mappings = gem.mapper(input, index)
    sam = gem.gem2sam(mappings, index, compact=True)
    result = results_dir + '/test_sam.bam'
    bam = gem.sam2bam(sam, output=result)
    assert os.path.exists(result)
    count = 0
    for l in gem.files.open(result):
        count += 1

    assert count == 10000, 'Count 10000!=%d' % count