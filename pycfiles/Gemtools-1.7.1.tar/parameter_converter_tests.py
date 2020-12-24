# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/devel/thasso/git/github/gemtools/python/test/parameter_converter_tests.py
# Compiled at: 2013-04-17 04:25:02
import os
from nose.tools import raises
__author__ = 'Thasso Griebel <thasso.griebel@gmail.com>'
import gem
from testfiles import testfiles

def test_splice_consensus_conversion():
    assert gem._prepare_splice_consensus_parameter(None) == 'GT+AG'
    assert gem._prepare_splice_consensus_parameter([('AA', 'BB'), ('CC', 'DD')]) == 'AA+BB,CC+DD'
    return


def test_quality_parameter():
    assert gem._prepare_quality_parameter(None) == 'ignore'
    assert gem._prepare_quality_parameter(33) == 'offset-33'
    assert gem._prepare_quality_parameter(64) == 'offset-64'
    return


def test_index_parameter():
    idx = testfiles['genome.gem']
    dir = os.path.dirname(idx)

    def c(suf):
        return '%s/genome%s' % (dir, suf)

    assert gem._prepare_index_parameter(c('.gem')) == c('.gem')
    assert gem._prepare_index_parameter(c('')) == c('.gem')
    assert gem._prepare_index_parameter(c(''), False) == c('')
    assert gem._prepare_index_parameter(c('.gem'), False) == c('')


@raises(IOError)
def test_index_parameter_checks_file():
    gem._prepare_index_parameter('unknown_index', False)