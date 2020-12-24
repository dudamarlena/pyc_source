# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unitindexd_test.py
# Compiled at: 2020-03-14 11:10:26
# Size of source mod 2**32: 6488 bytes
import pytest
from requests import HTTPError

def get_rec(gen3_index, guid):
    return gen3_index.get_record(guid)


def test_system(gen3_index):
    """

    Test that gen3_index is healthy

    """
    if not gen3_index.is_healthy():
        raise AssertionError
    else:
        assert gen3_index.get_version()
        assert gen3_index.get_stats()


def test_get_urls(gen3_index):
    """

    Test get_urls

    """
    rec1 = gen3_index.create_record(hashes={'md5': '374c12456782738abcfe387492837483'},
      size=0)
    rec2 = gen3_index.create_record(hashes={'md5': 'adbc12447582738abcfe387492837483'},
      size=2)
    rec3 = gen3_index.create_record(hashes={'md5': 'adbc82746782738abcfe387492837483'},
      size=1)
    if not gen3_index.get_urls(hashes='md5:374c12456782738abcfe387492837483'):
        raise AssertionError
    else:
        if not gen3_index.get_urls(size=1):
            raise AssertionError
        else:
            if not gen3_index.get_urls(size=2):
                raise AssertionError
            else:
                drec = gen3_index.delete_record(rec1['did'])
                assert drec._deleted
            drec = gen3_index.delete_record(rec2['did'])
            assert drec._deleted
        drec = gen3_index.delete_record(rec3['did'])
        assert drec._deleted


def test_bulk(gen3_index):
    """

    Test get_records

    """
    rec1 = gen3_index.create_record(hashes={'md5': '374c12456782738abcfe387492837483'},
      size=0)
    rec2 = gen3_index.create_record(hashes={'md5': 'adbc12447582738abcfe387492837483'},
      size=0)
    rec3 = gen3_index.create_record(hashes={'md5': 'adbc82746782738abcfe387492837483'},
      size=0)
    recs = gen3_index.get_records([rec1['did'], rec2['did'], rec3['did']])
    dids = [
     rec1['did']] + [rec2['did']] + [rec3['did']]
    v = True
    for rec in recs:
        if rec['did'] not in dids:
            v = False

    if not v:
        raise AssertionError
    else:
        drec = gen3_index.delete_record(rec1['did'])
        assert drec._deleted
        drec = gen3_index.delete_record(rec2['did'])
        assert drec._deleted
        drec = gen3_index.delete_record(rec3['did'])
        assert drec._deleted


def test_get_with_params(gen3_index):
    """

    test get_with_params

    """
    rec1 = gen3_index.create_record(hashes={'md5': '374c12456782738abcfe387492837483'},
      size=1615680)
    rec2 = gen3_index.create_record(hashes={'md5': 'adbc82746782738abcfe387492837483'},
      size=15945566)
    if not rec1:
        raise AssertionError
    else:
        if not rec2:
            raise AssertionError
        else:
            drec = gen3_index.delete_record(rec1['did'])
            assert drec._deleted
        drec = gen3_index.delete_record(rec2['did'])
        assert drec._deleted


def test_new_record(gen3_index):
    """

    Test the creation, update, and deletion a record

        index.py functions tested:
            create_record
            get
            get_record
            update_record
            delete_record

    """
    newrec = gen3_index.create_record(hashes={'md5': 'adbc12456782738abcfe387492837483'},
      size=0)
    checkrec = gen3_index.get(newrec['baseid'])
    if not (newrec['did'] == checkrec['did'] and newrec['baseid'] == checkrec['baseid'] and newrec['rev'] == checkrec['rev']):
        raise AssertionError
    else:
        updated = gen3_index.update_record((newrec['did']),
          acl=['prog1', 'proj1'], file_name='fakefilename')
        updatedrec = get_rec(gen3_index, updated['did'])
        assert updatedrec['acl'] == ['prog1', 'proj1']
        assert updatedrec['file_name'] == 'fakefilename'
        assert updatedrec['did'] == checkrec['did']
        assert updatedrec['rev'] != checkrec['rev']
        drec = gen3_index.delete_record(updatedrec['did'])
        assert drec._deleted


def test_versions(gen3_index):
    """

    Test creation of a record and a new version of it

    index.py functions tested:
        create_record
        create_new_version
        get_versions
        get_latest_version

    """
    newrec = gen3_index.create_record(acl=[
     'prog1', 'proj1'],
      hashes={'md5': '437283456782738abcfe387492837483'},
      size=0,
      version='1')
    newversion = gen3_index.create_new_version((newrec['did']),
      acl=[
     'prog1', 'proj1'],
      hashes={'md5': '437283456782738abcfe387492837483'},
      size=1,
      version='2')
    newrec = get_rec(gen3_index, newrec['did'])
    newversion = get_rec(gen3_index, newversion['did'])
    if not newrec['did'] != newversion['did']:
        raise AssertionError
    else:
        if not newrec['baseid'] == newversion['baseid']:
            raise AssertionError
        else:
            versions = gen3_index.get_versions(newversion['did'])
            latest_version = gen3_index.get_latest_version(newrec['did'], 'false')
            assert versions[0]['did'] == newrec['did']
            assert versions[1]['did'] == newversion['did']
            assert latest_version['did'] == newversion['did']
            assert latest_version['version'] == '2'
            drec = gen3_index.delete_record(newrec['did'])
            assert drec._deleted
        drec = gen3_index.delete_record(newversion['did'])
        assert drec._deleted