# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rejester/tests/test_task_master.py
# Compiled at: 2015-07-08 07:32:10
"""Unit tests for the rejester task master.

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2015 Diffeo, Inc.
"""
from __future__ import absolute_import, division
import logging, uuid, pytest
from rejester._task_master import WORK_UNITS_, _FINISHED, WORK_UNIT_STATUS_BY_NAME
from rejester.exceptions import LostLease, NoSuchWorkUnitError
logger = logging.getLogger(__name__)
pytest_plugins = 'rejester.tests.fixtures'
work_spec = {'name': 'tbundle', 
   'desc': 'a test work bundle', 
   'min_gb': 8, 
   'config': {'many': '', 'params': ''}, 'module': 'tests.rejester.test_workers', 
   'run_function': 'work_program', 
   'terminate_function': 'work_program'}

def test_task_master_basic_interface(task_master):
    work_units = dict(foo={}, bar={})
    task_master.update_bundle(work_spec, work_units)
    assert task_master.registry.pull(WORK_UNITS_ + work_spec['name'])
    assert task_master.get_work('fake_worker_id', available_gb=3) is None
    work_unit = task_master.get_work('fake_worker_id', available_gb=13)
    assert work_unit.key in work_units
    work_unit.data['status'] = 10
    work_unit.update()
    assert task_master.registry.pull(WORK_UNITS_ + work_spec['name'])[work_unit.key]['status'] == 10
    work_unit.finish()
    work_unit.finish()
    assert task_master.registry.pull(WORK_UNITS_ + work_spec['name'] + _FINISHED)[work_unit.key]['status'] == 10
    assert 'status' in task_master.inspect_work_unit(work_spec['name'], work_unit.key)
    return


def test_list_work_specs(task_master):
    assert task_master.list_work_specs() == ([], None)
    work_units = dict(foo={'length': 3}, foobar={'length': 6})
    task_master.update_bundle(work_spec, work_units)
    specs, next = task_master.list_work_specs()
    specs = dict(specs)
    assert len(specs) == 1
    assert work_spec['name'] in specs
    assert specs[work_spec['name']]['desc'] == work_spec['desc']
    return


def test_clear(task_master):
    assert task_master.list_work_specs() == ([], None)
    work_units = dict(foo={'length': 3}, foobar={'length': 6})
    task_master.update_bundle(work_spec, work_units)
    specs, next = task_master.list_work_specs()
    specs = dict(specs)
    assert len(specs) == 1
    assert work_spec['name'] in specs
    assert specs[work_spec['name']]['desc'] == work_spec['desc']
    task_master.clear()
    assert task_master.list_work_specs() == ([], None)
    return


def test_list_work_units(task_master):
    work_units = dict(foo={'length': 3}, foobar={'length': 6})
    task_master.update_bundle(work_spec, work_units)
    u = task_master.list_work_units(work_spec['name'])
    for k, v in u.iteritems():
        assert k in work_units
        assert 'length' in v
        assert len(k) == v['length']

    assert sorted(work_units.keys()) == sorted(u.keys())
    work_unit = task_master.get_work('fake_worker_id', available_gb=13)
    assert work_unit.key in work_units
    u = task_master.list_work_units(work_spec['name'])
    assert work_unit.key in u
    assert sorted(u.keys()) == sorted(work_units.keys())
    work_unit.finish()
    u = task_master.list_work_units(work_spec['name'])
    assert work_unit.key not in u
    assert all(k in work_units for k in u.iterkeys())
    assert all(k == work_unit.key or k in u for k in work_units.iterkeys())


def test_list_work_units_start_limit(task_master):
    work_units = dict(foo={'length': 3}, bar={'length': 6})
    task_master.update_bundle(work_spec, work_units)
    u = task_master.list_work_units(work_spec['name'], start=0, limit=1)
    assert u == {'bar': {'length': 6}}
    u = task_master.list_work_units(work_spec['name'], start=1, limit=1)
    assert u == {'foo': {'length': 3}}
    u = task_master.list_work_units(work_spec['name'], start=2, limit=1)
    assert u == {}


