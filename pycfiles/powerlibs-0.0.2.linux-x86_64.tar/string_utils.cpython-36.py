# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cleber/.pyenv/versions/powerlibs_aws_sqs_dequeuer/lib/python3.6/site-packages/powerlibs/string_utils.py
# Compiled at: 2017-04-15 22:25:47
# Size of source mod 2**32: 254 bytes
import re

def snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', '\\1_\\2', name)
    return re.sub('([a-z0-9])([A-Z])', '\\1_\\2', s1).lower()


def camel_case(name):
    return ''.join((p.title() if i else p) for i, p in enumerate(name.split('_')))