# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/module.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 692 bytes


class Module:
    web3 = None

    def __init__(self, web3):
        self.web3 = web3

    @classmethod
    def attach(cls, target, module_name=None):
        if not module_name:
            module_name = cls.__name__.lower()
        else:
            if hasattr(target, module_name):
                raise AttributeError("Cannot set {0} module named '{1}'.  The web3 object already has an attribute with that name".format(target, module_name))
            if isinstance(target, Module):
                web3 = target.web3
            else:
                web3 = target
        setattr(target, module_name, cls(web3))