def test_del_work_units_simple(task_master):
    work_units = dict(foo={'length': 3}, bar={'length': 6})
    task_master.update_bundle(work_spec, work_units)
    rc = task_master.del_work_units(work_spec['name'], work_unit_keys=[
     'foo'])
    assert rc == 1
    assert task_master.get_work_units(work_spec['name']) == [
     (
      'bar', {'length': 6})]


STATES = [
 'AVAILABLE', 'PENDING', 'FINISHED', 'FAILED']

def prepare_one_of_each(task_master):
    task_master.update_bundle(work_spec, {'FA': {'x': 1}})
    wu = task_master.get_work('worker', available_gb=16)
    assert wu.key == 'FA'
    wu.fail()
    task_master.update_bundle(work_spec, {'FI': {'x': 1}})
    wu = task_master.get_work('worker', available_gb=16)
    assert wu.key == 'FI'
    wu.finish()
    task_master.update_bundle(work_spec, {'PE': {'x': 1}})
    wu = task_master.get_work('worker', available_gb=16)
    assert wu.key == 'PE'
    task_master.update_bundle(work_spec, {'AV': {'x': 1}})


@pytest.mark.parametrize('state', STATES)
def test_del_work_units_by_name(task_master, state):
    prepare_one_of_each(task_master)
    rc = task_master.del_work_units(work_spec['name'], work_unit_keys=[
     state[:2]])
    assert rc == 1
    expected = set(STATES)
    expected.remove(state)
    work_units = task_master.get_work_units(work_spec['name'])
    work_unit_keys = set(p[0] for p in work_units)
    assert work_unit_keys == set(st[0:2] for st in expected)


@pytest.mark.parametrize('state', STATES)
def test_del_work_units_by_state(task_master, state):
    prepare_one_of_each(task_master)
    rc = task_master.del_work_units(work_spec['name'], state=WORK_UNIT_STATUS_BY_NAME[state])
    assert rc == 1
    expected = set(STATES)
    expected.remove(state)
    work_units = task_master.get_work_units(work_spec['name'])
    work_unit_keys = set(p[0] for p in work_units)
    assert work_unit_keys == set(st[0:2] for st in expected)


@pytest.mark.parametrize('state', STATES)
def test_del_work_units_by_name_and_state(task_master, state):
    prepare_one_of_each(task_master)
    rc = task_master.del_work_units(work_spec['name'], work_unit_keys=[
     state[:2]], state=WORK_UNIT_STATUS_BY_NAME[state])
    assert rc == 1
    expected = set(STATES)
    expected.remove(state)
    work_units = task_master.get_work_units(work_spec['name'])
    work_unit_keys = set(p[0] for p in work_units)
    assert work_unit_keys == set(st[0:2] for st in expected)


def prepare_two_of_each(task_master):
    task_master.update_bundle(work_spec, {'FA': {'x': 1}, 'IL': {'x': 1}})
    wu = task_master.get_work('worker', available_gb=16)
    wu.fail()
    wu = task_master.get_work('worker', available_gb=16)
    wu.fail()
    task_master.update_bundle(work_spec, {'FI': {'x': 1}, 'NI': {'x': 1}})
    wu = task_master.get_work('worker', available_gb=16)
    wu.finish()
    wu = task_master.get_work('worker', available_gb=16)
    wu.finish()
    task_master.update_bundle(work_spec, {'PE': {'x': 1}, 'ND': {'x': 1}})
    wu = task_master.get_work('worker', available_gb=16)
    wu = task_master.get_work('worker', available_gb=16)
    task_master.update_bundle(work_spec, {'AV': {'x': 1}, 'AI': {'x': 1}})


