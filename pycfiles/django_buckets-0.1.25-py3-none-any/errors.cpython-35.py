# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-buckets/buckets/test/errors.py
# Compiled at: 2017-08-07 09:58:40
# Size of source mod 2**32: 290 bytes
EXCEED_MAX_SIZE = '\n    <Error>\n        <Code>EntityTooLarge</Code>\n        <Message>Your proposed upload exceeds the maximum\n                 allowed size</Message>\n        <MaxSizeAllowed>{max_size}</MaxSizeAllowed>\n        <ProposedSize>{proposed_size}</ProposedSize>\n    </Error>\n'