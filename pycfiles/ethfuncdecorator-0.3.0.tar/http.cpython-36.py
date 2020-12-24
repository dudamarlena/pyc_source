# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/utils/http.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 235 bytes


def construct_user_agent(class_name):
    from web3 import __version__ as web3_version
    user_agent = 'Web3.py/{version}/{class_name}'.format(version=web3_version,
      class_name=class_name)
    return user_agent