@pytest.mark.parametrize('state', STATES)
def test_del_work_units_by_name2(task_master, state):
    prepare_two_of_each(task_master)
    rc = task_master.del_work_units(work_spec['name'], work_unit_keys=[
     state[:2]])
    assert rc == 1
    expected = set(st[0:2] for st in STATES)
    expected.update(set(st[2:4] for st in STATES))
    expected.remove(state[0:2])
    work_units = task_master.get_work_units(work_spec['name'])
    work_unit_keys = set(p[0] for p in work_units)
    assert work_unit_keys == expected


@pytest.mark.parametrize('state', STATES)
def test_del_work_units_by_state2(task_master, state):
    prepare_two_of_each(task_master)
    rc = task_master.del_work_units(work_spec['name'], state=WORK_UNIT_STATUS_BY_NAME[state])
    assert rc == 2
    expected = set(st[0:2] for st in STATES)
    expected.update(set(st[2:4] for st in STATES))
    expected.remove(state[0:2])
    expected.remove(state[2:4])
    work_units = task_master.get_work_units(work_spec['name'])
    work_unit_keys = set(p[0] for p in work_units)
    assert work_unit_keys == expected


@pytest.mark.parametrize('state', STATES)
def test_del_work_units_by_name_and_state2(task_master, state):
    prepare_two_of_each(task_master)
    rc = task_master.del_work_units(work_spec['name'], work_unit_keys=[
     state[:2]], state=WORK_UNIT_STATUS_BY_NAME[state])
    assert rc == 1
    expected = set(st[0:2] for st in STATES)
    expected.update(set(st[2:4] for st in STATES))
    expected.remove(state[0:2])
    work_units = task_master.get_work_units(work_spec['name'])
    work_unit_keys = set(p[0] for p in work_units)
    assert work_unit_keys == expected


def test_task_master_reset_all(task_master):
    work_units = dict(foo={}, bar={})
    task_master.update_bundle(work_spec, work_units)
    assert task_master.num_finished(work_spec['name']) == 0
    assert task_master.num_pending(work_spec['name']) == 0
    assert task_master.num_available(work_spec['name']) == 2
    work_unit = task_master.get_work('fake_worker_id', available_gb=13)
    work_unit.data['status'] = 10
    assert task_master.num_finished(work_spec['name']) == 0
    assert task_master.num_available(work_spec['name']) == 1
    assert task_master.num_pending(work_spec['name']) == 1
    work_unit.update()
    assert task_master.num_finished(work_spec['name']) == 0
    assert task_master.num_available(work_spec['name']) == 1
    assert task_master.num_pending(work_spec['name']) == 1
    work_unit.finish()
    assert task_master.num_finished(work_spec['name']) == 1
    assert task_master.num_available(work_spec['name']) == 1
    assert task_master.num_pending(work_spec['name']) == 0
    task_master.reset_all(work_spec['name'])
    assert task_master.num_finished(work_spec['name']) == 0
    assert task_master.num_available(work_spec['name']) == 2
    assert task_master.num_pending(work_spec['name']) == 0
    assert len(task_master.registry.pull(WORK_UNITS_ + work_spec['name'])) == 2
    with task_master.registry.lock() as (session):
        assert session.popitem(WORK_UNITS_ + work_spec['name'], priority_max=-1) is None
    return


