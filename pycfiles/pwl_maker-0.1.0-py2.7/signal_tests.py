# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/signal_tests.py
# Compiled at: 2014-11-01 21:29:40
from nose.tools import *
import pwl_maker
from pwl_maker.signal import Signal
import os.path
print 'test', pwl_maker

def test_assign_name():
    s = Signal('signal')
    assert_equal(s.name, 'signal')


def test_auto_name():
    signal1 = Signal()
    signal2 = Signal()
    assert_equal(signal1.name, 'signal-1')
    assert_equal(signal2.name, 'signal-2')


def test_no_initial_value():
    s = Signal()
    assert_equal(s.data, [[0, 0]])


def test_set_initial_value():
    s = Signal(initial_value=5)
    assert_equal(s.data, [[0, 5]])


def test_simple():
    s = Signal(slew=1)
    s.at(1).to(3).at(5).to(-1)
    assert_equals(s.data, [
     [
      0, 0],
     [
      1, 0],
     [
      2, 3],
     [
      5, 3],
     [
      6, -1]])


def test_extend_to():
    s = Signal(slew=1)
    s.at(1).to(3).extend_to(5)
    assert_equals(s.data, [
     [
      0, 0],
     [
      1, 0],
     [
      2, 3],
     [
      5, 3]])


def test_extend_to_before_end():
    s = Signal(slew=1)
    s.at(1).to(3).extend_to(1)
    assert_equals(s.data, [
     [
      0, 0],
     [
      1, 0],
     [
      2, 3]])


def test_save_with_default_name():
    s = Signal()
    s.extend_to(4)
    s.save()
    expected_name = s.name + '.pwl'
    assert_true(os.path.isfile(expected_name))
    with open(expected_name) as (f):
        content = f.readlines()
    assert_equal(content, ['0\t0\n', '4\t0\n'])
    os.remove(expected_name)


def test_as_lists():
    s = Signal(slew=1)
    s.at(1).to(3).extend_to(5)
    assert_equals(s.as_lists(), (
     [
      0, 1, 2, 5], [0, 0, 3, 3]))


def test_scale_time():
    s = Signal(slew=1)
    s.at(1).to(3)
    s.scale_time(0.001)
    assert_equals(s.data, [
     [
      0, 0],
     [
      0.001, 0],
     [
      0.002, 3]])


def test_scale_value():
    s = Signal(slew=1)
    s.at(1).to(3)
    s.scale_value(3)
    assert_equals(s.data, [
     [
      0, 0],
     [
      1, 0],
     [
      2, 9]])