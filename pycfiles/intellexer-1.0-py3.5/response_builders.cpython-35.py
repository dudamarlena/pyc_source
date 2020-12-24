# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/intellexer/core/response_builders.py
# Compiled at: 2019-04-15 15:11:33
# Size of source mod 2**32: 331 bytes
import json

def response_builder_json(builder):

    def target(raw):
        json_data = json.loads(raw)
        return builder(json_data)

    return target


def response_builder_void(builder):

    def target(raw):
        return builder(raw)

    return target


builders = (
 response_builder_void,
 response_builder_json)