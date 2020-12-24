# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dave/checkouts/prompter/build/lib/prompter/_version.py
# Compiled at: 2015-01-17 19:54:57
version_version = '0.3.8-dirty'
version_full = '8013d0796c8f6ed65359d42174f115cb84476d33-dirty'

def get_versions(default={}, verbose=False):
    return {'version': version_version, 'full': version_full}