def test_task_master_retry(task_master):
    work_units = dict(foo={}, bar={})
    task_master.update_bundle(work_spec, work_units)
    assert task_master.num_failed(work_spec['name']) == 0
    assert task_master.num_finished(work_spec['name']) == 0
    assert task_master.num_pending(work_spec['name']) == 0
    assert task_master.num_available(work_spec['name']) == 2
    work_unit = task_master.get_work('fake_worker_id', available_gb=13)
    wuname = work_unit.key
    assert task_master.num_failed(work_spec['name']) == 0
    assert task_master.num_finished(work_spec['name']) == 0
    assert task_master.num_available(work_spec['name']) == 1
    assert task_master.num_pending(work_spec['name']) == 1
    work_unit.fail(exc=Exception())
    assert task_master.num_finished(work_spec['name']) == 0
    assert task_master.num_pending(work_spec['name']) == 0
    assert task_master.num_failed(work_spec['name']) == 1
    assert task_master.num_available(work_spec['name']) == 1
    task_master.retry(work_spec['name'], wuname)
    assert task_master.num_failed(work_spec['name']) == 0
    assert task_master.num_finished(work_spec['name']) == 0
    assert task_master.num_pending(work_spec['name']) == 0
    assert task_master.num_available(work_spec['name']) == 2
    with pytest.raises(NoSuchWorkUnitError):
        task_master.retry(work_spec['name'], wuname)
    assert sorted(task_master.list_work_units(work_spec['name'])) == [
     'bar', 'foo']
    work_unit = task_master.get_work('fake_worker_id', available_gb=13)
    assert 'traceback' not in work_unit.data
    work_unit.finish()
    work_unit = task_master.get_work('fake_worker_id', available_gb=13)
    assert 'traceback' not in work_unit.data
    work_unit.finish()
    work_unit = task_master.get_work('fake_worker_id', available_gb=13)
    assert work_unit is None
    return


def test_task_master_lost_lease(task_master, monkeypatch):
    """test that waiting too long to renew a lease allows another worker
    to get the lease and leads to LostLease exception in the worker
    that waited too long.
    """
    monkeypatch.setattr('time.time', lambda : 100000000)
    work_units = dict(task_key_42=dict(data='hello'))
    task_master.update_bundle(work_spec, work_units)
    work_unit1 = task_master.get_work('fake_worker_id1', available_gb=13, lease_time=30)
    monkeypatch.setattr('time.time', lambda : 100000060)
    work_unit2 = task_master.get_work('fake_worker_id2', available_gb=13, lease_time=30)
    assert work_unit1.key == work_unit2.key
    assert work_unit1.worker_id == 'fake_worker_id1'
    assert work_unit2.worker_id == 'fake_worker_id2'
    with pytest.raises(LostLease):
        work_unit1.update()


def test_task_master_regenerate(task_master):
    """test that getting work lets us resubmit the work spec"""
    task_master.update_bundle(work_spec, {'one': {'number': 1}})
    work_unit1 = task_master.get_work('fake_worker_id1', available_gb=13)
    assert work_unit1.key == 'one'
    task_master.update_bundle(work_unit1.spec, {'two': {'number': 2}})
    work_unit1.finish()
    work_unit2 = task_master.get_work('fake_worker_id1', available_gb=13)
    assert work_unit2.key == 'two'
    work_unit2.finish()
    work_unit3 = task_master.get_work('fake_worker_id1', available_gb=13)
    assert work_unit3 is None
    return


def test_worker_child(task_master):
    """test the basic parent/child worker interface"""
    task_master.worker_register('child', mode=task_master.get_mode(), parent='parent')
    try:
        assert task_master.get_child_work_units('parent') == {'child': None}
        assert task_master.get_child_work_units('child') == {}
        task_master.update_bundle(work_spec, {'k': {'kk': 'vv'}})
        wu = task_master.get_work('child', available_gb=13)
        assert wu is not None
        assert wu.key == 'k'
        cwus = task_master.get_child_work_units('parent')
        assert cwus.keys() == ['child']
        cwu = cwus['child']
        assert cwu.worker_id == 'child'
        assert cwu.work_spec_name == work_spec['name']
        assert cwu.key == wu.key
        assert cwu.expires == wu.expires
        assert task_master.get_child_work_units('child') == {}
    finally:
        task_master.worker_unregister('child', parent='parent')

    return


