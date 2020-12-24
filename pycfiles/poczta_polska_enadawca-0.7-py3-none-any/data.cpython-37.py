# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/boyhack/programs/pocsuite3/pocsuite3/lib/core/data.py
# Compiled at: 2019-03-15 03:35:12
# Size of source mod 2**32: 630 bytes
from pocsuite3.lib.core.datatype import AttribDict
from pocsuite3.lib.core.log import LOGGER
logger = LOGGER
conf = AttribDict()
kb = AttribDict()
cmd_line_options = AttribDict()
merged_options = AttribDict()
paths = AttribDict()