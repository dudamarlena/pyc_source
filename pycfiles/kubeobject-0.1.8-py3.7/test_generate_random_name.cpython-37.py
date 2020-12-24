# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_generate_random_name.py
# Compiled at: 2019-10-01 18:18:07
# Size of source mod 2**32: 1836 bytes
from kubeobject import generate_random_name

def test_prefix():
    r0 = generate_random_name(prefix='prefix--')
    assert r0.startswith('prefix--')
    assert len(r0) > len('prefix--')


def test_suffix():
    r0 = generate_random_name(suffix='--suffix')
    assert r0.endswith('--suffix')
    assert len(r0) > len('--suffix')


def test_size():
    r0 = generate_random_name(size=0)
    assert len(r0) == 0
    r0 = generate_random_name(size=1)
    assert len(r0) == 1
    r0 = generate_random_name(size=100)
    assert len(r0) == 63
    r0 = generate_random_name(size=20)
    assert len(r0) == 20


def test_prefix_size():
    r0 = generate_random_name(prefix='prefix--', size=0)
    assert len(r0) == len('prefix--')
    assert r0.startswith('prefix--')
    r0 = generate_random_name(prefix='prefix--', size=100)
    assert len(r0) == 63
    assert r0.startswith('prefix--')
    r0 = generate_random_name(prefix='prefix--', size=20)
    assert len(r0) == 20
    assert r0.startswith('prefix--')


def test_suffix_size():
    r0 = generate_random_name(suffix='--suffix', size=0)
    assert len(r0) == len('--suffix')
    assert r0.startswith('--suffix')
    r0 = generate_random_name(suffix='--suffix', size=100)
    assert len(r0) == 63
    assert r0.endswith('--suffix')
    r0 = generate_random_name(suffix='--suffix', size=20)
    assert len(r0) == 20
    assert r0.endswith('--suffix')


def test_prefix_suffix():
    r0 = generate_random_name(prefix='prefix--', suffix='--suffix')
    assert len(r0) == 63
    r0 = generate_random_name(prefix='prefix--', suffix='--suffix', size=0)
    assert len(r0) == len('prefix--') + len('--suffix')
    r0 = generate_random_name(prefix='prefix--', suffix='--suffix', size=20)
    assert len(r0) == 20
    assert r0.startswith('prefix--')
    assert r0.endswith('--suffix')