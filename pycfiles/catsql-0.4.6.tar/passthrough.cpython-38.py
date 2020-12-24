# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__HANDLERS__/passthrough/passthrough.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 828 bytes


def handle(context):
    return context.get('cs_content', '')