def test_worker_child_expiry(task_master, monkeypatch):
    """test the parent/child interface when a job expires"""
    monkeypatch.setattr('time.time', lambda : 100000000)
    task_master.worker_register('child', mode=task_master.get_mode(), parent='parent')
    try:
        assert task_master.get_child_work_units('parent') == {'child': None}
        assert task_master.get_child_work_units('child') == {}
        task_master.update_bundle(work_spec, {'k': {'kk': 'vv'}})
        wu = task_master.get_work('child', available_gb=13, lease_time=30)
        assert wu is not None
        assert wu.key == 'k'
        monkeypatch.setattr('time.time', lambda : 100000060)
        cwus = task_master.get_child_work_units('parent')
        assert cwus.keys() == ['child']
        cwu = cwus['child']
        assert cwu.worker_id == 'child'
        assert cwu.work_spec_name == work_spec['name']
        assert cwu.key == wu.key
        assert cwu.expires == wu.expires
        assert task_master.get_child_work_units('child') == {}
    finally:
        task_master.worker_unregister('child', parent='parent')

    return


def test_worker_child_stolen(task_master, monkeypatch):
    """test the parent/child interface when a job expires"""
    monkeypatch.setattr('time.time', lambda : 100000000)
    task_master.worker_register('child', mode=task_master.get_mode(), parent='parent')
    try:
        assert task_master.get_child_work_units('parent') == {'child': None}
        assert task_master.get_child_work_units('child') == {}
        task_master.update_bundle(work_spec, {'k': {'kk': 'vv'}})
        wu = task_master.get_work('child', available_gb=13, lease_time=30)
        assert wu is not None
        assert wu.key == 'k'
        monkeypatch.setattr('time.time', lambda : 100000060)
        wu = task_master.get_work('thief', available_gb=13)
        assert wu is not None
        assert wu.key == 'k'
        cwus = task_master.get_child_work_units('parent')
        assert cwus.keys() == ['child']
        cwu = cwus['child']
        assert cwu.worker_id == 'thief'
        assert cwu.work_spec_name == work_spec['name']
        assert cwu.key == wu.key
        assert cwu.expires == wu.expires
        assert task_master.get_child_work_units('child') == {}
    finally:
        task_master.worker_unregister('child', parent='parent')

    return


def test_task_master_binary_work_unit(task_master):
    work_units = {'\x00': {'k': '\x00', 't': 'single null'}, '\x00\x01\x02\x03': {'k': '\x00\x01\x02\x03', 't': 'control chars'}, '\x00a\x00b': {'k': '\x00a\x00b', 't': 'UTF-16BE'}, 'a\x00b\x00': {'k': 'a\x00b\x00', 't': 'UTF-16LE'}, 'fü': {'k': 'fü', 't': 'UTF-8'}, b'f\xfc': {'k': b'f\xfc', 't': 'ISO-8859-1'}, b'\xf0\x0f': {'k': b'\xf0\x0f', 't': 'F00F'}, b'\xff': {'k': b'\xff', 't': 'FF'}, b'\xff\x80': {'k': b'\xff\x80', 't': 'FF80'}}
    task_master.update_bundle(work_spec, work_units)
    assert task_master.list_work_units(work_spec['name']) == work_units
    completed = []
    for _ in xrange(len(work_units)):
        wu = task_master.get_work('fake_worker_id', available_gb=13)
        assert wu.key in work_units
        assert wu.data == work_units[wu.key]
        completed.append(wu.key)
        wu.finish()

    wu = task_master.get_work('fake_worker_id', available_gb=13)
    assert wu is None
    assert sorted(completed) == sorted(work_units.keys())
    assert task_master.list_finished_work_units(work_spec['name']) == work_units
    return


def test_task_master_work_unit_value(task_master):
    work_units = {'k': {'list': [1, 2, 3], 'tuple': (4, 5, 6), 
             'mixed': [
                     1, (2, [3, 4])], 
             'uuid': uuid.UUID('01234567-89ab-cdef-0123-456789abcdef'), 
             'str': 'foo', 
             'unicode': 'foo', 
             'unicode2': 'fü'}}
    task_master.update_bundle(work_spec, work_units)
    assert task_master.list_work_units(work_spec['name']) == work_units