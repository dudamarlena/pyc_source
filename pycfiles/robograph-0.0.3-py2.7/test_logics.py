# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/tests/test_logics.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.nodes.lib import logics

def test_not():
    expected_reqs = [
     'function', 'argument']
    instance = logics.Not()
    assert instance.requirements == expected_reqs
    instance.input(dict(argument=[True, False, False]))
    instance.set_output_label('any')
    assert instance.output() == [False, True, True]


def test_and():
    expected_reqs = [
     'function', 'argument']
    instance = logics.And()
    assert instance.requirements == expected_reqs
    instance.input(dict(argument=[True, True]))
    instance.set_output_label('any')
    assert instance.output()
    instance = logics.And()
    instance.input(dict(argument=[True, False]))
    instance.set_output_label('any')
    assert not instance.output()


def test_or():
    expected_reqs = [
     'function', 'argument']
    instance = logics.Or()
    assert instance.requirements == expected_reqs
    instance.input(dict(argument=[True, False]))
    instance.set_output_label('any')
    assert instance.output()
    instance = logics.Or()
    instance.input(dict(argument=[False, False]))
    instance.set_output_label('any')
    assert not instance.output()


def test_all():
    expected_reqs = [
     'function', 'argument']
    instance = logics.All()
    assert instance.requirements == expected_reqs
    instance.input(dict(argument=[True, True, False]))
    instance.set_output_label('any')
    assert not instance.output()
    instance = logics.All()
    instance.input(dict(argument=[True, True, True]))
    instance.set_output_label('any')
    assert instance.output()


def test_any():
    expected_reqs = [
     'function', 'argument']
    instance = logics.Any()
    assert instance.requirements == expected_reqs
    instance.input(dict(argument=[True, False, False]))
    instance.set_output_label('any')
    assert instance.output()
    instance = logics.Any()
    instance.input(dict(argument=[False, False, False]))
    instance.set_output_label('any')
    assert not instance.output()


def test_nil():
    expected_reqs = [
     'function', 'argument']
    instance = logics.Nil()
    assert instance.requirements == expected_reqs
    instance.input(dict(argument=[True, False, False]))
    instance.set_output_label('any')
    assert not instance.output()
    instance = logics.Nil()
    instance.input(dict(argument=[False, False, False]))
    instance.set_output_label('any')
    assert instance.output()