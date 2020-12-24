# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/test_default_settings.py
# Compiled at: 2017-02-24 16:57:38
"""
Test for recognizing default settings.

Also helps to keeping them in line.
"""

def test_defaults(default_config):
    """Load defaults config for fullauth."""
    assert 'fullauth' in default_config.registry['config']
    assert default_config.registry['config']['fullauth']['check_csrf'] is True
    assert default_config.registry['config']['fullauth']['AuthTkt']['hashalg'] is not 'md5'