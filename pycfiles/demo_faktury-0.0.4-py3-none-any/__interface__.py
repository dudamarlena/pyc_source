# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: <demo_faktury-0.0.4>\__interface__.py
# Compiled at: 2020-03-26 17:02:32
# Size of source mod 2**32: 221 bytes
"""
Interface for extraction plugins.

Each plugin is a module (file) in package `plugins` that provides at a minimum the `extract`
function with those arguments:

def extract(settings, optimized_str, output)
"""