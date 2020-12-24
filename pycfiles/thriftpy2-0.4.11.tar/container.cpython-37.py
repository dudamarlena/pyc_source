# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/Idea/thriftpy2/tests/container.py
# Compiled at: 2019-02-28 10:40:44
# Size of source mod 2**32: 461 bytes
"""This file is a demo for what the dynamiclly generated code would be like.
"""
from thriftpy2.thrift import TPayload, TType

class MixItem(TPayload):
    thrift_spec = {1:(
      TType.LIST, 'list_map',
      (
       TType.MAP, (TType.STRING, TType.STRING))), 
     2:(
      TType.MAP, 'map_list',
      (
       TType.STRING, (TType.LIST, TType.STRING)))}
    default_spec = [
     ('list_map', None), ('map_list', None)]