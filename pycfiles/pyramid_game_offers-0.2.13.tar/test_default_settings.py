# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/unit/test_default_settings.py
# Compiled at: 2017-02-24 16:57:38
__doc__ = '\nTest for recognizing default settings.\n\nAlso helps to keeping them in line.\n'

def test_defaults(default_config):
    """Load defaults config for fullauth."""
    assert 'fullauth' in default_config.registry['config']
    assert default_config.registry['config']['fullauth']['check_csrf'] is True
    assert default_config.registry['config']['fullauth']['AuthTkt']['hashalg'] is not 'md5'