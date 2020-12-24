# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/okhin/git/orage.io/pygcrypt/env/lib/python3.6/site-packages/pygcrypt/test/test_ecurve.py
# Compiled at: 2016-12-28 04:38:18
# Size of source mod 2**32: 833 bytes
import pytest, pygcrypt.errors as errors
from pygcrypt.ecurve import ECurve
from pygcrypt.gctypes.mpi import MPIint
from pygcrypt.gctypes.sexpression import SExpression

def test_get(context):
    ec = ECurve(curve='secp192r1')
    assert isinstance(ec['a'], MPIint)


def test_set(context):
    ec = ECurve(curve='secp192r1')
    a = ec['a'] * 2
    ec['a'] = a
    assert ec['a'] == a


def test_getkey(context):
    sexp = SExpression('(public-key (ecc (curve "NIST P-256")(q #0442B927242237639A36CE9221B340DB1A9AB76DF2FE3E171277F6A4023DED146EE86525E38CCECFF3FB8D152CC6334F70D23A525175C1BCBDDE6E023B2228770E#)))')
    ec = ECurve(keyparam=sexp)
    with pytest.raises(errors.GcryptException):
        priv = ec.key(mode='SECKEY')
    pub = ec.key(mode='PUBKEY')
    assert pub.type == 'public'