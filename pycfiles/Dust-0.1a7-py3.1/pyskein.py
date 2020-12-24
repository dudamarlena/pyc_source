# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/crypto/pyskein.py
# Compiled at: 2010-06-01 15:20:32
try:
    from skein import skein512 as cskein512

    def skein512(msg=b'', mac=b'', pers=b'', nonce=b'', tree=None, digest_bits=512):
        return cskein512(msg, mac=mac, pers=pers, nonce=nonce, tree=tree, digest_bits=digest_bits).digest()


except:
    print('Using pure python skein')
    from dust.crypto.skein512_512 import skein512_512
    from dust.crypto.skein512_256 import skein512_256

    def skein512(msg=b'', mac=b'', pers=b'', nonce=b'', tree=None, digest_bits=512):
        if digest_bits == 512:
            return skein512_512(msg, mac, pers, nonce, tree)
        else:
            if digest_bits == 256:
                return skein512_256(msg, mac, pers, nonce, tree)
            else:
                print('Digest_bits must be 512 or 256')
                return
            return