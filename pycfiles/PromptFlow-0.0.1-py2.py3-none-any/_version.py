# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/dave/checkouts/prompter/build/lib/prompter/_version.py
# Compiled at: 2015-01-17 19:54:57
version_version = '0.3.8-dirty'
version_full = '8013d0796c8f6ed65359d42174f115cb84476d33-dirty'

def get_versions(default={}, verbose=False):
    return {'version': version_version, 'full': version_full}