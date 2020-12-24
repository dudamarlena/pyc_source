# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\i18n\tests\test_toolboxadmi18n.py
# Compiled at: 2011-07-14 06:09:08


def test_support_explicit_lang():
    """Test that i18n msg extraction handles arguments in gettext calls correctly."""
    assert _('Something', 'en') == 'Something'
    assert _('New', 'en') == 'New'