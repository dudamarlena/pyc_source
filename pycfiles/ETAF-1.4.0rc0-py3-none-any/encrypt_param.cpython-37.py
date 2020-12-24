# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/encrypt_param.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 2679 bytes
from arch.api.utils import log_utils
from federatedml.param.base_param import BaseParam
from federatedml.util import consts
LOGGER = log_utils.getLogger()

class EncryptParam(BaseParam):
    __doc__ = "\n    Define encryption method that used in federated ml.\n\n    Parameters\n    ----------\n    method : str, default: 'Paillier'\n        If method is 'Paillier', Paillier encryption will be used for federated ml.\n        To use non-encryption version in HomoLR, just set this parameter to be any other str.\n        For detail of Paillier encryption, please check out the paper mentioned in README file.\n\n    key_length : int, default: 1024\n        Used to specify the length of key in this encryption method. Only needed when method is 'Paillier'\n\n    "

    def __init__(self, method=consts.PAILLIER, key_length=1024):
        super(EncryptParam, self).__init__()
        self.method = method
        self.key_length = key_length

    def check(self):
        if self.method is not None and type(self.method).__name__ != 'str':
            raise ValueError("encrypt_param's method {} not supported, should be str type".format(self.method))
        else:
            if self.method is None:
                pass
            else:
                user_input = self.method.lower()
                if user_input == 'paillier':
                    self.method = consts.PAILLIER
                else:
                    if user_input == 'iterativeaffine':
                        self.method = consts.ITERATIVEAFFINE
                    else:
                        raise ValueError("encrypt_param's method {} not supported".format(user_input))
            if type(self.key_length).__name__ != 'int':
                raise ValueError("encrypt_param's key_length {} not supported, should be int type".format(self.key_length))
            else:
                if self.key_length <= 0:
                    raise ValueError("encrypt_param's key_length must be greater or equal to 1")
            LOGGER.debug('Finish encrypt parameter check!')
            return True