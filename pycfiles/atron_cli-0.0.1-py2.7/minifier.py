# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/atron_cli/minifier.py
# Compiled at: 2019-03-27 01:48:37


def minify(input_file):
    import python_minifier
    with open(input_file, 'r') as (handler):
        return python_minifier.minify(handler.read())