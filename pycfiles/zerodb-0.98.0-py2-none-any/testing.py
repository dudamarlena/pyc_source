# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/testing.py
# Compiled at: 2016-07-10 18:12:03
"""
Pytest fixtures for zerodb tests

To activate the fixtures, add this to your conftest.py:

from zerodb.testing import *
"""
import pytest, shutil, tempfile
from time import sleep
from multiprocessing import Process
from os import path
import zerodb
from zerodb.crypto import ecc
from zerodb.permissions import elliptic
from zerodb.permissions.base import PermissionsDatabase
from zerodb.storage import ZEOServer
from zerodb.util import encode_hex
kdf = elliptic.Client.kdf
TEST_PASSPHRASE = 'v3ry 53cr3t pa$$w0rd'
TEST_PUBKEY = ecc.private(TEST_PASSPHRASE, ('root', 'ZERO'), kdf=kdf).get_pubkey()
TEST_PUBKEY_3 = ecc.private(TEST_PASSPHRASE + ' third', ('third', 'ZERO'), kdf=kdf).get_pubkey()
TEST_PERMISSIONS = 'realm ZERO\nauth_secp256k1_scrypt:root:%s\nauth_secp256k1_scrypt:third:%s' % (encode_hex(TEST_PUBKEY), encode_hex(TEST_PUBKEY_3))
ZEO_CONFIG = '<zeo>\n  address %(sock)s\n  authentication-protocol auth_secp256k1_scrypt\n  authentication-database %(pass_file)s\n  authentication-realm ZERO\n</zeo>\n\n<filestorage>\n  path %(dbfile)s\n  pack-gc false\n</filestorage>'
elliptic.register_auth()
__all__ = [
 'TEST_PASSPHRASE',
 'TEST_PUBKEY',
 'tempdir',
 'pass_file',
 'pass_db',
 'do_zeo_server',
 'zeo_server',
 'db']

@pytest.fixture(scope='module')
def tempdir(request):
    tmpdir = tempfile.mkdtemp()
    request.addfinalizer(lambda : shutil.rmtree(tmpdir))
    return tmpdir


@pytest.fixture(scope='module')
def pass_file(request, tempdir):
    filename = path.join(tempdir, 'authdb.conf')
    with open(filename, 'w') as (f):
        f.write(TEST_PERMISSIONS)
    return filename


@pytest.fixture(scope='function')
def pass_db(request, pass_file):
    pdb = PermissionsDatabase(pass_file)
    request.addfinalizer(pdb.close)
    return pdb


def do_zeo_server(request, pass_file, tempdir, name=None):
    """
    :return: Temporary UNIX socket
    :rtype: str
    """
    sock = path.join(tempdir, 'zeosocket_auth')
    zeroconf_file = path.join(tempdir, 'zeo.config')
    dbfile = path.join(tempdir, 'db2.fs')
    with open(zeroconf_file, 'w') as (f):
        f.write(ZEO_CONFIG % {'sock': sock, 
           'pass_file': pass_file, 
           'dbfile': dbfile})
    server = Process(name=name, target=ZEOServer.run, kwargs={'args': ('-C', zeroconf_file)})

    @request.addfinalizer
    def fin():
        sleep(1)
        server.terminate()
        server.join(1)

    server.daemon = True
    server.start()
    return sock


@pytest.fixture(scope='module')
def zeo_server(request, pass_file, tempdir):
    sock = do_zeo_server(request, pass_file, tempdir, name='zeo_server')
    return sock


@pytest.fixture(scope='module')
def db(request, zeo_server):
    zdb = zerodb.DB(zeo_server, username='root', password=TEST_PASSPHRASE, debug=True)

    @request.addfinalizer
    def fin():
        zdb.disconnect()

    return zdb