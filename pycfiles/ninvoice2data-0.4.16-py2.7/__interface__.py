# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ninvoice2data/extract/plugins/__interface__.py
# Compiled at: 2019-02-01 05:18:39
"""
Interface for extraction plugins.

Each plugin is a module (file) in package `plugins` that provides at a minimum the `extract`
function with those arguments:

def extract(settings, optimized_str, output)
"""