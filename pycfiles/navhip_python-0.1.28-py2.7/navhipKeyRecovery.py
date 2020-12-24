# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/navhip/navhipKeyRecovery.py
# Compiled at: 2020-02-12 12:19:44
import ecdsa
from ecdsa.curves import SECP256k1
from ecdsa.ellipticcurve import Point
from ecdsa.util import string_to_number, number_to_string

class MyVerifyingKey(ecdsa.VerifyingKey):

    @classmethod
    def from_signature(klass, sig, recid, h, curve):
        """ See http://www.secg.org/download/aid-780/sec1-v2.pdf, chapter 4.1.6 """
        from ecdsa import util, numbertheory
        import msqr
        curveFp = curve.curve
        G = curve.generator
        order = G.order()
        r, s = util.sigdecode_string(sig, order)
        x = r + recid / 2 * order
        alpha = (x * x * x + curveFp.a() * x + curveFp.b()) % curveFp.p()
        beta = msqr.modular_sqrt(alpha, curveFp.p())
        y = beta if (beta - recid) % 2 == 0 else curveFp.p() - beta
        R = Point(curveFp, x, y, order)
        e = string_to_number(h)
        minus_e = -e % order
        inv_r = numbertheory.inverse_mod(r, order)
        Q = inv_r * (s * R + minus_e * G)
        return klass.from_public_point(Q, curve)


def point_to_ser(P):
    return ('04' + '%064x' % P.x() + '%064x' % P.y()).decode('hex')


def recoverKey(signature, hashValue, keyX):
    rLength = signature[3]
    r = signature[4:4 + rLength]
    sLength = signature[(4 + rLength + 1)]
    s = signature[4 + rLength + 2:]
    if rLength == 33:
        r = r[1:]
    if sLength == 33:
        s = s[1:]
    r = str(r)
    s = str(s)
    for i in range(4):
        try:
            key = MyVerifyingKey.from_signature(r + s, i, hashValue, curve=SECP256k1)
            candidate = point_to_ser(key.pubkey.point)
            if candidate[1:33] == keyX:
                return candidate
        except:
            pass

    raise Exception('Key recovery failed')