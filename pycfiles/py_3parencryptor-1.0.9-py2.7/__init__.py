# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hpe3parencryptor/__init__.py
# Compiled at: 2018-10-26 08:18:02
"""
HPE 3PAR Encryption Utility.
:Author: Anand Totala
:Copyright: Copyright 2012-2016 Hewlett Packard Enterprise Development LP
:License: Apache v2.0
"""
version_tuple = (1, 0, 9)

def get_version_string():
    """Current version of HPE3PARClient."""
    if isinstance(version_tuple[(-1)], str):
        return ('.').join(map(str, version_tuple[:-1])) + version_tuple[(-1)]
    return ('.').join(map(str, version_tuple))


version = get_version_string()