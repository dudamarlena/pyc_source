# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/test/_testRegistrar.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 375 bytes
import ioflo.base.registering as registering

def TestRegistry():
    """Module self test
    """
    x = Registrar()
    print(x.name)
    y = Registrar()
    print(y.name)
    name = 'Hello'
    if Registrar.VerifyName(name):
        z = Registrar(name=name)
    print(Registrar.Names)
    print(Registrar.VerifyName(name))


if __name__ == '__main__':
    TestRegistry()