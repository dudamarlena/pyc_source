# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/catchbot/message/content/dynamic.py
# Compiled at: 2018-06-23 13:58:03
# Size of source mod 2**32: 578 bytes
import logging

def _get_logger():
    return logging.getLogger(__name__)


def get_dynamic_msg_content(mapping, static_content, loaders):
    result = {}
    for key, value in mapping.items():
        if not isinstance(value, str):
            result[key] = get_dynamic_msg_content(value, static_content, loaders)
        else:
            loader = loaders[value]
            try:
                x = loader(static_content)
            except KeyError as e:
                x = '!' + loader.__name__
                _get_logger().warning(str(e))

            result[key] = x

    return result