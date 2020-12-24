# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/store/tests/test_store.py
# Compiled at: 2015-09-05 21:22:47
"""dossier.store.tests.test_store

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.

"""
from __future__ import absolute_import, division, print_function
import logging, pytest, kvlayer
from dossier.fc import FeatureCollection as FC
from dossier.store import Store, feature_index
from dossier.store.tests import kvl
logger = logging.getLogger(__name__)

@pytest.fixture
def fcstore(kvl):
    return Store(kvl)


def mk_fc_names(*names):
    assert len(names) > 0
    feat = FC()
    feat['canonical_name'][names[0]] = 1
    for name in names:
        feat['NAME'][name] += 1

    return feat


def test_content_id_scan(fcstore):
    fcstore.put([('aA', mk_fc_names('x'))])
    fcstore.put([('aB', mk_fc_names('y'))])
    fcstore.put([('bC', mk_fc_names('z'))])
    ids = list(fcstore.scan_prefix_ids('a'))
    assert 2 == len(ids)
    assert all(map(lambda cid: isinstance(cid, str), ids))


def test_fcs(fcstore):
    feata = mk_fc_names('foo', 'baz')
    fcstore.put([('a', feata)])
    assert fcstore.get('a') == feata


def test_fcs_index(fcstore):
    fcstore.define_index('NAME', feature_index('NAME'), lambda s: s.lower().encode('utf-8'))
    feata = mk_fc_names('foo', 'baz')
    fcstore.put([('a', feata)], indexes=True)
    assert list(fcstore.index_scan('NAME', 'FoO'))[0] == 'a'
    assert list(fcstore.index_scan('NAME', 'bAz'))[0] == 'a'
    assert list(fcstore.index_scan_prefix('NAME', 'b'))[0] == 'a'
    assert list(fcstore.index_scan_prefix_and_return_key('NAME', 'bA'))[0] == ('baz',
                                                                               'a')


def test_fcs_bad_unicode_index(fcstore):
    fcstore.define_index('NAME', feature_index('NAME'), lambda s: unicode(s.lower()))
    feata = mk_fc_names('foo', 'baz')
    with pytest.raises(kvlayer.BadKey):
        fcstore.put([('a', feata)], indexes=True)


def test_fcs_index_only_canonical(fcstore):
    fcstore.define_index('NAME', feature_index('canonical_name'), lambda s: s.lower().encode('utf-8'))
    feata = mk_fc_names('foo', 'baz')
    fcstore.put([('a', feata)], indexes=True)
    assert list(fcstore.index_scan('NAME', 'FoO'))[0] == 'a'
    assert len(list(fcstore.index_scan('NAME', 'bAz'))) == 0


def test_fcs_index_raw(fcstore):
    fcstore.define_index('NAME', feature_index('NAME'), lambda s: s.lower().encode('utf-8'))
    feata = mk_fc_names('foo', 'baz')
    fcstore.put([('a', feata)], indexes=False)
    assert len(list(fcstore.index_scan('NAME', 'FoO'))) == 0
    assert len(list(fcstore.index_scan('NAME', 'bAz'))) == 0
    fcstore._index_put_raw('NAME', 'a', 'foo')
    fcstore._index_put_raw('NAME', 'a', 'baz')
    assert list(fcstore.index_scan('NAME', 'FoO'))[0] == 'a'
    assert list(fcstore.index_scan('NAME', 'bAz'))[0] == 'a'
    assert list(fcstore.index_scan_prefix('NAME', 'b'))[0] == 'a'


def test_index_order(fcstore):
    fcstore.define_index('a', None, None)
    fcstore.define_index('z', None, None)
    fcstore.define_index('d', None, None)
    fcstore.define_index('c', None, None)
    assert fcstore.index_names() == ['a', 'z', 'd', 'c']
    return


def test_index_key_flip(fcstore):
    fca, fcb = FC(), FC()
    fca['a']['foo'] = 1
    fca['b']['foo'] = 1
    fcstore.define_index('a', feature_index('a'), lambda s: s.lower().encode('utf-8'))
    fcstore.define_index('b', feature_index('b'), lambda s: s.lower().encode('utf-8'))
    fcstore.put([('fca', fca), ('fcb', fcb)])
    assert list(fcstore.index_scan('a', 'foo')) == ['fca']


def test_one_to_many_indexing(kvl):
    index_config = [{'foo': ['bar', 'baz']}]
    store = Store(kvl, feature_indexes=index_config)
    fcx, fcy, fcz = FC(), FC(), FC()
    fcx['unrelated']['a'] = 1
    fcy['bar']['a'] = 1
    fcy['baz']['a'] = 1
    fcz['baz']['a'] = 1
    fcy['baz']['c'] = 1
    fcz['baz']['b'] = 1
    store.put([('x', fcx), ('y', fcy), ('z', fcz)])
    assert list(store.index_scan('foo', 'a')) == ['y', 'z']
    assert list(store.index_scan('foo', 'b')) == ['z']
    assert list(store.index_scan('foo', 'c')) == ['y']