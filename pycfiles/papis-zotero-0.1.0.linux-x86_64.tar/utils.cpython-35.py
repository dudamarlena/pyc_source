# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/papis_zotero/utils.py
# Compiled at: 2019-04-04 21:02:46
# Size of source mod 2**32: 230 bytes
import os, re

def is_pdf(filepath):
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'rb') as (fd):
        magic = fd.read(8)
    return re.match('%PDF-.\\..', magic.decode()) is not None